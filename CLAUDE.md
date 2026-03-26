# Prospector QC — Sistema de Prospeccao B2B com IA

## O que e
Sistema de prospeccao B2B que usa IA multi-motor (Claude Code CLI, OpenAI, Anthropic, Google Gemini) para encontrar leads qualificados. Inclui enriquecimento via Firecrawl e export CSV/JSON para Azure Blob.

## Stack
- Frontend: SvelteKit + Tailwind v4 + Design System Petra IA v2 (Outfit font)
- Backend: Python FastAPI (estrutura IT Valley — tudo na raiz de backend/)
- DB: SQL Server Azure (dblumina, schema prospector)
- Storage: Azure Blob (saprospectorqc/sistemaprospect)
- Engines: Claude Code CLI, OpenAI API, Anthropic API, Google Gemini API
- Enricher: Firecrawl API

## Estrutura
```
prospector-qc/
  backend/
    main.py
    routers/          # prospection, lead, engine, export, settings, health
    services/         # prospection, lead, engine, settings, export
    factories/        # prospection_factory, lead_factory
    mappers/          # prospection_mapper, lead_mapper, engine_mapper
    engines/          # claude_code_engine, ai_api_engine
      providers/      # openai, anthropic, google
    enrichers/        # firecrawl_enricher
    dtos/             # por dominio/caso-de-uso
    models/           # prospection, lead, lead_contact, enrichment, engine_config, setting
    data/             # connections (database, blob_storage)
    tests/            # test_factories
    .env
  frontend/
    src/
      routes/         # /, /resultados, /resultados/[id], /historico, /configuracoes
      lib/
        components/   # ui/ (Button, Card, Badge, Input, Select, Modal, ProgressBar, DataTable), layout/ (Navbar)
        dtos/         # prospection, lead, engine
        services/     # prospection-service, engine-service, websocket-service
        repositories/ # prospection-repository, engine-repository (mock/real via VITE_USE_MOCK)
        mocks/        # prospections, engines
        utils/        # status
    .env
```

## API Routes
```
POST /api/prospections         → criar prospeccao (dispara engine em background)
GET  /api/prospections         → listar todas
GET  /api/prospections/{id}    → detalhe com leads
GET  /api/leads/prospection/{id} → leads de uma prospeccao
GET  /api/leads/{id}           → detalhe do lead com contatos
GET  /api/engines              → listar engines configuradas
POST /api/engines              → configurar engine
POST /api/export/{id}          → exportar leads (CSV/JSON) → blob
GET  /api/settings             → listar settings
POST /api/settings             → salvar setting
GET  /api/settings/{chave}     → buscar setting
GET  /health                   → health check
WS   /ws/prospection/{id}      → progresso real-time
```

## Como rodar
```bash
# Backend
cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Frontend
cd frontend && npm run dev -- --port 5175 --host 0.0.0.0

# Testes backend
cd backend && source venv/bin/activate && python -m pytest tests/ -v

# Testes frontend (Playwright)
cd frontend && npx playwright test
```

## Portas
- Frontend: 5175
- Backend: 8002

## Azure
- DB: srvmasterclass.database.windows.net / dblumina / schema: prospector
- Storage: saprospectorqc / container: sistemaprospect
- Key Vault: kv-api-key-itvalley
- Web Apps: prospector-qc-api (Python 3.12), prospector-qc-web (Node 20)
- ASP: ASP-rgwebapps-978c (P0v3)
