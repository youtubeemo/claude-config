# Claude Config – zentrale Projektregeln

Zentrale, versionskontrollierte Vorlagen für Claude Code in den Projekten von youtubeemo.

## Bereits konfigurierte Projekte

- gta-shorts-germany
- storyhouse-originals
- cartoon-story-universe
- dschungel-freunde
- gta-shorts-website

Die vorhandenen Projektkonfigurationen bleiben eigenständig. **Änderungen an diesem Repository werden nicht automatisch synchronisiert.** Für neue oder aktualisierte Regeln müssen die jeweiligen Projektdateien über geprüfte Pull Requests aktualisiert werden.

## Aufbau

- `templates/CLAUDE.md`: allgemeine Skill-Auswahl
- `templates/AGENTS.md`: Kosten- und Sicherheitsregeln
- `templates/settings.json`: gemeinsame Claude-Code-Plugin-Konfiguration
- `projects.md`: projektspezifische Ergänzungen und Plugin-Auswahl

## Einrichtung in neuen Projekten

1. Vorlagen prüfen und auf das Zielprojekt anpassen.
2. Nur benötigte Plugins aktivieren (Taste-Skill für UI, Lemo Opuscar für ausdrücklich gewünschte Stilfilme).
3. `CLAUDE.md`, `AGENTS.md` und `.claude/settings.json` über einen eigenen Branch und Pull Request einbringen.
4. Installation/Vertrauen in Claude Code bestätigen, falls abgefragt.
5. Keine kostenpflichtigen Produktionen oder Workflows auslösen.

## Grenzen

Diese Dateien sind Anweisungen an Claude Code, keine technische Garantie. Sie ersetzen keine Berechtigungs- oder Budgetkontrollen. Die Konfiguration enthält keine Secrets. Claude-Mem und FreeLLMAPI sind nicht aktiviert.

## Lizenzhinweis

Lemo Opuscar: Code und begleitende Inhalte können unterschiedliche Lizenzen haben. Nicht-kommerzielle Texte/Prompts nicht unverändert für monetarisierte Produktionen übernehmen.
