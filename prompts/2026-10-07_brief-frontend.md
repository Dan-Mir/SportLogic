# Brief — Rigenerazione frontend SportLogic (2026-10-07)

> Questo file è il **punto di partenza** per rigenerare il frontend da zero.
> Il vecchio UI (pagine, layout, tema, token) è stato eliminato dal working tree
> ed è recuperabile da `master` (`git show master:frontend/src/pages/...`) **solo
> come riferimento funzionale, non come riferimento visivo**. Non copiare layout,
> classi o stile dal vecchio codice: si parte da zero.

## 0. Design read

**Reading this as:** console operativa (gestionale) per lo staff di un impianto
sportivo — reception, gestori, istruttori — con un linguaggio **funzionale,
legibile, a densità media**, che privilegia chiarezza e velocità d'uso quotidiano
sull'estetica. Non è una landing page, non è un portfolio, non è un sito
marketing.

> Nota: la skill `design-taste-frontend` è dichiarata fuori scope per
> dashboard/data-tables/product UI. Non usarla come guida visiva. Per un
> gestionale la scelta corretta è un design system coerente (Mantine, già in
> stack) usato in modo pulito e intenzionale, non un'estetica "tasteful".

**Dial di riferimento** (per orientare le scelte, non vincolanti):
- `DESIGN_VARIANCE: 4` — ordine e prevedibilità, non caos
- `MOTION_INTENSITY: 2` — transizioni minime, niente animazioni decorative
- `VISUAL_DENSITY: 5` — dati leggibili, non cockpit né art-gallery

## 1. Stack (non cambiare)

- React 18 + TypeScript + Vite
- **Mantine 7** (`@mantine/core`, `@mantine/hooks`, `@mantine/form`,
  `@mantine/colors-generator`) — già in `package.json`
- `@tabler/icons-react` per le icone
- `react-router-dom` v6
- Font: `@fontsource-variable/inter` (già installato)

Non aggiungere librerie di design alternative. Un solo sistema: Mantine.

## 2. Strato dati — NON toccare

Questi file sono il contratto con il backend e restano **inalterati**:

- `frontend/src/api.ts` — `bootstrap()`, tipi `AppConfig` / `BrandConfig` /
  `ModuleInfo`, `fetchJson`
- `frontend/src/auth.ts` — `AuthContext`, `useAuth()`, `useAuthProvider()`,
  `authHeaders()`
- `frontend/src/config.ts` — `AppConfigContext`, `useAppConfig()`
- `frontend/src/moduleIcons.ts` — `moduleIcon(name)` (mappa nome modulo → icona)

`main.tsx` monta `MantineProvider` + `BrowserRouter` e passa `config` ad `App`.
Il tema Mantine va **ricostruito da zero** in `main.tsx` (o in un nuovo
`theme.ts`): colore primario `brand` derivato da `config.brand.shades`
(già generato da `generateColors` in `api.ts`). Il vecchio `theme.ts` e
`tokens.css` sono stati eliminati: non riproporli, non importarli.

## 3. Routing e gate di auth (contratto da preservare)

`App.tsx` deve mantenere questa struttura (i nomi dei componenti di pagina sono
liberi, i path no):

- `/login` → se `auth.token` presente, redirect a `/`; altrimenti pagina login
- Route protette (richiedono `auth.token`, altrimenti redirect a `/login`),
  dentro una shell con sidebar + header:
  - `/` → Dashboard
  - `/modules/anagrafica` → Soci
  - `/modules/abbonamenti` → Abbonamenti
  - `/modules/:name` → pagina generica di modulo
  - `/users` → Utenti
  - `/settings` → Impostazioni
- `*` → redirect a `/`

## 4. Specifica funzionale per pagina

Ogni pagina: gestire **loading**, **errore** e **stato vuoto** in modo
esplicito. Tutte le chiamate API usano `authHeaders()` (tranne il login).

### 4.1 Login (`/login`)
- Form email + password con validazione (email valida, password non vuota).
- `login(email, password)` da `useAuth()`.
- Errore di credenziali mostrato in modo chiaro.
- Su successo: redirect a `/`.

### 4.2 Dashboard (`/`)
- Data odierna in italiano.
- Azioni rapide: "Nuovo socio" → `/modules/anagrafica`, "Nuova prenotazione" →
  `/modules/booking.fields`.
