# Sichere Synchronisierung

Die Automatik erzeugt **nur Pull Requests** in fünf Ziel-Repositories. Sie führt keine Builds, Renderer, Uploads oder kostenpflichtigen APIs aus und mergt nichts.

## Einmalige Einrichtung

1. Erzeuge einen **Fine-grained personal access token** in GitHub mit Repository-Zugriff **nur** auf die fünf Ziel-Repositories. Benötigte Rechte: **Contents: Read and write** und **Pull requests: Read and write**; Metadata: Read ist implizit. Verwende ein Ablaufdatum und bewahre den Token geheim auf.
2. Im privaten Repository `youtubeemo/claude-config`: **Settings → Secrets and variables → Actions → New repository secret**. Name: `SYNC_TOKEN`, Wert: der Token.
3. Öffne **Actions → Propose Claude configuration updates → Run workflow**. Der manuelle Start ist standardmäßig ein Dry Run. Danach kann ein Lauf mit `dry_run=false` Pull Requests erstellen.
4. Änderungen an `managed/` auf `main` starten später automatisch die PR-Vorbereitung. **Nichts wird automatisch gemergt.**

## Was wird synchronisiert?

Nur die markierten Bereiche in `CLAUDE.md` und `AGENTS.md`. Projektspezifische Zeilen außerhalb der Marker bleiben erhalten. `.claude/settings.json` bleibt unberührt, damit sich Plugins je nach Projekt unterscheiden können.

## Sicherheit

- Niemals Tokens in Dateien, Chatnachrichten oder Logs einfügen.
- Bei bereits bestehendem Sync-Branch stoppt das Skript für dieses Repo, statt einen offenen PR zu überschreiben.
- Ohne `SYNC_TOKEN` werden keine Änderungen vorgenommen.
- Wenn ein Ziel-Repo nicht zugreifbar ist oder Marker fehlen, meldet der Job einen Fehler statt Dateien zu ersetzen.
- Der Token ist ein zusätzlicher Zugang zu den fünf Repositories. Bei Bedarf unter GitHub-Einstellungen widerrufen.
