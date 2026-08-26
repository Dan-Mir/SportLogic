# Requisiti — Gestionale impianti sportivi (2026-08-26)

> Documento di riferimento dei requisiti. Aggiornato a fine sessione.
> Nome di progetto **provvisorio**: "Arena" (codename da sostituire prima della
> prima release pubblica).

## 1. Visione e obiettivi

Gestionale **open source on-premise** per imprese sportive: palestre, piscine,
centri sportivi con campi (calcio, padel, tennis), e impianti multi-disciplinari.

Obiettivo: dare alle imprese la gestione **completamente autonoma e senza data
breach** di tutte le operazioni quotidiane, senza lock-in su SaaS cloud e senza
canoni ricorrenti. L'installazione avviene su infrastruttura del cliente
(`docker compose up`), con dati che non lasciano mai la rete locale.

## 2. Punti di forza / differenziatori

1. **On-premise, zero data breach** — specialmente rilevante perché i
   certificati medici sono dati sanitari (GDPR art. 9).
2. **Modulare e configurabile all'installazione** — si installa solo ciò che
   serve (es. una piscina attiva `corsi` ma non `booking.fields`); i moduli
   sono aggiungibili in un secondo momento senza downtime.
3. **White-label** — branding configurabile in pochi minuti dall'interfaccia.
4. **Chatbot interno con function calling** su LLM locale (Ollama), coerente
   con la filosofia "i dati non escono".

## 3. Principi guida

1. **On-premise**: un solo `docker compose up`, dati in casa del cliente.
2. **Modulare**: ogni modulo = package con manifest, dipendenze, migration
   separate; registry centrale + event bus interno.
3. **White-label**: tema (colori/logo/testi/template) configurabile, brand pack
   esportabile/importabile.
4. **Privacy by design**: cifratura at-rest per dati sanitari, retention, audit.
5. **Convention over configuration**: default sensati, ma tutto override-abile.

## 4. Decisioni prese (aggiornate al 2026-08-26)

| Tema | Decisione |
|------|-----------|
| Backend | Python 3.12+, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2 |
| Frontend | React 18 + TypeScript + Vite + Mantine v7 + react-router-dom + @tabler/icons-react |
| Worker | Dramatiq + Redis |
| DB | PostgreSQL 16 |
| Licenza | AGPL-3.0-or-later |
| Chatbot | Ollama locale (default) + endpoint OpenAI-compatibile opzionale; function calling via tool registry interno |
| MVP scope | Tutto tranne i **tornelli** (plugin post-MVP, hardware di terze parti) |
| Multi-tenant | singolo DB, filtro `tenant_id`/`site_id` (schema-per-tenant da validare su carichi reali) |
| Modelli impianto | `palestra`, `piscina`, `centro_sportivo`, `multi` → preset moduli nel wizard |
| Deploy | Docker Compose + Caddy (TLS automatico in produzione; `:80` in locale) |
| Design | Skill **Hallmark** installata (opencode globale) per future UI |

## 5. Architettura tecnica

- **Monolito modulare** (non microservizi): un container API, uno worker, uno
  frontend; i moduli sono package Python con `ModuleManifest`.
- **Registry moduli** (`arena/modules/registry.py`): risoluzione topologica
  delle dipendenze, rilevamento cicli, enable/disable con controllo reverse-dep.
- **Event bus** (`arena/events.py`): subscribe/emit per agganciare plugin
  (tornelli, fiscale, chatbot) senza toccare il core.
- **`apply_enabled()`** monta solo i router dei moduli attivi; il menu frontend
  è generato dinamicamente da `GET /api/modules`.
- **Migration per modulo**: ogni modulo ha la propria tabella versioni Alembic,
  così abilitare/disabilitare un modulo non rompe la storia migrazioni.
- **Config** (`arena/config.py`): pydantic-settings, prefisso `ARENA_`, file
  `.env`. Nota: i campi lista usano `Annotated[list, NoDecode]` (vedi fix).
- **Monorepo**: `backend/ frontend/ worker(=backend/arena/worker.py) deploy/ docs/ prompts/`.

## 6. Moduli

