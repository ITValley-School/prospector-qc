import csv
import json
import io
import os
from datetime import datetime

from sqlalchemy.orm import Session

from models.lead import Lead
from models.lead_contact import LeadContact
from data.connections.blob_storage import upload_blob

TENANT_ID = os.getenv("TENANT_ID", "prospector-qc")


def exportar_leads(db: Session, prospection_id: str, formato: str = "csv") -> dict:
    leads = (
        db.query(Lead)
        .filter(Lead.prospection_id == prospection_id, Lead.tenant_id == TENANT_ID)
        .order_by(Lead.score.desc())
        .all()
    )

    if not leads:
        raise ValueError("Nenhum lead encontrado para exportar")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"export_{prospection_id}_{timestamp}"

    if formato == "csv":
        return _exportar_csv(db, leads, filename)
    else:
        return _exportar_json(db, leads, filename)


def _exportar_csv(db: Session, leads, filename: str) -> dict:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Empresa", "Segmento", "Website", "Descricao", "Score", "Status",
        "Contato Nome", "Contato Cargo", "Contato Email", "Contato Telefone", "Contato LinkedIn"
    ])

    for lead in leads:
        contatos = (
            db.query(LeadContact)
            .filter(LeadContact.lead_id == lead.id, LeadContact.tenant_id == TENANT_ID)
            .all()
        )

        if contatos:
            for c in contatos:
                writer.writerow([
                    lead.nome_empresa, lead.segmento, lead.website, lead.descricao,
                    lead.score, lead.status,
                    c.nome, c.cargo, c.email, c.telefone, c.linkedin,
                ])
        else:
            writer.writerow([
                lead.nome_empresa, lead.segmento, lead.website, lead.descricao,
                lead.score, lead.status,
                "", "", "", "", "",
            ])

    data = output.getvalue().encode("utf-8-sig")
    blob_name = f"{filename}.csv"
    url = upload_blob(blob_name, data, "text/csv; charset=utf-8")

    return {"url": url, "formato": "csv", "total_leads": len(leads)}


def _exportar_json(db: Session, leads, filename: str) -> dict:
    result = []
    for lead in leads:
        contatos = (
            db.query(LeadContact)
            .filter(LeadContact.lead_id == lead.id, LeadContact.tenant_id == TENANT_ID)
            .all()
        )
        result.append({
            "nome_empresa": lead.nome_empresa,
            "segmento": lead.segmento,
            "website": lead.website,
            "descricao": lead.descricao,
            "score": lead.score,
            "status": lead.status,
            "contatos": [
                {"nome": c.nome, "cargo": c.cargo, "email": c.email,
                 "telefone": c.telefone, "linkedin": c.linkedin}
                for c in contatos
            ],
        })

    data = json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8")
    blob_name = f"{filename}.json"
    url = upload_blob(blob_name, data, "application/json")

    return {"url": url, "formato": "json", "total_leads": len(leads)}
