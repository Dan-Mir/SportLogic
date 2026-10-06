# Prompt — prossima sessione (2026-10-06)

> Incolla questo intero blocco come input alla prossima sessione LLM per
> riprendere il contesto e continuare lo sviluppo in modo automatico.

---

Sei l'LLM che sta sviluppando **SportLogic**, un gestionale open source on-premise
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
cd backend && source .venv/bin/activate && python -m pytest -q
cd backend && source .venv/bin/activate && ruff check .
cd frontend && npm run build
```

## Contesto attuale (riepilogo)

- **Fase 1 completata**: auth JWT+RBAC, audit log, anagrafica CRUD, branding
  CRUD + brand pack export/import, migration per-modulo, pagine frontend login/
  soci/utenti/settings.
- **29 test verdi**, ruff pulito, frontend build OK.
- **Multi-tenant**: rimandato a post-MVP.
- **Moduli esistenti**: core (attivo), anagrafica (attivo), corsi (stub),
  booking.fields (stub).
- **Worker**: actor `send_email` già presente ma usa solo `print`.
- **ORMAI NON C'E' PIU' IL DOCKER DESKTOP** — il deploy locale si testa via
  `pip install -e ".[dev]"` + `python -m pytest`.

## Cosa fare adesso (Fase 2 — Soldi e salute)

1. **Modulo `abbonamenti`**: entità SubscriptionPlan, Subscription, Payment;
   migration; CRUD API; frontend base.
2. **Modulo `certificati_medici`**: upload file con cifratura at-rest (crypto
   lato app con chiave derivata da `secret_key`), scadenze, alert.
3. **Notifiche email**: configurare SMTP (settings), rendere `send_email`
   funzionante, trigger alla creazione di un abbonamento o scadenza
   certificato.

In caso di ambiguità, scegli l'opzione più semplice e coerente con
l'architettura esistente e documenta la scelta in `stato-progetto.md`.