| Nome | Dipendenze | Stato | Note |
|------|-----------|-------|------|
| core | — | ✅ attivo (Fase 0) | auth/RBAC (da fare), settings, branding, `/api/modules` |
| anagrafica | core | 🟡 stub | soci, staff, famiglie, minori/tutori |
| corsi | core, anagrafica | 🟡 stub | corsi multi-livello, calendario, capienza |
| booking.fields | core, anagrafica | 🟡 stub | campi/fasce orarie, tariffe stagionali |
| abbonamenti | core, anagrafica | ⬜ da fare | piani, rate, solleciti, ricevute |
| certificati_medici | core, anagrafica | ⬜ da fare | upload, scadenze, cifratura |
| iscrizioni | core, anagrafica | ⬜ da fare | portale pubblico, rinnovi |
| tessere | core, anagrafica | ⬜ da fare | wallet, crediti, fidelity |
| convenzioni | core, anagrafica | ⬜ post-MVP | aziendali/regionali, welfare, rimborsi |
| documenti | core | ⬜ post-MVP | PDF da template, firma |
| dashboard | core | ⬜ post-MVP | KPI, occupazione, incassi |
| notifiche | core | ⬜ (email MVP) | email → SMS/WhatsApp |
| chatbot | core | ⬜ post-MVP | function calling, RAG |
| tornelli (plugin) | core, tessere | ⬜ post-MVP | adapter hardware, whitelist offline |
| fiscale (plugin) | core | ⬜ post-MVP | corrispettivi, FE, PagoPA |

Legenda: ✅ implementato · 🟡 scheletro · ⬜ non iniziato

## 7. Requisiti funzionali per area

### 7.1 Core / Auth / RBAC (Fase 1)
- Autenticazione JWT + refresh token; opzionale SSO/OIDC per impianti comunali.
- Ruoli minimi: `admin`, `gestore`, `reception`, `istruttore`, `socio`.
- Multi-società e multi-impianto: filtro `tenant_id` + `site_id` su tutte le
  query; un utente può appartenere a più società.
- Audit log su operazioni sensibili (chi, cosa, quando, su chi).
- Impostazioni per-tenant (non solo globali).

### 7.2 Anagrafica
- Soci: dati anagrafici, contatti, foto, documenti identità, consensi GDPR.
- Staff e istruttori con qualifiche e certificazioni.
- Famiglie e minori con tutori esercenti la potestà.
- Duplicati (dedup per codice fiscale), import/export CSV.

### 7.3 Iscrizioni
- Portale pubblico white-label (dominio custom).
- Moduli di iscrizione online, rinnovi, iscrizioni stagionali.
- Gestione liste d'attesa.

### 7.4 Abbonamenti & pagamenti
- Piani (mensile, stagionale, a ingressi), rinnovi automatici.
- Rate e rateizzazione; solleciti morosità (via notifiche).
- Ricevute e quietanze; movimenti contabili.
- Nota fiscale: per ASD/SSD gestire il regime agevolato (esenzione IVA,
  tracciabilità incassi) — rimanda al plugin fiscale.

### 7.5 Certificati medici (GDPR art. 9)
- Upload documento, data di validità, scadenze con alert automatici.
- Blocco accesso (tornello/reception) se certificato scaduto.
- **Cifratura at-rest** del documento; retention policy; consenso esplicito.
- DPIA obbligatoria; minimizzazione (non salvare dati clinici oltre il
  necessario).

### 7.6 Corsi e lezioni
- Corsi multi-livello (es. nuoto: livelli, corsie), calendario stagionale.
- Capienza massima, liste d'attesa, iscrizioni e pagamento corso.
- Assenze e recuperi; istruttori e sostituzioni.

### 7.7 Impianti / campi
- Fasce orarie, tariffe stagionali e per fascia (picco/non picco).
- Campi padel/calcio/tennis; prenotazione, check-in, no-show.

### 7.8 Tessere ricaricabili & wallet
- Tessera con crediti; ricariche (reception, online, kiosk).
- Fidelity/loyalty (punti, sconti); storico movimenti.
- Emissione badge (QR/RFID) per accessi.

### 7.9 Convenzioni
- Convenzioni aziendali/regionali: listini convenzionati, rimborsi.
- Welfare aziendale (flussi di import/export verso portali welfare).

### 7.10 Accessi / tornelli (post-MVP)
- MVP: ingressi manuali da reception + kiosk self check-in.
- Modello astratto da subito: entità `AccessEvent` + endpoint HTTP di verifica
  badge; adapter per hardware (HTTP/MQTT/websocket/RS485).
