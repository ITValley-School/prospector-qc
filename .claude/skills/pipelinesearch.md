# Pipeline de Busca — Prospector QC

## Visao Geral

O pipeline de busca e o fluxo completo desde o usuario clicar "Prospectar" ate os leads aparecerem na tela e serem salvos no Azure Blob (datalake).

---

## Fluxo Visual

```
[Usuario preenche formulario]
        |
        v
POST /api/prospections (FastAPI)
        |
        v
+------------------------------+
| 1. VALIDACAO                 |
| - titulo nao vazio           |
| - segmento nao vazio         |
| - engine: claude_code|ai_api |
| - quantidade: 1 a 50         |
+------------------------------+
        |
        v
[Salva no SQL Server com status="pendente"]
        |
        v (Background Task)
+------------------------------+
| 2. MONTAGEM DO PROMPT        |
| montar_prompt_prospeccao()   |
| - Injeta: segmento,          |
|   localizacao, quantidade    |
| - Append: instrucoes custom  |
+------------------------------+
        |
        v
+------------------------------+
| 3. EXECUCAO DA ENGINE        |
|                              |
| claude_code:                 |
|   $ claude -p "prompt"       |
|     --output-format json     |
|                              |
| ai_api:                      |
|   OpenAI (gpt-4o)           |
|   Anthropic (claude-sonnet)  |
|   Google (gemini-2.0-flash)  |
+------------------------------+
        |
        v
+------------------------------+
| 4. PARSING DO RESULTADO      |
| parsear_resultado_ia()       |
| - Remove markdown ```json    |
| - Encontra [ ... ] no texto  |
| - JSON.parse                 |
| - Valida que e um array      |
+------------------------------+
        |
        v
+------------------------------+
| 5. CRIACAO DE LEADS          |
| Para cada item do array:     |
| - Cria Lead no banco         |
| - Cria LeadContacts          |
| (nome, cargo, email, tel)    |
+------------------------------+
        |
        v
+------------------------------+
| 6. AUTO-EXPORT DATALAKE      |
| - Gera JSON com leads+contatos|
| - Upload Azure Blob Storage  |
| - Salva URL no prospection   |
+------------------------------+
        |
        v
[status="concluido" + WebSocket broadcast]
```

---

## Prompt Template (Etapa 2)

```
Voce e um especialista em prospeccao B2B. Encontre {quantidade} empresas reais
do segmento "{segmento}" localizadas em "{localizacao}".

Para cada empresa, retorne um JSON array com objetos contendo:
- nome_empresa: nome completo da empresa
- segmento: segmento de atuacao
- website: URL do site oficial
- descricao: breve descricao da empresa (2-3 frases)
- score: nota de 0 a 10 indicando relevancia para prospeccao
- contatos: array com objetos contendo nome, cargo, email, telefone, linkedin

IMPORTANTE:
- Retorne APENAS o JSON array, sem texto adicional
- Use dados reais e verificaveis
- Priorize empresas de medio e grande porte
- Inclua pelo menos 1 contato por empresa quando possivel

