# Stato progetto — 2026-10-06

## Riepilogo sessione

Completato il primo blocco della **Fase 1** rimasta in sospeso e allineata la
documentazione. In particolare:

- **Audit log**: tabella `audit_log`, migration `0003`, hook `log_action`
  applicato a login, create user, branding CRUD e a tutti gli endpoint
  anagrafica (create/update/delete di member, staff, family).
- **CRUD anagrafica**: aggiunti endpoint PUT/DELETE per member, staff e family.
- **Lista utenti**: nuovo endpoint `GET /api/core/users` e pagina frontend
  `/users` con elenco e modale creazione.
- **Impostazioni brand interattive**: SettingsPage ora permette modifica nome/
  colore/dominio in tempo reale + export/import brand pack via UI.
- **29 test backend** (tutti verdi), ruff pulito, frontend build OK.

## Fase corrente: Fase 1 — COMPLETATA · prossima: Fase 2

---

## 1. Cosa è stato fatto

### 1.1 Audit log
- Modello `AuditLog` in `core/models.py` (user_id, action, resource,
  resource_id, detail, ip_address, created_at).
- Migration `0003_create_audit_log.py` con indici su user_id, action,
  created_at.
- Funzione `log_action()` e helper `get_client_ip()` in `core/deps.py`.
- Audit applicato a:
  - `POST /api/core/auth/login`
  - `POST /api/core/users`
  - `PUT /api/core/branding`
  - `POST /api/core/branding/import`
  - `POST /api/anagrafica/members`, `/staff`, `/families`
  - `PUT  /api/anagrafica/members/:id`, `/staff/:id`, `/families/:id`
  - `DELETE /api/anagrafica/members/:id`, `/staff/:id`, `/families/:id`

### 1.2 CRUD anagrafica completo
- Aggiunti endpoint PUT/DELETE per Member, Staff, Family (erano solo
  list/create/get).
- Aggiunti schemi `MemberUpdate`, `StaffUpdate`, `FamilyUpdate` con campi
  opzionali (partial update via `exclude_unset`).

### 1.3 Gestione utenti
- Nuovo endpoint `GET /api/core/users` (admin‑only, lista ordinata).
- Nuova pagina frontend `UsersPage` con tabella utenti e modale di creazione.

### 1.4 Branding interattivo
- SettingsPage: form editabile per nome brand, colore primario, dominio
  pubblico con salvataggio via `PUT /api/core/branding`.
- Pulsante "Esporta brand pack" → download JSON.
- Pulsante "Importa brand pack" → modale con textarea JSON.
- Pulsanti "Annulla" e "Salva" ovunque.

### 1.5 Test
- `test_audit_log.py` (4 test): login, user.create, branding.update,
  member.create.
- CRUD anagrafica testato indirettamente via audit log test.
- Totale: 29 test, tutti verdi.

### 1.6 Decisioni
- **Multi-tenant**: rinviato a post-MVP. Le entità esistenti non hanno
  `tenant_id`/`site_id`. Quando servirà, si adotterà single-DB + filtro.

---

## 2. Cosa manca (Fase 2 → Fase 10)

### Fase 2 — Soldi e salute (prossima, priorità alta)
- [ ] Modulo `abbonamenti` (piani, rate, rinnovi, ricevute).
- [ ] Modulo `certificati_medici` (upload, scadenze, **cifratura at-rest**).
- [ ] Notifiche email (MVP — rendere reale l'actor `send_email` in worker).

### Fase 3 — Prenotazioni
- [ ] `corsi` (multi-livello, calendario, capienza, liste d'attesa, istruttori).
- [ ] `booking.fields` (fasce orarie, tariffe stagionali).

### Fase 4-10
- [ ] Tessere, convenzioni, documenti PDF, dashboard, notifiche avanzate,
  chatbot, plugin tornelli/fiscale, hardening, beta pilota.

---

## 3. Blockers / rischi

- **Nessun blocker tecnico** al momento.
- Decisioni ancora aperte: nome definitivo, SSO, provider documenti/firma,
  provider SMS/WhatsApp, strategia monetizzazione.

## 4. Prossimi passi concreti (per la prossima sessione)

1. Modulo **abbonamenti**: piani, rate, rinnovi automatici, solleciti morosità,
   ricevute (entità + migration + API + frontend).
2. Modulo **certificati medici**: upload file, scadenze, cifratura at-rest
   (crittografia lato applicazione con chiave derivata da secret).
3. **Notifiche email**: rendere operativo l'actor `send_email` (con SMTP
   configurato).