- Card "Prossime attività" e "Scadenze da attenzionare": per ora placeholder
  (nessun dato reale dal backend) — struttura pronta per essere popolata.
- Griglia "Aree di lavoro": una card per ogni modulo con `has_frontend === true`
  (da `useAppConfig().modules`), link a `/modules/<name>`, icona da
  `moduleIcon(name)`, label e nome tecnico.

### 4.3 Soci / Anagrafica (`/modules/anagrafica`)
- **Lista**: `GET /api/anagrafica/members` (opz. `?q=<search>`).
  Campi: `id, first_name, last_name, fiscal_code, email, phone, city, is_active`.
- **Ricerca** per nome/cognome/codice fiscale.
- **Nuovo socio** (modale): `POST /api/anagrafica/members` con
  `{ first_name, last_name, fiscal_code, email, phone, city }` (i campi
  opzionali vanno mandati come `null` se vuoti).
- Stato vuoto: "Nessun socio registrato".

### 4.4 Abbonamenti (`/modules/abbonamenti`)
- **Piani**: `GET /api/abbonamenti/plans`.
  Campi: `id, name, billing_type, price, duration_days, included_entries,
  is_active`.
- **Abbonamenti**: `GET /api/abbonamenti/subscriptions`.
  Campi: `id, member_id, plan (oggetto Plan), starts_on, ends_on, status`.
- Visualizzare piani (con prezzo formattato in €) e lista abbonamenti attivi.
- "Nuovo abbonamento": per ora **disabilitato** (funzionalità in sviluppo).

### 4.5 Utenti (`/users`)
- **Lista**: `GET /api/core/users`.
  Campi: `id, email, full_name, role, is_active`.
- **Nuovo utente** (modale): `POST /api/core/users` con
  `{ email, password, full_name, role }`.
- Ruoli disponibili: `admin, gestore, reception, istruttore, socio`.

### 4.6 Impostazioni (`/settings`)
- **Branding**: `GET /api/core/branding` per caricare, `PUT /api/core/branding`
  per salvare. Campi: `brand_name, brand_primary_color, public_domain`.
- **Brand pack**:
  - Esporta: `GET /api/core/branding/export` → download JSON `brand-pack.json`.
  - Importa: `POST /api/core/branding/import` con il JSON incollato.
- Feedback di successo/errore dopo salvataggio e import/export.

### 4.7 Modulo generico (`/modules/:name`)
- Cerca il modulo in `useAppConfig().modules` per `name`.
- Se non trovato/non attivo: messaggio di errore.
- Altrimenti: header con icona, label, versione, descrizione + placeholder
  "Modulo in sviluppo".

### 4.8 Shell (layout)
- Header: logo/monogramma brand (colore `config.brand.primaryColor`), nome
  brand, area utente (avatar + logout).
- Sidebar: Dashboard, i moduli con `has_frontend`, sezione "Sistema" con
  Impostazioni. Responsive (drawer su mobile).
- Logout: `logout()` da `useAuth()` → redirect a `/login`.

## 5. Vincoli anti-slop (obbligatori)

Non produrre i default LLM. In particolare **evita**:
- gradienti viola/indaco "AI", hero centrati su sfondo scuro con mesh
- glassmorphism ovunque, micro-animazioni a loop infinite
- tre card feature uguali in fila, Inter + slate-900 come estetica di default
- card dentro card dentro card

**Preferisci**:
- gerarchia tipografica chiara, spaziatura coerente, allineamenti a griglia
- stati vuoti, di caricamento e di errore curati (non "Caricamento…")
- tabelle per dati tabellari (utenti, abbonamenti), card solo dove ha senso
- un solo accento di colore (il brand), grigi neutri per il resto
- accessibilità: label sugli input, focus visibile, contrasto adeguato

## 6. Verifica

- `cd frontend && npm run build` deve passare (TypeScript + Vite).
- Ogni pagina deve compilare e gestire i tre stati (loading/errore/vuoto).
- Non modificare `api.ts`, `auth.ts`, `config.ts`, `moduleIcons.ts`.

## 7. Note di processo

- Il vecchio UI è in `master` se serve capire **cosa** faceva una pagina
  (endpoint, campi), ma **non** come riferimento di stile.
- A fine lavoro aggiornare `docs/` e `prompts/` con la data odierna secondo le
  regole di processo del progetto.
