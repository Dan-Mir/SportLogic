# Stato progetto — 2026-08-26

## Riepilogo sessione

Sessione completa: dall'idea alla **Fase 0 finita e funzionante su Docker
Desktop**, con frontend reale, deploy verificato e skill di design installata.

## Fase corrente: Fase 0 (Setup) — COMPLETATA · prossima: Fase 1

---

## 1. Cosa è stato fatto

### 1.1 Scaffolding monorepo
```
backend/                 FastAPI + registry moduli + event bus + CLI
  arena/
    config.py            pydantic-settings (ARENA_*, .env, NoDecode)
    db.py                SQLAlchemy (engine/session lazy)
    events.py            EventBus (subscribe/emit)
    main.py              app factory + /health + /api/modules
    worker.py            worker Dramatiq (Redis) + actor send_email
    bootstrap.py         wizard di installazione (rich, pulizia ANSI)
    cli.py               arena modules / enable / disable / bootstrap
    modules/
      base.py            ModuleManifest (dataclass)
      registry.py        ModuleRegistry (risoluzione topologica, cicli, reverse-dep)
      __init__.py        discover_builtin() + apply_enabled()
      core/              manifest + router (/api/core/info, /api/core/settings)
      anagrafica/        manifest (stub)
      corsi/             manifest (stub)
      booking_fields/    manifest (stub)
  tests/                 9 test (registry + event bus)
  Dockerfile
frontend/                React 18 + TS + Vite + Mantine v7 + react-router-dom
  src/
    api.ts               bootstrap() → brand + moduli da API
    config.ts            AppConfigContext
    main.tsx             tema dinamico (generateColors dal brand)
    App.tsx              rotte
    layout/AppShellLayout.tsx   header + sidebar (menu da moduli attivi)
    pages/               Dashboard, ModulePage, SettingsPage
  Dockerfile             multi-stage (node → nginx)
deploy/Caddyfile         reverse proxy su :80 (locale)
docker-compose.yml       db, redis, api, worker, frontend, caddy, ollama(profile llm)
.github/workflows/ci.yml backend (ruff+pytest) + frontend (build)
LICENSE                  AGPL-3.0
README.md
.env.example
```

### 1.2 Funzionalità implementate e verificate
- **Registry moduli** con dipendenze, rilevamento cicli, enable/disable.
- **Event bus** pronto per plugin (tornelli, fiscale, chatbot).
- **`apply_enabled()`** monta solo i router dei moduli attivi.
- **Wizard bootstrap** con preset per tipologia impianto.
- **Endpoint** `/health`, `/api/modules`, `/api/core/info`, `/api/core/settings`.
- **Frontend reale**: AppShell con sidebar, dashboard, pagine modulo, pagina
  impostazioni, tema dinamico dal colore brand, menu generato dai moduli.
- **Deploy Docker completo** su Windows/Docker Desktop: tutti i container
  attivi, worker processa task, frontend HTTP 200 via Caddy.

### 1.3 Verifiche eseguite
- Backend: `pytest` 9/9, `ruff check` pulito, smoke test API OK.
- Frontend: `npm run build` OK.
- `docker compose config` valido; stack `up` e endpoint raggiungibili.
- Worker: task `send_email` consumata e loggata correttamente.

### 1.4 Fix applicati durante il primo deploy reale
1. **`config.py`**: `modules_enabled` → `Annotated[list[str], NoDecode]`
   (pydantic-settings tentava `json.loads` sulla stringa CSV e crashava).
2. **`worker.py`**: Dramatiq non ha `.run()`; `start()` non blocca e `join()`
   serve solo nei test → ora `start()` + attesa su `SIGINT`/`SIGTERM` +
   `stop()`; aggiunto `logging.basicConfig`.
3. **`deploy/Caddyfile`**: corretto il blocco (c'era un `{...}` globale errato);
   ora site address `:80` per il locale. Per produzione sostituire con il
   dominio per HTTPS automatico.
4. **`bootstrap.py`**: pulizia sequenze ANSI dagli input (`_clean`) per evitare
   artefatti del terminale (Git Bash) in `.env`.

### 1.5 Tooling installato
- **Skill Hallmark** (anti-AI-slop design) in
  `C:\Users\danym\.config\opencode\skills\hallmark\` (frontmatter adattato:
  rimosso `version`). Richiede riavvio di opencode.

---

## 2. Cosa manca (Fase 1 → Fase 10)

### Fase 1 — Fondazioni (prossima, priorità alta)
- [ ] Autenticazione JWT + refresh token.
- [ ] RBAC (admin/gestore/reception/istruttore/socio).
- [ ] Multi-società/multi-impianto (`tenant_id`/`site_id`).
- [ ] Audit log.
- [ ] Migration Alembic **per-modulo** (tabella versioni separata).
- [ ] Motore branding CRUD su DB + **brand pack** export/import.
- [ ] Modello dati `Member`/`Staff`/`Family` in `anagrafica` + migration.
- [ ] Frontend: form login, CRUD impostazioni, pagina anagrafica.

### Fase 2 — Soldi e salute
- [ ] Modulo `abbonamenti` (piani, rate, rinnovi, ricevute).
- [ ] Modulo `certificati_medici` (upload, scadenze, **cifratura at-rest**).
- [ ] Notifiche email (email MVP).

### Fase 3 — Prenotazioni
- [ ] `corsi` (multi-livello, calendario, capienza, liste d'attesa, istruttori).
- [ ] `booking.fields` (fasce orarie, tariffe stagionali).

### Fase 4 — Accessi e tessere
- [ ] Ingressi manuali da reception + kiosk self check-in.
- [ ] `tessere` (wallet, crediti, fidelity).

### Fase 5-10
- [ ] `convenzioni`, `documenti` (PDF), `dashboard`, `notifiche` avanzate,
  `chatbot` (function calling + RAG, Ollama), plugin `tornelli` e `fiscale`,
  hardening (security audit, DPIA, backup/restore), beta pilota.

---

## 3. Blockers / rischi

- **Nessun blocker tecnico** al momento.
- Rischio principale: **scope enorme** → milestone disciplinate, MVP senza
  tornelli.
- Da decidere (vedi requisiti §12): nome definitivo, SSO, provider documenti/
  firma, modello tenant su carichi reali, provider SMS/WhatsApp, monetizzazione.

## 4. Prossimi passi concreti (per la prossima sessione)

1. Impostare Alembic con **migration per-modulo** (pattern da definire).
2. Implementare auth JWT + refresh + RBAC.
3. Modello dati e API `anagrafica`.
4. Branding CRUD su DB + brand pack (chiudere il cerchio del white-label).
5. Frontend: login + CRUD impostazioni + pagina anagrafica.

Per ripartire in automatico: incollare il contenuto di
`prompts/2026-08-26_prompt-prossima-sessione.md`.