- Whitelist offline locale sul tornello (tolleranza guasti rete).

### 7.11 Documenti automatici
- Generazione PDF da template (contratti, ricevute, deleghe, certificati).
- Provider da decidere: WeasyPrint vs Gotenberg; firma elettronica opzionale.

### 7.12 Dashboard & report
- KPI: occupazione impianti, incassi, scadenze certificati, abbonamenti in
  scadenza; export report.

### 7.13 Notifiche
- Email (MVP) → SMS/WhatsApp (post-MVP); avvisi di massa (maltempo/chiusure);
  sondaggi.

### 7.14 Chatbot (post-MVP)
- Function calling su operazioni ripetibili: prenota, ricarica, stato tessera.
- RAG su regolamenti interni; LLM locale (Ollama) + fallback API esterna.

### 7.15 Fiscale (plugin post-MVP)
- Corrispettivi telematici, fatturazione elettronica, PagoPA.

## 8. Branding / white-label

- Tema via CSS variables + Mantine theme (già implementato: colore primario +
  10 tonalità generate via `@mantine/colors-generator`).
- Logo, favicon, nome, dominio pubblico, testi/traduzioni da tabella settings.
- **Brand pack** JSON esportabile/importabile.
- Template documenti con brand; portale pubblico con dominio custom + TLS.

## 9. Requisiti non funzionali

- **Deploy**: `docker compose up` + wizard bootstrap; backup `pg_dump`
  schedulato + restore testato.
- **GDPR**: dati sanitari cifrati, retention, DPIA, audit log, minimizzazione.
- **Sicurezza**: RBAC fine, rate limiting, secret non in chiaro, TLS.
- **Affidabilità**: idempotenza, coda worker, retry, tolleranza guasti.
- **Testing**: pytest (backend) + test UI; CI (ruff + pytest + build frontend).
- **Osservabilità**: log strutturati (worker già con logging INFO), healthcheck.

## 10. Casi d'uso aggiuntivi (mappati, non prioritari)

Famiglie/minori con tutori · noleggio attrezzature · armadietti/guardaroba ·
gestione staff (turni/presenze) · squadre/tornei agonistici · impianti comunali
in concessione · certificazioni interne (DAE/primo soccorso) · sondaggi ·
punto vendita/bar leggero · solleciti morosità.

## 11. Roadmap

- **Fase 0 — Setup** ✅ completata (vedi stato-progetto).
- **Fase 1 — Fondazioni**: auth JWT+refresh, RBAC, multi-società, audit log,
  migration Alembic per-modulo, branding CRUD + brand pack, modello dati
  `Member`/`Staff`/`Family`, layout frontend completo.
- **Fase 2 — Soldi e salute**: abbonamenti + pagamenti + certificati medici +
  notifiche email.
- **Fase 3 — Prenotazioni**: corsi/lezioni + impianti/campi + calendario.
- **Fase 4 — Accessi e tessere**: ingressi manuali, kiosk, wallet, fidelity.
- **Fase 5 — Convenzioni**: aziendali/regionali/welfare.
- **Fase 6 — Documenti e dati**: PDF automatici, dashboard, report.
- **Fase 7 — AI**: chatbot function calling + notifiche avanzate.
- **Fase 8 — Plugin**: tornelli, fiscale (adapter community).
- **Fase 9 — Hardening**: security audit, DPIA, backup/restore, installer finale.
- **Fase 10 — Beta pilota**: un impianto reale per validare l'MVP.

## 12. Domande aperte

1. Nome definitivo del progetto.
2. SSO/OIDC per impianti comunali: priorità?
3. Provider documenti (WeasyPrint vs Gotenberg) e firma elettronica.
4. Modello tenant: confermare `tenant_id` single-DB vs schema-per-tenant.
5. Provider SMS/WhatsApp da integrare.
6. Strategia di monetizzazione open source (AGPL + offerta managed hosting?).

## 13. Processo di lavoro (obbligatorio)

A fine di ogni sessione si aggiornano SEMPRE, con data odierna nel nome file
(`YYYY-MM-DD`), tre file:

- `docs/YYYY-MM-DD_requisiti.md`
- `docs/YYYY-MM-DD_stato-progetto.md`
- `prompts/YYYY-MM-DD_prompt-prossima-sessione.md`
