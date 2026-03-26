import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from data.connections.database import get_db
from dtos.prospection.criar.request import CriarProspectionRequest
from services.prospection_service import criar, listar, buscar, atualizar_status, processar_resultado
from services.export_service import exportar_leads
from factories.prospection_factory import montar_prompt_prospeccao
from engines.claude_code_engine import executar_claude_code
from engines.ai_api_engine import executar_ai_api
from routers.ws_manager import manager

router = APIRouter(prefix="/api/prospections", tags=["prospections"])


@router.post("")
def criar_prospection(request: CriarProspectionRequest,
                      background_tasks: BackgroundTasks,
                      db: Session = Depends(get_db)):
    try:
        response = criar(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Dispara processamento em background
    background_tasks.add_task(
        _processar_prospection,
        prospection_id=response.id,
        segmento=request.segmento,
        localizacao=request.localizacao,
        quantidade=request.quantidade_leads,
        customizado=request.prompt_customizado,
        engine_tipo=request.engine_tipo,
    )

    return response


@router.get("")
def listar_prospections(db: Session = Depends(get_db)):
    return listar(db)


@router.get("/{prospection_id}")
def buscar_prospection(prospection_id: str, db: Session = Depends(get_db)):
    result = buscar(db, prospection_id)
    if not result:
        raise HTTPException(status_code=404, detail="Prospection nao encontrada")
    return result


async def _processar_prospection(prospection_id: str, segmento: str,
                                  localizacao: str | None, quantidade: int,
                                  customizado: str | None, engine_tipo: str):
    """Background task que executa a engine e salva resultados."""
    from data.connections.database import SessionLocal

    db = SessionLocal()
    try:
        atualizar_status(db, prospection_id, "processando")
        await manager.broadcast(prospection_id, {"status": "processando", "progresso": 10})

        prompt = montar_prompt_prospeccao(segmento, localizacao, quantidade, customizado)

        async def on_progress(status, value):
            await manager.broadcast(prospection_id, {"status": status, "progresso": value})

        if engine_tipo == "claude_code":
            resultado = await executar_claude_code(prompt, on_progress)
        else:
            resultado = await executar_ai_api(prompt, on_progress=on_progress)

        await manager.broadcast(prospection_id, {"status": "parseando", "progresso": 80})

        total = processar_resultado(db, prospection_id, resultado)

        # Auto-export para Azure Blob (datalake)
        try:
            export_result = exportar_leads(db, prospection_id, "json")
            atualizar_status(db, prospection_id, "concluido",
                             arquivo_export_url=export_result["url"])
        except Exception as export_err:
            print(f"[WARN] Auto-export falhou: {export_err}")

        await manager.broadcast(prospection_id, {
            "status": "concluido",
            "progresso": 100,
            "total_leads": total,
        })

    except Exception as e:
        atualizar_status(db, prospection_id, "erro", erro=str(e))
        await manager.broadcast(prospection_id, {"status": "erro", "erro": str(e)})
    finally:
        db.close()
