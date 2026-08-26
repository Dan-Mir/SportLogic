# SportLogic — gestionale open source per impianti sportivi

> **Nota:** il codice usa ancora il prefisso tecnico `ARENA_*` e il package
> Python `arena` (eredità del codename iniziale). La rinominazione interna è
> prevista prima della prima release pubblica.

Gestionale **on-premise** per palestre, piscine e centri sportivi. Pensato per
dare alle imprese il controllo totale dei propri dati (niente cloud, niente data
breach), con moduli attivabili in fase di installazione.

## Cosa fa

Iscrizioni, prenotazioni (corsi/lezioni e campi/impianti), convenzioni regionali,
certificati medici, ingressi (tornelli via plugin), tessere ricaricabili con
crediti, documenti automatici, dashboard, notifiche e un chatbot interno con
function calling (LLM locale via Ollama).

## Principi

- **On-premise**: un `docker compose up`, dati in casa del cliente.
- **Modulare**: ogni modulo è registrato in un registry, con dipendenze e
  migration separate. Si installa solo ciò che serve (es. una piscina attiva
  `corsi` ma non `booking.fields`).
- **White-label**: tema (colori/logo/testi) configurabile dall'interfaccia, con
  "brand pack" esportabile.
- **Privacy by design**: i certificati medici sono dati sanitari (GDPR art. 9).

## Stack

- Backend: Python 3.12+, FastAPI, SQLAlchemy 2, Alembic
- Frontend: React + TypeScript (Vite, Mantine)
- Worker: Dramatiq + Redis
- DB: PostgreSQL · LLM: Ollama (opzionale, locale)
- Deploy: Docker Compose + Caddy (TLS automatico)

## Avvio rapido (sviluppo)

```bash
docker compose up -d          # db, redis, ollama
cd backend && pip install -e ".[dev]"
arena bootstrap               # wizard: scegli i moduli, genera .env
uvicorn arena.main:app --reload
```

## Struttura

```
backend/      API FastAPI + registry moduli + event bus
frontend/     SPA React/TypeScript
worker/       worker Dramatiq
deploy/       docker-compose, Caddy, entrypoint
docs/         requisiti e stato del progetto (versionati per data)
prompts/      prompt di handoff per le sessioni LLM successive
```

## Documentazione di processo

Il progetto si evolve per iterazioni. A fine di ogni sessione vengono aggiornati:

- `docs/YYYY-MM-DD_requisiti.md` — requisiti e decisioni
- `docs/YYYY-MM-DD_stato-progetto.md` — stato attuale, fatto/da fare, blockers
- `prompts/YYYY-MM-DD_prompt-prossima-sessione.md` — prompt da incollare al
  prossimo LLM per riprendere il contesto

## Licenza

[GNU AGPL-3.0](LICENSE)
