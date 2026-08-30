# HKF Plugin

Anforderungen an das Plugin, das eine Wissensbasis nach **HKF Core 1.0**
bedienbar macht — Anlegen, Importieren, Exportieren, Linten, Abfragen. Was
hier steht, ist kein Entwurf der Skills selbst, sondern die drei Festlegungen,
die vor ihnen kommen: wo die Ablage liegt, wie sie synchronisiert wird und
warum sie ein Repository ist.

Vorbild für die erste Festlegung ist der Skill
[`llm-wiki`](file:///Users/arminpfarr/.hermes/skills/research/llm-wiki/SKILL.md).

## 1. Die Ablage wird über eine Umgebungsvariable gefunden

`llm-wiki` macht das vorbildlich: der Skill nennt keinen Pfad, er nennt eine
Variable.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

Damit ist die Ablage vom Harness getrennt. Der Skill wird einmal installiert
und liegt beim Werkzeug; die Wissensbasis liegt, wo der Mensch sie haben will
— auf einem externen Volume, in einer Cloud, in einem geklonten Repository.
Keine der beiden Seiten weiß etwas über den Ort der anderen.

**Das HKF-Plugin macht es genauso.**

```bash
HKB="${HKB_PATH:-$HOME/hkb}"
```

| | |
|---|---|
| Variable | `HKB_PATH` |
| Vorgabe | `~/hkb`, wenn nicht gesetzt |
| Ort der Definition | `~/.claude/settings.json` unter `env`, oder eine `.env` der Werkzeugumgebung |
| Prüfung | Der Skill liest `$HKB/hkb.md` und prüft die Property `hkf`. Fehlt die Datei, ist der Pfad keine Ablage — abbrechen und den Menschen fragen, nicht raten. |

Drei Regeln dazu:

- **Kein Skill schreibt einen Pfad fest.** Nicht in Beispielen, nicht in
  Werkzeugaufrufen, nicht in einer Prüfroutine.
- **Das Arbeitsverzeichnis ist nicht die Ablage.** Ein Agent kann in einem
  Coderepository stehen und trotzdem in die Wissensbasis schreiben. Wer
  `.` annimmt, schreibt irgendwann Notizen in ein fremdes Verzeichnis.
- **Mehrere Wissensbasen sind der Normalfall.** `HKB_PATH` nennt die
  vorgegebene; ein ausdrücklich genannter Pfad im Auftrag sticht sie. Die
  Reihenfolge ist: Auftrag → `HKB_PATH` → Vorgabe.

Für die Ablage der Bundles gilt dasselbe, sobald es sie gibt: `HKF_BUNDLE_PATH`
für das Verzeichnis, in dem `hk-export` ablegt und `hk-import` sucht.

## 2. Synchronisiert wird mit obsidian-headless

Eine Wissensbasis ist zugleich ein Obsidian-Vault. Auf einer Maschine ohne
Bildschirm — Server, Cron-Lauf, Agent im Hintergrund — gibt es keine
Obsidian-App, die den Vault abgleicht. `obsidian-headless` erledigt das über
Obsidian Sync ohne Oberfläche.

```bash
# Node.js 22+
npm install -g obsidian-headless

ob login --email <adresse> --password '<passwort>'
ob sync-create-remote --name "Meine Wissensbasis"

cd "$HKB_PATH"
ob sync-setup --vault "<vault-id>"
ob sync
```

Dauerhaft im Hintergrund über einen Dienst (`ob sync --continuous`, unter
systemd mit `WorkingDirectory` auf `$HKB_PATH`, unter macOS als LaunchAgent).

Was das bringt: Der Agent schreibt in die Ablage, während dieselbe Ablage auf
Laptop und Telefon in Obsidian offen ist. Die Änderungen stehen in Sekunden
auf allen Geräten. Das Plugin braucht dafür keine eigene Synchronisation und
keinen eigenen Konfliktbegriff.

Zwei Punkte, die das Plugin regeln muss:

- **Obsidian Sync und Git laufen nebeneinander**, nicht gegeneinander. Sync
  hält die Geräte gleich, Git hält die Geschichte. `.git/` gehört nicht in den
  Sync — bei `ob sync-setup` ausschließen.
- **Vor einem größeren Schreibvorgang einmal `ob sync`**, danach noch einmal.
  Sonst arbeitet der Agent auf einem veralteten Stand und erzeugt Konflikte,
  die niemand gesehen hat.

## 3. Jede Wissensbasis ist ein Git-Repository

Eine Wissensbasis ohne Geschichte ist ein Verzeichnis, in dem ein Sprachmodell
ohne Zeugen arbeitet. Also: **`hk-init` legt nicht nur die Grundausstattung an,
sondern auch das Repository.**

1. `git init`
2. `.gitignore` schreiben (siehe unten)
3. Alles hinzufügen, ein erster Commit: `hkb: Grundausstattung`

`tools/make-hkb-template.py` schreibt die `.gitignore` heute schon, ruft aber
kein `git init` auf. Das ist die Lücke, die das Plugin schließt.

Die `.gitignore` — der Stand aus `HenniHKF-Core`, der sich bewährt hat:

```gitignore
# Sitzungsprotokolle und Suchindex der Werkzeugumgebung
.memsearch/

# persönliches Fensterlayout von Obsidian
.obsidian/workspace.json

# macOS
.DS_Store
```

Warum gerade diese drei:

| Eintrag | Grund |
|---|---|
| `.memsearch/` | gehört dem Harness, nicht der Ablage — genau die Trennung aus §1, hier auf der Ebene der Versionierung |
| `.obsidian/workspace.json` | persönliches Fensterlayout, ändert sich bei jedem Öffnen und gehört keinem zweiten Gerät |
| `.DS_Store` | Rauschen |

Der Rest von `.obsidian/` **bleibt versioniert**: Wikilinks, vollständige
Pfade, die registrierten Property-Typen. Das ist Teil des Formats, nicht
Geschmack — eine Wissensbasis, die diese Konfiguration verliert, zeigt Daten
und Listen falsch an.

Was daraus für die Skills folgt:

- **Commit nach jedem abgeschlossenen Vorgang**, nicht nach jeder Datei. Ein
  Import ist ein Commit, ein Lint-Lauf mit Korrekturen ist ein Commit.
- **Nie `git add -A` blind.** Es gilt der Skill `git-vault-safety`: erst
  `git status` lesen, dann gezielt hinzufügen.
- **Kein Push ohne Auftrag.** Die Geschichte ist lokal wertvoll; wohin sie
  veröffentlicht wird, entscheidet der Mensch.

## Offen

- Name und Vorgabe der Bundle-Variablen (`HKF_BUNDLE_PATH`) — erst festlegen,
  wenn `hk-export` steht.
- Ob `hk-init` das Repository selbst anlegt oder ein bestehendes akzeptiert,
  wenn das Zielverzeichnis schon eins ist.
- Verhältnis zu `hkf-kb-template`: Wer über „Use this template" startet,
  bekommt das Repository geschenkt und braucht Schritt 3 nicht.
