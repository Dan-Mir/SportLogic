# Prossima sessione — 2026-10-07

Il frontend SportLogic e' stato rigenerato da zero e la build e' verde.

## Stato attuale

- `frontend/src/App.tsx` contiene shell, routing, pagine e componenti locali.
- `frontend/src/app.css` contiene soltanto gli stili strutturali della console.
- `frontend/src/main.tsx` definisce il nuovo tema Mantine usando `brand` dal
  bootstrap.
- I contratti `api.ts`, `auth.ts`, `config.ts` e `moduleIcons.ts` non sono
  stati modificati.

## Funzionalita' disponibili

- Login con validazione e feedback credenziali.
- Dashboard, soci, abbonamenti, utenti, impostazioni e route dei moduli.
- Creazione soci e utenti, ricerca soci, branding, import/export brand pack.
- Stati loading, errore e vuoto per le pagine che caricano dati.

## Verifica eseguita

```bash
cd frontend && npm run build
```

La build TypeScript e Vite passa.

## Passi utili successivi

1. Eseguire una verifica manuale contro un backend avviato con utenti aventi
   ruoli differenti, in particolare per i permessi di branding e utenti.
2. Collegare le pagine placeholder della dashboard alle API quando calendario e
   alert scadenze saranno disponibili.
3. Quando saranno esposti endpoint di creazione, abilitare il flusso `Nuovo
   abbonamento`.