{instrucoes_customizadas}
```

### Parametros injetados:
| Parametro | Origem | Exemplo |
|-----------|--------|---------|
| `quantidade` | Campo "Quantidade de leads" | 10 |
| `segmento` | Campo "Segmento" | Restaurantes |
| `localizacao` | Campo "Localizacao" (opcional) | Quebec, Canada |
| `instrucoes_customizadas` | Campo "Instrucoes adicionais" | Quero telefone e email |

---

## Instrucoes do Sistema por Provider (Etapa 3)

Cada provider recebe uma instrucao de sistema ANTES do prompt:

| Provider | System Instruction | Modelo | Max Tokens |
|----------|-------------------|--------|------------|
| OpenAI | "Voce e um especialista em prospeccao B2B. Responda sempre em JSON." | gpt-4o | 4096 |
| Anthropic | "Voce e um especialista em prospeccao B2B. Responda sempre em JSON." | claude-sonnet-4-20250514 | 4096 |
| Google | (prepended ao prompt) | gemini-2.0-flash | - |
| Claude Code CLI | (sem system, prompt direto) | modelo do CLI | - |

---

## Formato de Resposta Esperado (Etapa 4)

O parser espera um JSON array assim:

```json
[
  {
    "nome_empresa": "Pizzeria Napoletana",
    "segmento": "Restaurante Italiano",
    "website": "https://www.napoletana.com",
    "descricao": "Pizzaria tradicional fundada em 1948...",
    "score": 8.5,
    "contatos": [
      {
        "nome": "Mario Rossi",
        "cargo": "Proprietario",
        "email": "mario@napoletana.com",
        "telefone": "+1-514-555-1234",
        "linkedin": "https://linkedin.com/in/mariorossi"
      }
    ]
  }
]
```

---

## Estrutura de Dados Persistidos (Etapa 5)

### Tabela: prospector.leads
| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | UUID | PK |
| prospection_id | UUID | FK → prospections |
| nome_empresa | String(300) | Nome da empresa |
| segmento | String(200) | Segmento |
| website | String(500) | URL do site |
| descricao | Text | Descricao |
| score | Float | 0-10 |
| status | String(50) | "novo" |

### Tabela: prospector.lead_contacts
| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | UUID | PK |
| lead_id | UUID | FK → leads |
| nome | String(200) | Nome do contato |
| cargo | String(200) | Cargo |
| email | String(300) | Email |
| telefone | String(50) | Telefone |
| linkedin | String(500) | LinkedIn |

---

## Datalake / Azure Blob (Etapa 6)

- **Storage Account**: saprospectorqc
- **Container**: sistemaprospect
- **Formato**: `export_{prospection_id}_{timestamp}.json`
- **Conteudo**: JSON com leads + contatos completos
- **URL salva em**: prospection.arquivo_export_url

---

## Arquivos do Pipeline

| Etapa | Arquivo | Funcao |
|-------|---------|--------|
| Validacao | `factories/prospection_factory.py` | `criar_prospection()` |
| Prompt | `factories/prospection_factory.py` | `montar_prompt_prospeccao()` |
| Orquestracao | `routers/prospection.py` | `_processar_prospection()` |
| Engine Claude | `engines/claude_code_engine.py` | `executar_claude_code()` |
| Engine AI API | `engines/ai_api_engine.py` | `executar_ai_api()` |
| Provider OpenAI | `engines/providers/openai_provider.py` | `chamar_openai()` |
| Provider Anthropic | `engines/providers/anthropic_provider.py` | `chamar_anthropic()` |
| Provider Google | `engines/providers/google_provider.py` | `chamar_google()` |
| Parser | `factories/lead_factory.py` | `parsear_resultado_ia()` |
| Leads | `factories/lead_factory.py` | `criar_lead_from_dict()` |
| Contatos | `factories/lead_factory.py` | `criar_contatos_from_dict()` |
| Export | `services/export_service.py` | `exportar_leads()` |
| Blob | `data/connections/blob_storage.py` | `upload_blob()` |
| WebSocket | `routers/ws_manager.py` | `manager.broadcast()` |

---

## O que pode ser melhorado

1. **Fonte dos dados**: Hoje a IA responde do conhecimento proprio (training data). Pode ser impreciso. Integrar com Google Maps API, SerpAPI, ou Firecrawl para dados reais.
2. **Enriquecimento**: O modelo `Enrichment` existe mas nao esta sendo usado. Pode scrape do site real para validar dados.
3. **Retry**: Se a IA retornar formato invalido, nao ha retry. Pode re-solicitar com prompt mais restritivo.
4. **Rate limiting**: Sem controle de quota por provider.
5. **Prompt tuning**: O prompt pode ser mais especifico por segmento/pais.
