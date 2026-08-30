# HKF Plugin

Anforderungen an das Plugin, das eine Wissensbasis nach **HKF Core 1.0**
bedienbar macht — Anlegen, Importieren, Exportieren, Linten, Abfragen. Was
hier steht, ist kein Entwurf der Skills selbst, sondern die vier Festlegungen,
die vor ihnen kommen: wo die Ablage liegt, wie sie synchronisiert wird, warum
sie ein Repository ist und wer die Kurationspolitik führt.

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

## 4. Die Kurationspolitik hat zwei Orte

Anlass ist Ken Moriwakis Aufbau eines minimalen LLM-Wikis
([Medium, 24. Mai 2026](https://medium.com/@ken.moriwaki/building-a-minimal-llm-wiki-19a2fb0e9ac7)).
Dort führt die Ablage eine `schema.md` — die Datei, die das Modell liest,
bevor es schreibt. Sie erfüllt vier Aufgaben auf einmal:

| Was in `schema.md` steht | Wo es in HKF steht |
|---|---|
| Gegenstand der Wissensbasis | `name` in `hkb.md` |
| „Concept pages live in `wiki/concepts/`" | der Abschnitt `# Typen` in `hkb.md`, normativ die `typedefs/` |
| der Frontmatter-Block, die Tag-Taxonomie | Property-Tabelle des Typs, `proptypes/`, Anhang B.4 |
| Konventionen für Verweise und Zeitangaben | die Regeln in `AGENTS.md`, abgeleitet nach Core §5.4 |
| **wann eine Notiz entsteht, was bei Widerspruch geschieht** | **nirgends** |

Die ersten vier Zeilen sind in HKF besser gelöst, und zwar aus einem Grund:
Sie stehen als Tabellen da, nicht als Fließtext, also prüft `hk-lint` sie.
Moriwakis Prototyp muss dafür ein Modell ein Audit schreiben lassen — und der
Artikel hält selbst fest, dass dieses Audit Widersprüche übersehen,
übertreiben oder erfinden kann. Ein Vertrag in Prosa lässt sich nur erinnern,
einer in Tabellen prüfen.

Die letzte Zeile ist die Lücke. Core nennt sie nicht, und das ist richtig:
Core ist ein Format, keine Arbeitsanweisung. Irgendwo muss sie trotzdem
stehen, sonst entscheidet sie jedes Modell bei jedem Lauf neu.

### Warum das nicht bloß Stil ist

Moriwaki nennt das Risiko **over-synthesis**, und er hält es für gefährlicher
als Halluzination: Ein Modell macht aus Uneinigkeit einen Konsens, aus
Unsicherheit eine klare Zusammenfassung. Gefährlich ist das, weil eine
saubere Notiz mit Überschriften und Belegabschnitt Autorität ausstrahlt, die
ihr Inhalt nicht deckt. Dann ist die Wissensbasis schlechter als der Stapel
Quellen, aus dem sie entstand.

Dagegen hilft keine Formatregel, sondern eine Politik: Widersprechen sich zwei
Quellen, steht das in der Notiz. Ist eine Aussage unsicher, wird sie als
unsicher gekennzeichnet.

### Der Schnitt

Dieselbe Linie wie bei `HKB_PATH` in §1, eine Ebene höher: Was der Ablage
gehört, reist mit der Ablage; was dem Werkzeug gehört, reist mit dem Werkzeug.

| | |
|---|---|
| **`AGENTS.md`, Abschnitt `# Hinweise`** | Was **diese** Wissensbasis angeht: ihr Gegenstand, ab wann etwas eine eigene Notiz wert ist, welche Typen hier bevorzugt werden, welche Quellen als belastbar gelten. Der Abschnitt ist nach Core §5.4 genau dafür da — er überlebt `hk-lint --fix`, während der Rest der Datei neu erzeugt wird. |
| **Die Skills des Plugins** | Was den Umgang mit **jeder** HKB angeht: der Ablauf eines Ingests, wann committet wird, wann das Modell rückfragt statt zu entscheiden, das Verbot der glatten Zusammenfassung. |

Drei Regeln dazu:

- **Kein Skill schreibt Politik in die Spezifikation zurück.** Was hier
  festgelegt wird, ist Gebrauch, nicht Format.
- **`typedefs/` und `proptypes/` bleiben tabu**, auch für die Politik. Es gilt
  Regel 6 aus `AGENTS.md`. Wer eine Aussage über Belastbarkeit
  maschinenlesbar braucht, legt einen eigenen Typ oder Property-Typ daneben —
  nicht in die Grundausstattung.
- **In `# Hinweise` schreibt das Plugin nur auf Auftrag.** Der Abschnitt
  gehört dem Menschen; ein Modell, das sich dort selbst Regeln gibt, hat sie
  am nächsten Tag vergessen oder verschärft.

### Was keine eigene Datei bekommt

Moriwakis Prototyp führt daneben `log.md` und `audit.md`. Beides braucht eine
HKB nicht: Die Geschichte steht in Git (§3), der Befund kommt aus `hk-lint`.
Core §5.8 sieht nur auf den ersten Blick nach einem Protokoll aus — dort
werden Importurteile festgehalten, damit dieselbe Rückfrage nicht wiederkehrt,
nicht Änderungen mitgeschrieben.

## Offen

- Name und Vorgabe der Bundle-Variablen (`HKF_BUNDLE_PATH`) — erst festlegen,
  wenn `hk-export` steht.
- Ob `hk-init` das Repository selbst anlegt oder ein bestehendes akzeptiert,
  wenn das Zielverzeichnis schon eins ist.
- Verhältnis zu `hkf-kb-template`: Wer über „Use this template" startet,
  bekommt das Repository geschenkt und braucht Schritt 3 nicht.
- Ob die Kurationspolitik eines Tages eine eigene Notiz verdient — ein Typ
  `policy` in der Ablage statt Prosa in `# Hinweise`. Erst entscheiden, wenn
  eine Wissensbasis so groß ist, dass die Hinweise unübersichtlich werden.
