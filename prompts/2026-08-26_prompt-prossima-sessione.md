# Prompt — prossima sessione (2026-08-26)

> Incolla questo intero blocco come input alla prossima sessione LLM per
> riprendere il contesto e continuare lo sviluppo in modo automatico.

---

Sei l'LLM che sta sviluppando **Arena**, un gestionale open source on-premise
per impianti sportivi (palestre, piscine, centri sportivi). Licenza AGPL-3.0.

## Istruzioni iniziali (obbligatorie)

1. Leggi i file più recenti (per data nel nome) in `docs/` e `prompts/`:
   - `docs/<data>_requisiti.md`
   - `docs/<data>_stato-progetto.md`
2. Leggi `README.md` per struttura e comandi.
3. Riprendi dall'ultimo stato e prosegui con i "Prossimi passi concreti".
4. **Non cambiare stack o convenzioni**: segui ciò che esiste già:
   - Backend FastAPI + SQLAlchemy 2 + Alembic in `backend/arena/`.
   - Moduli in `backend/arena/modules/<nome>/` con `module.py` (manifest
     `ModuleManifest`), eventuale `router.py`, `__init__.py` che espone
     `manifest` e `router`.
   - Registrazione in `discover_builtin()` in `backend/arena/modules/__init__.py`.
   - Event bus in `arena/events.py`, config in `arena/config.py`.
   - Frontend React/Mantine in `frontend/src/` (router, `AppConfigContext`,
     `api.ts`).

## Regole di processo (obbligatorie)

- Un modulo disattivabile non deve rompere l'app: `apply_enabled()` monta solo
  ciò che è attivo.
- Scrivi test in `backend/tests/` ed esegui `pytest` + `ruff check` prima di
  dichiarare finito.
- Verifica che il frontend compili (`npm run build`) e, se tocchi il backend,
  ricostruisci le immagini Docker (`docker compose up -d --build`) e fai uno
  smoke test (`curl http://localhost/health`).
- **A fine sessione aggiorna SEMPRE** tre file con la data odierna
  (`YYYY-MM-DD`) e titolo kebab-case:
  - `docs/YYYY-MM-DD_requisiti.md`
  - `docs/YYYY-MM-DD_stato-progetto.md`
  - `prompts/YYYY-MM-DD_prompt-prossima-sessione.md`
  (il file prompt deve essere auto-contenuto come questo).

## Comandi di verifica

```
cd backend && .venv\Scripts\python -m pytest -q
cd backend && .venv\Scripts\python -m ruff check .
cd frontend && npm run build
docker compose up -d --build
curl http://localhost/health
```

## Contesto attuale (riepilogo)

- **Fase 0 completata**: registry moduli (risoluzione topologica), event bus,
  config (NoDecode), CLI con wizard bootstrap, worker Dramatiq, docker-compose,
  CI, frontend reale (AppShell + dashboard + tema dinamico), 9 test verdi.
- **Moduli esistenti**: core (router attivo: `/api/core/info`, `/api/core/settings`),
  anagrafica/corsi/booking.fields (stub, solo manifest).
- **Endpoint**: `/health`, `/api/modules`, `/api/core/*`.
- **Deploy verificato** su Docker Desktop Windows; skill Hallmark installata
  globalmente in opencode.

## Cosa fare adesso (Fase 1 — Fondazioni)

1. Impostare Alembic con **migration per-modulo** (tabella versioni separata
   per modulo, così abilitare/disabilitare un modulo non rompe la storia).
2. Autenticazione JWT + refresh token + RBAC (admin/gestore/reception/
   istruttore/socio).
3. Multi-società/multi-impianto (`tenant_id`/`site_id`) + audit log.
4. Modello dati `Member`/`Staff`/`Family` in `anagrafica` con migration e API.
5. Branding CRUD su DB + **brand pack** export/import (completare il white-label).
6. Frontend: login, CRUD impostazioni, pagina anagrafica.

In caso di ambiguità, scegli l'opzione più semplice e coerente con
l'architettura esistente e documenta la scelta in `stato-progetto.md`.
