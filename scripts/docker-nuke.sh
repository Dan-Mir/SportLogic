#!/usr/bin/env bash
set -Eeuo pipefail

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  printf '%s\n' "Errore: Docker Compose non è disponibile." >&2
  exit 1
fi

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
project_name="$(basename "$project_dir" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-')"
project_name="${project_name%-}"

printf '%s\n' "ATTENZIONE: questa operazione è DISTRUTTIVA."
printf '%s\n' "Verranno rimossi solo i container, le immagini, i volumi e la rete del progetto Compose: $project_name"
printf '%s\n' "Le risorse Docker di altri progetti non verranno toccate."
read -r -p "Scrivi DELETE per continuare: " confirmation

if [[ "$confirmation" != "DELETE" ]]; then
  printf '%s\n' "Operazione annullata."
  exit 0
fi

printf '%s\n' "Arresto e rimozione delle risorse SportLogic..."
docker compose --project-directory "$project_dir" --project-name "$project_name" down \
  --volumes --remove-orphans --rmi all

printf '%s\n' "Pulizia Docker di SportLogic completata."
