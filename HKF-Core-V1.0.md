---
type: specification
title: HKF Core V1.0 — Henni Knowledge Format
description: Der Kern des Formats — typbezogene Ablage, Wertformen, Property-Typen, qualifizierte Wikilinks, Bundle-Format und Methoden. Ohne Vokabular.
status: draft
---

# HKF Core V1.0

Diese Spezifikation beschreibt zwei Dinge:

- **HKF** — das **Bundle-Format**: eine übertragbare, für sich lesbare
  Sammlung von Notizen samt ihrer Typdefinitionen.
- **HKB** — die **Henni Knowledge Base**: ein Obsidian-Vault, der beliebig
  viele HKF-Bundles importieren und wieder exportieren kann.

Beide teilen denselben Kern: typbezogene Ablage, native Obsidian-Properties,
qualifizierte Wikilinks. Sie unterscheiden sich nur in ihrer Wurzeldatei und
darin, was sie zusätzlich dürfen.

HKF ist kein Ontologiesystem. Ein Typ ist ein Verzeichnis mit einer
Beschreibung. Mehr nicht.

## Core und Base

Das Format ist auf zwei Dokumente verteilt, weil es zwei Fragen beantwortet:

- **HKF Core** — dieses Dokument. Wie eine Ablage aufgebaut ist: Verzeichnisse,
  Wertformen, Property-Typen, Verweise, Typdefinitionen, das Bundle-Format und
  die drei Methoden. Es nennt **keinen einzigen inhaltlichen Typ**.
- **HKF Base** — das Vokabular: neun Typdefinitionen für Person, Körperschaft,
  Ort, Ereignis, Quelle, Begriff, Thema, Notiz und Spezifikation, dazu zwei
  Property-Typen. Es wird als Bundle geliefert und ist freiwillig.

Konform ist eine Wissensbasis nach **Core**. Wer nur Core erfüllt, hat eine
leere, aber vollständige Ablage und definiert seine Typen selbst. Wer Base
lädt, verpflichtet sich zusätzlich auf die dort festgelegte Bedeutung dieser
neun Typen — der Preis dafür, dass Bundles zwischen fremden Wissensbasen
austauschbar sind.

Der Schnitt liegt dort, wo die Beliebigkeit anfängt. Dass eine Notiz in dem
Verzeichnis ihres Typs liegt, gilt für jede Wissensbasis. Dass eine Person
`born` und `died` trägt, ist eine Verabredung, die man auch anders treffen
kann.

---

# 1. Kurzfassung (der einzige Abschnitt, den ein Werkzeug lesen muss)

```text
HKB — Knowledge Base              HKF — Bundle
──────────────────────────────    ──────────────────────────────
hkb.md                            hbundle.md
<base>/typedefs/<typ>.md          typedefs/<typ>.md
<base>/proptypes/<prop-typ>.md    proptypes/<prop-typ>.md
<base>/bundles/<id>.md            —
<base>/<verzeichnis>/…            <verzeichnis>/…
<media_base>/images/…             media/images/…
<media_base>/videos/…             media/videos/…
<media_base>/audios/…             media/audios/…
<media_base>/documents/…          media/documents/…
```

Beide Bäume beginnen im Verzeichnis ihrer Wurzeldatei — dem Wurzelverzeichnis
der Ablage. Es muss nicht die Wurzel des Vaults sein.

1. **Lies die Wurzeldatei** — `hkb.md` oder `hbundle.md`. Sie enthält den
   Basispfad und eine Tabelle aller Typen mit Verzeichnis und Zweck. Danach
   ist die gesamte Ablage bekannt.
2. **Brauchst du einen Typ genauer, lies genau eine Datei:**
   `<base>/typedefs/<typ>.md`. Ihre Property-Tabelle ist der vollständige
   Vertrag des Typs.
3. **Jede Notiz hat genau eine Pflicht-Property:** `type`.
4. **Jeder interne Verweis ist ein qualifizierter Wikilink:**
   `[[<pfad-ohne-.md>]]`, optional mit `|Anzeigetext`.
5. **Drei Methoden der HKB:** `hk-import`, `hk-export`, `hk-lint`.
6. **Dieses Dokument nennt keine inhaltlichen Typen.** Welche Typen eine
   Ablage führt, steht in der Typtabelle ihrer Wurzeldatei. Ein verbreitetes
   Vokabular liefert **HKF Base**.
7. **Grundausstattung und Zuladung.** Die zwölf Property-Typen und die drei
   Kern-Typen entstehen mit der Wissensbasis — ohne sie ließe sich nichts
   importieren. Alles Weitere kommt als Bundle dazu und ist freiwillig (§5.3).
8. **Ein unbekannter Typ hält einen Import nicht auf.** Eine Notiz mit einem
   Typ, den die Wissensbasis nicht kennt, wird übernommen; für ihn entsteht
   eine vorläufige Typdefinition (§5.5). Führt die Wissensbasis den Namen
   dagegen bereits, muss vor der Übernahme entschieden werden, ob beide
   dasselbe meinen (§5.6).
9. **Der Import verknüpft die Lieferung mit dem Bestand.** Was ankommt, wird
   in einem Abschnitt `# Siehe auch` mit dem verbunden, was schon da ist, in
   beide Richtungen und mit einem Grund je Verweis (§5.7).

Mehr Kontext ist für das Lesen und Schreiben nicht nötig.

---

# 2. Begriffe

| Begriff | Bedeutung |
|---|---|
| **HKF-Bundle** | Übertragbare Sammlung von Notizen mit `hbundle.md` in der Wurzel. |
| **HKB** | Knowledge Base: Vault mit `hkb.md` in der Wurzel. |
| **Ablage** | Sammelbegriff für beides: ein Baum nach den Regeln von §3. |
| **Notiz** | Markdown-Datei mit YAML-Frontmatter und Body. |
| **Typ** | Name einer Notizart, registriert durch eine Typdefinition. |
| **Typdefinition** | Notiz mit `type: typedef` in `typedefs/`. |
| **Wertform** | Einer der sechs nativen Obsidian-Property-Typen. |
| **Property-Typ** | Notiz mit `type: proptype` in `proptypes/`; schränkt eine Wertform ein. |
| **Bundle-Notiz** | Notiz mit `type: bundle`; die Wurzeldatei eines Bundles. |
| **Notiz-ID** | Pfad der Notiz relativ zum Basispfad, ohne `.md`. |
| **Vorläufige Typdefinition** | Beim Import erzeugte Typdefinition für einen Typ, den niemand mitgeliefert hat; trägt `provisional: true` (§5.5). |
| **Bedeutungsprüfung** | Entscheidung, ob zwei gleichnamige Typen dasselbe meinen (§5.6). |
| **Siehe auch** | Maschinell gepflegter Abschnitt am Ende einer Notiz; hält Verweise mit ihrem Grund (§5.7). |

---

# 3. Gemeinsamer Kern

Dieses Kapitel gilt unverändert für HKF-Bundles und für HKBs.

## 3.1 Wurzeldatei und Basispfad

Jede Ablage hat genau eine Wurzeldatei in ihrem Wurzelverzeichnis: `hkb.md`
bei einer HKB, `hbundle.md` bei einem Bundle. Sie ist keine Notiz im Sinne von
§3.3 und liegt in keinem Typverzeichnis.

Ihr Frontmatter trägt mindestens:

```yaml
hkf: "1.0"
base: ""
media_base: media
```

`base` ist der Basispfad für die Typverzeichnisse, relativ zur Wurzel, ohne
führenden und ohne abschließenden `/`. Optional; Vorgabe ist der leere Wert,
also die Wurzel. In einem Bundle ist `base` immer leer.

Eine Ablage muss nicht das ganze Vault sein. Ihr Wurzelverzeichnis ist
schlicht das Verzeichnis, in dem ihre Wurzeldatei liegt. Bei einer HKB heißt
der Pfad dorthin, von der Vault-Wurzel aus gerechnet, **Ablagepfad**; er ist
leer, wenn die HKB in der Vault-Wurzel liegt, und er steht in jedem Wikilink
vor der Notiz-ID (§3.6).

**Ein Bundle hat keinen Ablagepfad.** Es wird ausgeliefert und landet beim
Empfänger an beliebiger Stelle; seine Verweise sind deshalb immer auf die
Bundle-Wurzel bezogen und tragen nie einen Präfix. Liegt ein Bundle innerhalb
eines Vaults, kann Obsidian seine Verweise darum nicht richtig auflösen — im
Zweifel zeigt `[[persons/ada-lovelace]]` dort auf die gleichnamige Notiz der
Wissensbasis. Das ist der Preis dafür, dass ein Bundle überall auspackbar
bleibt, und es ist der richtige Tausch: Ein Bundle ist eine Lieferung, kein
Arbeitsbereich.

`media_base` ist der Basispfad für die Medienverzeichnisse (§3.2.1), ebenfalls
relativ zur Wurzel und ohne führenden und abschließenden `/`. Optional;
Vorgabe ist der leere Wert, also ebenfalls die Wurzel. Anders als `base` darf
`media_base` auch in einem Bundle gesetzt sein — Quelle und Ziel eines
Imports dürfen verschiedene Medienpfade haben (§6.1).

Ihr Body enthält den Abschnitt `# Typen`:

```markdown
# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| typedef | typedefs | Registriert einen Typ. |
| proptype | proptypes | Schränkt eine Wertform ein. |
| bundle | bundles | Beschreibt eine Lieferung. |
| person | persons | Ein Mensch. |
```

Die Tabelle ist **abgeleitet**: Sie fasst alle Typdefinitionen der Ablage
zusammen und wird von `hk-lint --fix` neu erzeugt. Sie existiert allein
deshalb, damit ein Werkzeug die gesamte Ablage aus einer einzigen Datei
kennt. Bei Abweichung gewinnen immer die Typdefinitionen.

## 3.2 Typbezogene Ablage

Alle Notizen liegen typbezogen unter dem Basispfad:

```text
<base>/<verzeichnis des typs>/<dateiname>.md
```

Unterverzeichnisse innerhalb eines Typverzeichnisses sind erlaubt.

Im Basispfad existieren **immer** die Verzeichnisse `typedefs`, `proptypes`
und `bundles`. Dort liegen die Typdefinitionen, die Property-Typen und die
Bundle-Notizen. In einem Bundle bleibt `bundles/` leer oder entfällt, weil
die Bundle-Notiz dort in der Wurzel liegt (§4).

Ein Pflichtverzeichnis, das leer bliebe, darf entfallen. Git kann leere
Verzeichnisse nicht abbilden, und ein über Git verteiltes Bundle verlöre sie
still. Ein Werkzeug legt ein fehlendes Verzeichnis an, sobald es etwas
hineinschreibt, und meldet sein Fehlen nicht.

**Zur Ablage gehört**, was unter ihrem Wurzelverzeichnis liegt: die
Wurzeldatei, die Typverzeichnisse unter `base` und die Medienverzeichnisse
unter `media_base`. Alles andere im Vault ist außerhalb von HKF und wird
weder geprüft noch verwaltet — eine Spezifikation, ein README, Notizen, die
zu keiner Wissensbasis gehören.

Eine Ablage darf **keine zweite Ablage enthalten**. Ein Werkzeug erkennt eine
Ablage an ihrer Wurzeldatei; läge unter einer weitere, wäre für jede Notiz
darin unklar, zu welcher sie gehört. Mehrere Ablagen nebeneinander in einem
Vault sind dagegen zulässig und der Normalfall, sobald Bundles in
Unterverzeichnissen liegen.

Die Wurzeldatei eines Bundles heißt `hbundle.md` und nicht `bundle.md` — der
kürzere Name gehört bereits der Typdefinition des Kern-Typs `bundle`, die als
`typedefs/bundle.md` in jeder Ablage liegt. Ein Werkzeug, das nach
Wurzeldateien sucht, hielte sonst jede Ablage mit registriertem `bundle`-Typ
für verschachtelt.

Zusätzlich erkennt man eine Wurzeldatei an der Property `hkf`, die keine Notiz
trägt. Der Name allein sollte genügen; die Prüfung auf `hkf` macht die
Erkennung unabhängig davon, ob jemand eine Notiz `hbundle` nennt.

**Regeln**

1. Der Pfad bestimmt den Typ. Eine Notiz gehört zu dem Typ, unter dessen
   Verzeichnis sie liegt. `type` im Frontmatter MUSS damit übereinstimmen.
2. Verzeichnisnamen der Typen sind eindeutig; keines darf unter einem anderen
   liegen.
3. Dateinamen sind `kebab-case` und innerhalb ihres Typverzeichnisses
   eindeutig. Derselbe Name darf in verschiedenen Typverzeichnissen
   vorkommen.
4. Die **Notiz-ID** ist der Pfad ab dem Basispfad ohne `.md`, etwa
   `persons/ada-lovelace`. Sie ist die Identität der Notiz.
5. Umbenennen oder Verschieben ändert die Identität. Ein Werkzeug MUSS
   dabei alle Verweise mitziehen.

### 3.2.1 Medienverzeichnisse

Mediendateien sind keine Notizen: Bilder, Videos, Tonaufnahmen und Dokumente.
Sie liegen nicht in den Typverzeichnissen, sondern unter `media_base` in genau
vier Verzeichnissen:

```text
<media_base>/images/
<media_base>/videos/
<media_base>/audios/
<media_base>/documents/
```

| Verzeichnis | Medienart | Inhalt |
|---|---|---|
| `images` | `image` | Bilder, Grafiken |
| `videos` | `video` | Bewegtbild |
| `audios` | `audio` | Tonaufnahmen |
| `documents` | `document` | PDFs und andere Dokumente |

- Diese vier Namen sind unter `media_base` reserviert. Unmittelbar unter
  `media_base` darf **kein** anderes Verzeichnis liegen.
- Innerhalb der vier Verzeichnisse ist jede Unterstruktur erlaubt, etwa
  `images/persons/portraets/`.
- Ein Verzeichnis wird angelegt, sobald Medien seiner Art vorkommen.
- Kein Typverzeichnis darf unter `media_base` liegen und keines der vier
  Medienverzeichnisse darf als `dir` einer Typdefinition beansprucht werden.
- Die Medienart ergibt sich allein aus dem Verzeichnis, nicht aus der
  Dateiendung.

## 3.3 Notizen

Jede Notiz beginnt mit YAML-Frontmatter. Pflicht ist genau eine Property:

```yaml
type: person
```

Alles Weitere ist optional und frei. Empfohlen, aber nicht gefordert:
`title`, `description`, `tags`, `status`, `created`, `updated`. Ohne `title`
gilt der Dateiname als Titel.

Dass `type` die einzige Pflicht ist, ist keine Sparsamkeit, sondern die
Bedingung dafür, dass eine Notiz überall ankommt: Eine Wissensbasis kann sie
übernehmen, auch wenn sie ihren Typ nicht kennt — sie legt ihn dann vorläufig
an (§5.5).

Drei Properties führen die Geschichte einer Notiz: `created`, `modified` und
`modified_by` (Anhang A.2). In einem Bundle sind sie freigestellt, in einer
HKB werden sie geführt. **Wer eine Notiz maschinell ändert, MUSS `modified`
und `modified_by` setzen** — ein Sprachmodell trägt dort seinen Modellnamen
ein. Ohne das lässt sich beim Import nicht entscheiden, welche Fassung die
jüngere ist (§6.1).

Der Body ist gewöhnliches Markdown. HKF leitet aus dem Body nichts ab,
ausgenommen die vier ausdrücklich normativen Strukturen: `# Typen` (§3.1),
`# Properties` (§3.7), `# Siehe auch` (§5.7) und den Importnachweis einer
Bundle-Notiz (§5.1). Werkzeuge MÜSSEN unbekannte Properties unverändert
erhalten.

## 3.4 Wertformen

Es werden ausschließlich die nativen Obsidian-Property-Typen verwendet:

| Obsidian-Typ | Wertform | Beispiel |
|---|---|---|
| Text | `text` | `type: person` |
| Liste | `list` | `tags: [mathematik, geschichte]` |
| Zahl | `number` | `capacity: 120` |
| Checkbox | `checkbox` | `cancelled: false` |
| Datum | `date` | `born: 1815-12-10` |
| Datum & Uhrzeit | `datetime` | `starts_at: 2026-10-14T18:15:00` |

Verschachtelte Abbildungen und Listen von Abbildungen sind **nicht** zulässig.
Strukturierte Information gehört als Liste oder Tabelle in den Body.

Weitere Regeln:

- Property-Namen sind `snake_case`.
- Leere Werte und `null` werden nicht geschrieben; eine unbekannte Property
  entfällt.
- Ein `datetime`-Wert ohne Uhrzeit bezeichnet den Tagesbeginn: `2026-08-27`
steht für `2026-08-27T00:00:00`. `hk-lint --fix` schreibt ihn aus, damit
Vergleiche nicht von der Schreibweise abhängen.

Zeiten stehen als Ortszeit ohne Versatz im Muster `JJJJ-MM-TTTHH:mm:ss`.
  Die Zone nennt die Wurzeldatei über die optionale Property `timezone`
  (IANA-Zonenname); ohne Angabe gilt die Systemzone.

## 3.5 Property-Typen

Ein Property-Typ schränkt eine Wertform ein — etwa auf eine URL, eine
geographische Breite oder einen Wikilink. Er ist eine Notiz in `proptypes/`;
der **Dateiname ist der Name des Property-Typs**.

Ein Property-Typ ist ein *Werttyp*, kein Property-Name. Welche Property eines
Konzepttyps welchen Property-Typ hat, sagt die Property-Tabelle der
Typdefinition (§3.7).

```markdown
---
type: proptype
form: text
pattern: "^https?://\\S+$"
---

Absolute HTTP- oder HTTPS-Adresse.
```

- `form` ist Pflicht und nennt eine der sechs Wertformen aus §3.4.
- Optional: `pattern` (regulärer Ausdruck; bei `form: list` je Eintrag),
  `values` (Liste erlaubter Werte), `unit`, `min`, `max`.
- Namen sind `kebab-case`. Das Präfix `hkf-` ist den Property-Typen dieser
  Spezifikation vorbehalten — gleich ob sie zur Grundausstattung gehören
  (§3.5.1) oder mit einem Bundle wie HKF Base kommen.

Für die sechs Wertformen selbst wird **kein** Property-Typ angelegt. Ebenso
wenig für Obsidian-eigene Properties wie `tags`, `aliases` und `cssclasses`.

### 3.5.1 Standard-Property-Typen

Diese zwölf Property-Typen kennt jede HKB. Sie sind Teil dieser
Spezifikation und gehören zur **Grundausstattung**: Eine HKB legt sie beim
Anlegen als Notizen in `proptypes/` an (§5.3).

| Property-Typ | Wertform | Einschränkung |
|---|---|---|
| `hkf-url` | `text` | `pattern: "^https?://\\S+$"` |
| `hkf-email` | `text` | `pattern: "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"` |
| `hkf-phone` | `text` | `pattern: "^\\+[1-9]\\d{6,14}$"` — E.164, also `+4993131885` |
| `hkf-lang` | `text` | `pattern: "^[a-z]{2}$"` — ISO 639-1, also `de`, `en` |
| `hkf-country` | `text` | `pattern: "^[A-Z]{2}$"` — ISO 3166-1 alpha-2, also `DE`, `GB` |
| `hkf-latitude` | `number` | `min: -90`, `max: 90`, `unit: Grad` |
| `hkf-longitude` | `number` | `min: -180`, `max: 180`, `unit: Grad` |
| `hkf-year` | `number` | `min: -4000`, `max: 9999` |
| `hkf-wikidata` | `text` | `pattern: "^Q[1-9]\\d*$"` — Wikidata-Kennung, etwa `Q7259` |
| `hkf-file` | `text` | Wikilink auf eine Mediendatei, **mit** Dateiendung |
| `hkf-link` | `text` | genau ein qualifizierter Wikilink nach §3.6 |
| `hkf-link-list` | `list` | jeder Eintrag ein qualifizierter Wikilink nach §3.6 |

`hkf-year` trägt eine Jahreszahl, wenn kein vollständiges Datum bekannt ist.
Negative Werte bezeichnen Jahre vor der Zeitenwende. Ein bekanntes Datum
gehört als `date` ins Frontmatter, nicht als Jahr.

`hkf-wikidata` verankert eine Notiz an einem Gegenstand der realen Welt.
Anders als alle übrigen Property-Typen beschreibt er nicht die Notiz, sondern
das, worüber sie handelt: `Q7259` bezeichnet Ada Lovelace, gleich wie die
Notiz heißt und in welcher Wissensbasis sie liegt. Damit lässt sich erkennen,
dass zwei Notizen aus verschiedenen Lieferungen dasselbe meinen — was die
pfadbasierte Identität aus §3.2 nicht leisten kann.

Er ist der einzige standardisierte Normdaten-Bezug, weil Wikidata als
einziges Verzeichnis Personen, Körperschaften, Orte, Werke und Begriffe
gleichermaßen abdeckt. Fachliche Normdateien wie GND, VIAF oder ORCID gehören
als eigene Property-Typen in die jeweilige Wissensbasis (§3.5).

Der Body der Notiz `proptypes/hkf-wikidata.md` beschreibt, wie sich aus der
Kennung weitere Angaben beschaffen lassen. Eine Wissensbasis SOLLTE diesen
Text führen: Er ist die einzige Stelle, an der ein Werkzeug erfährt, was mit
der Kennung anzufangen ist.

`hkf-file` verweist auf eine Mediendatei, nicht auf eine Notiz. Der Wert ist
ein qualifizierter Wikilink nach §3.6, der aber die **Dateiendung behält**,
weil sie bei einer Mediendatei zum Namen gehört:

```yaml
portrait: "[[media/images/persons/portraet-ada.png|portraet-ada.png]]"
```

- Das Ziel MUSS in einem der vier Medienverzeichnisse aus §3.2.1 liegen und
  eine Dateiendung tragen, die nicht `.md` ist.
- In Properties steht der Link ohne `!`. Einbettungen wie `![[…]]` sind
  gewöhnliches Markdown und nur im Body erlaubt.
- `hkf-file` darf mit einer **Medienart** eingeschränkt werden:
  `hkf-file:image`, `hkf-file:image,video`. Ohne Angabe ist jede Art
  zulässig. Das Verfahren entspricht dem der Zieltypen (§3.7.1).
- Die Listenform `hkf-file-list` ergibt sich aus §3.5.2 und darf ebenfalls
  eine Medienart tragen: `hkf-file-list:image`.

Ihre Bedeutung ist festgelegt und darf von einer Ablage nicht umdefiniert
werden. Ein Bundle darf sie weglassen, weil jede HKB sie ohnehin kennt; jede
andere verwendete Property-Typ-Notiz muss es mitliefern (§4).

`hkf-link` und `hkf-link-list` sind die einzige Art, einen Verweis in einer
Property zu führen. Auf welchen Typ der Verweis zeigt, legt die
Property-Tabelle fest, nicht der Property-Typ — siehe §3.7.1.

### 3.5.2 Listenformen

Zu jedem Property-Typ gehört ohne weitere Definition eine **Listenform**. Sie
heißt wie der Property-Typ mit angehängtem `-list`:

> `<property-typ>-list` bezeichnet eine Property der Wertform `list`, deren
> Einträge **je einzeln** den Property-Typ `<property-typ>` erfüllen.

Damit sind `hkf-url-list`, `hkf-email-list`, `hkf-phone-list` und jede weitere
Listenform sofort verwendbar, ohne dass eine Notiz in `proptypes/` angelegt
wird. Geprüft werden `pattern`, `values`, `min`, `max` und ein etwaiger
Zieltyp je Eintrag; `unit` gilt für alle Einträge gemeinsam.

- Die Listenform gibt es nur zu Property-Typen, deren `form` **nicht** `list`
  ist. `hkf-link-list-list` existiert nicht.
- `hkf-link-list` ist genau die so abgeleitete Listenform von `hkf-link`. Sie
  liegt zusätzlich als Notiz vor, weil sie besonders häufig gebraucht wird;
  die Regel liefert dasselbe Ergebnis. Ein Werkzeug MUSS ein `-list` deshalb
  **zuerst abtrennen** und erst dann entscheiden, welche Argumente ein `:`
  zulässt — sonst hält es `hkf-link-list:person` für unzulässig, obwohl §3.7.1
  es ausdrücklich erlaubt.
- Der Name eines eigenen Property-Typs darf nicht auf `-list` enden, damit er
  nicht mit einer Listenform verwechselt wird.
- Eine leere Liste wird nicht geschrieben; die Property entfällt dann (§3.4).

## 3.6 Verweise

Jeder Verweis auf eine Notiz derselben Ablage ist ein **qualifizierter
Wikilink**: das Ziel ist der vollständige Pfad, unter dem die Zieldatei liegt,
ohne die Endung `.md`. Er setzt sich zusammen aus dem Ablagepfad (§3.1), dem
`base` und der Notiz-ID.

```markdown
[[persons/ada-lovelace|Ada Lovelace]]
[[wissen/persons/ada-lovelace|Ada Lovelace]]   ← bei base: wissen
```

Ein Verweis trägt **standardmäßig einen Alias** — den Teil hinter `|`. Der
vollständige Pfad ist für Werkzeuge da, für Lesende ist er Ballast: ohne Alias
steht mitten im Satz `test/persons/ada-lovelace` statt `Ada Lovelace`. Der
Alias ist der `title` des Ziels, ersatzweise sein Dateiname; bei einer
Mediendatei ihr Dateiname samt Endung. Ein Verweis ohne Alias bleibt zulässig
und auflösbar, ist aber nicht die Vorzugsform — `hk-lint` meldet ihn als
Hinweis und `hk-lint --fix` ergänzt ihn.

Ein abweichender Alias ist erlaubt, wo der Satzbau ihn verlangt, etwa eine
gebeugte Form oder eine Kurzform.

**In einer Markdown-Tabelle wird der senkrechte Strich maskiert.** Er trennt
dort die Spalten, und ein unmaskierter Alias-Strich zerlegt die Zelle und
zerstört den Link:

```markdown
| [[persons/ada-lovelace\|Ada Lovelace]] | person | neu |
```

Das ist derselbe Verweis; nur die Tabellenzeile verlangt das `\`. Ausserhalb
von Tabellen steht der Strich unmaskiert. `hk-lint` prüft beide Formen und
meldet einen unmaskierten Strich in einer Tabellenzelle als Fehler.

Auch in Properties. YAML verlangt dort Anführungszeichen:

```yaml
organizer: "[[organisations/analytical-society|Analytical Society]]"
participants:
  - "[[persons/ada-lovelace|Ada Lovelace]]"
  - "[[persons/charles-babbage|Charles Babbage]]"
```

- Ein Wikilink ohne Verzeichnisanteil wie `[[ada-lovelace]]` ist nur dann
  konform, wenn die Zieldatei unmittelbar in der Wurzel der Ablage liegt —
  dann ist der Dateiname bereits der vollständige Pfad. Das trifft in der
  Praxis auf die Wurzeldatei zu: `[[hkb]]` und `[[bundle]]` sind konform.
  Für jede Notiz in einem Typverzeichnis ist ein verzeichnisloser Link
  **nicht** konform, auch wenn Obsidian ihn auflösen könnte.
- `.md`, `./` und `../` kommen im Ziel nicht vor. Mediendateien behalten
  dagegen **immer** ihre Dateiendung, weil sie dort zum Namen gehört:
  `[[media/images/portraet-ada.png|portraet-ada.png]]`.
- In einer HKB bilden Ablagepfad und `base` zusammen den **Präfix** jedes
  Verweises. Er ist genau der Pfad, unter dem Obsidian die Datei findet; damit
  bleibt ein Verweis klickbar, auch wenn die Wissensbasis nur ein
  Unterverzeichnis des Vaults ist.
- In einem Bundle gibt es keinen Präfix. Das Ziel ist die Notiz-ID selbst,
  weil ein Bundle keinen Ablagepfad hat (§3.1) und `base` dort immer leer ist.
- Import und Export tauschen genau diesen Präfix aus (§6) — mehr geschieht mit
  einem Verweis beim Wechsel zwischen Lieferung und Wissensbasis nicht.
- **Die Wurzeldatei verweist relativ zu sich selbst.** In `hkb.md` und
  `hbundle.md` — und in einer begleitenden Anleitung wie `AGENTS.md`, die
  daneben liegt — beginnt ein Ziel beim Wurzelverzeichnis der Ablage, ohne
  Ablagepfad: `[[specifications/hkf-core-1.0|HKF Core 1.0]]`. Diese Dateien
  beschreiben die Ablage von innen und dürfen nicht wissen müssen, wo sie im
  Vault liegt;
  sonst stünde der Ablagepfad doppelt da und ein Verschieben der Wissensbasis
  erzwänge, die Wurzeldatei umzuschreiben.

  Der Preis ist, dass Obsidian ein solches Ziel nur auflöst, solange es im
  Vault eindeutig ist. Das ist hinnehmbar: Diese Dateien tragen wenige
  Verweise, während eine Notiz zwischen Tausenden stehen kann.
- Externe Ziele werden als gewöhnliche Markdown-Links geschrieben.
- Ein Link trägt keine Beziehungsart. Die ergibt sich aus dem Property-Namen
  oder aus dem umgebenden Text.

## 3.7 Typdefinitionen

Eine Typdefinition registriert einen Typ. Der **Dateiname ist der Typname**.
Das folgende Beispiel ist ein gekürzter Auszug des Typs `person` aus HKF Base;
dort steht seine verbindliche Fassung.

```markdown
---
type: typedef
title: Person
description: Ein Mensch als Gegenstand der Wissensbasis.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| born | date | nein | Geburtsdatum |
| died | date | nein | Sterbedatum |
| homepage | hkf-url | nein | Persönliche Webseite |
| email | hkf-email | nein | Kontaktadresse |
| employer | hkf-link:organisation | nein | Arbeitgeber |
| memberships | hkf-link-list:organisation | nein | Mitgliedschaften |

# Konventionen

Dateiname ist Nachname-Vorname in kebab-case.
```

- `dir` ist der Ablageort der Instanzen als **Pfad relativ zum Basispfad**.
  Optional; Vorgabe ist der Typname mit angehängtem `s`. Die Kern-Typen und
  das Vokabular aus HKF Base kommen damit aus; nur ein Typ, der abweichend
  abgelegt werden soll, schreibt ihn.

  Der Pfad darf mehrere Abschnitte haben. Damit lassen sich Typverzeichnisse
  gruppieren, ohne die Typnamen zu verlängern:

  ```yaml
  dir: reihen                  # ein Abschnitt
  dir: veranstaltungen/reihen  # mehrere
  dir: stammdaten/kunde        # Gruppierung nach Herkunft
  ```

  Es gelten die Regeln aus §3.2: Kein `dir` darf unter einem anderen liegen,
  auch nicht unter einem der drei Pflichtverzeichnisse. `stammdaten/kunde` und
  `stammdaten/lieferant` sind nebeneinander zulässig — sie teilen sich ein
  Elternverzeichnis, aber keines liegt im anderen. `stammdaten` selbst wäre
  dann für keinen weiteren Typ mehr frei.

  Ein Gruppierungsverzeichnis wie `stammdaten` ist selbst **kein**
  Typverzeichnis. Eine Notiz, die unmittelbar darin läge, gehörte zu keinem
  Typ und wäre ein Befund (§3.7.1).
- `description` ist Pflicht und eine Zeile lang. Sie erscheint in der
  Typtabelle der Wurzeldatei und ist damit oft die einzige Information, die
  ein Werkzeug über einen Typ liest.
- Typnamen sind kleingeschrieben, aus Buchstaben, Ziffern und Bindestrichen,
  und in der Ablage eindeutig.

### Die Property-Tabelle

Der Abschnitt `# Properties` ist optional. Ist er vorhanden, ist er
**normativ** und wird von `hk-lint` geprüft.

- **Property** — der `snake_case`-Name im Frontmatter.
- **Typ** — entweder eine Wertform aus §3.4 oder der Name eines
  Property-Typs aus `proptypes/`. Bei `hkf-link` darf ein Zieltyp, bei
  `hkf-file` eine Medienart angehängt werden (§3.7.1). Mehrere zulässige
  Typen werden mit ` / ` getrennt, und die Beschreibung nennt sie in Worten
  (§3.7.2).
- **Pflicht** — `ja` oder `nein`.
- **Beschreibung** — freier Text. Stehen in der Typ-Spalte Alternativen, nennt
  sie die Beschreibung ausdrücklich, damit die Zeile für sich verständlich ist.

`type` wird nicht aufgeführt; es gilt für jede Notiz. Properties, die nicht
in der Tabelle stehen, sind weiterhin erlaubt und werden nicht geprüft
(§3.3). Die Tabelle beschränkt also nicht, sie sichert zu. Wer sehen will,
was außerhalb der Zusicherungen liegt, ruft `hk-lint --strict` (§6.3).

### 3.7.1 Die Typ-Angabe

Ein Verweis in einer Property hat den Property-Typ `hkf-link` (ein Verweis)
oder `hkf-link-list` (mehrere). Beide sagen für sich nur, dass der Wert ein
qualifizierter Wikilink ist — nicht, worauf er zeigt. Der **Zieltyp** legt das
fest. Er steht in der Typ-Spalte der Property-Tabelle, nicht im Property-Typ,
denn derselbe Property-Typ wird an vielen Stellen mit verschiedenen Zielen
verwendet.

#### Schreibweise

```text
typzelle      = typangabe { " / " typangabe }
typangabe     = wertform | proptypangabe | linkangabe | medienangabe
proptypangabe = proptyp-name [ "-list" ]
linkangabe    = "hkf-link" [ "-list" ] [ ":" zieltypen ]
medienangabe  = "hkf-file" [ "-list" ] [ ":" medienarten ]
zieltypen     = typname { "," typname }
medienarten   = medienart { "," medienart }
medienart     = "image" | "video" | "audio" | "document"
```

Die beiden Trennzeichen bedeuten Verschiedenes und stehen auf verschiedenen
Ebenen:

- `,` trennt **Argumente eines Typs**, ohne Leerzeichen — welche Zieltypen
  oder Medienarten er zulässt.
- ` / ` trennt **ganze Typen**, mit Leerzeichen auf beiden Seiten — welche
  Property-Typen der Wert überhaupt haben darf (§3.7.2). Die Leerzeichen sind
  Pflicht: Ohne sie liest sich `image/hkf-url` wie ein Pfad.

- Zwischen `hkf-link`, `:`, den Typnamen und den `,` steht **kein**
  Leerzeichen.
- `typname` ist der Dateiname einer Typdefinition ohne `.md`, also der
  Typname selbst — nicht sein Verzeichnis.
- Mehrere Typnamen bedeuten **oder**: das Ziel muss von einem der genannten
  Typen sein.
- Ohne `:` ist jeder Typ zulässig.
- Der `:`-Zusatz ist **ausschließlich** bei `hkf-link` und `hkf-file` samt
  ihren Listenformen erlaubt: bei `hkf-link` mit Typnamen, bei `hkf-file` mit
  Medienarten. An einer Wertform oder einem anderen Property-Typ ist er ein
  Fehler in der Typdefinition.

| Zelle | Bedeutung |
|---|---|
| `hkf-link` | ein Verweis auf eine Notiz beliebigen Typs |
| `hkf-link:organisation` | ein Verweis auf eine Notiz vom Typ `organisation` |
| `hkf-link:person,organisation` | ein Verweis auf eine Notiz vom Typ `person` **oder** `organisation` |
| `hkf-link-list:person` | eine Liste; **jeder** Eintrag verweist auf eine `person` |
| `hkf-file` | ein Verweis auf eine Mediendatei beliebiger Art |
| `hkf-file:image` | ein Verweis auf eine Datei unter `<media_base>/images/` |
| `hkf-file-list:image,video` | eine Liste aus Bildern und Videos |
| `hkf-file:image / hkf-url` | eine Datei **oder** eine Adresse — Alternative, §3.7.2 |

#### Auflösung

Der Typ eines Verweisziels wird **allein aus dem Pfad** bestimmt. Die
Zieldatei wird dafür nicht geöffnet. Das ist der Zweck der typbezogenen
Ablage aus §3.2: Ein Werkzeug prüft einen Verweis, ohne die verlinkte Notiz zu
lesen.

Für einen Wert wird der Reihe nach ermittelt:

1. **Wikilink erkennen.** Der Wert muss als Ganzes `[[ziel]]` oder
   `[[ziel|anzeigetext]]` sein. Der Anzeigetext ist für die Prüfung ohne
   Bedeutung. Ein Wert mit Text vor oder nach den Klammern ist kein Verweis
   und damit ein Formfehler.
2. **Ziel entnehmen.** `ziel` ist der Pfad ab der Wurzel der Ablage — bei
   einer Notiz ohne `.md`, bei einem Anhang mit seiner Dateiendung (§3.6).
   Ein verzeichnisloses oder relatives Ziel ist ein Verstoß gegen §3.6 und
   wird nicht geraten.
3. **Basispfad abziehen.** Beginnt `ziel` mit dem `base` der Ablage, wird
   dieses Präfix samt folgendem `/` entfernt. Übrig bleibt die Notiz-ID.
4. **Mediendatei erkennen.** Liegt `ziel` unter `<media_base>/images/`,
   `/videos/`, `/audios/` oder `/documents/`, ist es eine Mediendatei und
   keine Notiz. Die Medienart ergibt sich aus dem Verzeichnis. Ist eine
   Medienart gefordert, MUSS sie eine der genannten sein. Zulässig ist das
   nur für `hkf-file`; für `hkf-link` ist es ein Fehler. Die Prüfung endet
   hier. Für `hkf-file` endet sie umgekehrt hier auch dann, wenn das Ziel
   **keine** Mediendatei ist — dann als Fehler.
5. **Typverzeichnis suchen.** Gesucht wird die Typdefinition, deren `dir` ein
   **segmentweises Präfix** der Notiz-ID ist. Der Vergleich läuft über ganze
   Pfadsegmente: `persons` ist ein Präfix von `persons/historisch/ada`,
   aber nicht von `persons-archiv/ada`. Nach §3.2 trifft höchstens eine
   Typdefinition zu.
6. **Tatsächlichen Typ bestimmen.** Er ist der Typname der gefundenen
   Typdefinition.
7. **Vergleichen.** Ist ein Zieltyp angegeben, MUSS der tatsächliche Typ
   einer der genannten sein. Der Vergleich ist exakt und
   groß-/kleinschreibungsempfindlich.

HKF kennt **keine** Ober- oder Untertypen. Ein Zieltyp passt nur auf sich
selbst; `hkf-link:organisation` akzeptiert keine Notiz vom Typ `verein`, auch
wenn ein Verein fachlich eine Organisation ist. Sollen beide zulässig sein,
werden beide genannt: `hkf-link:organisation,verein`.

Bei `hkf-link-list` wird jeder Eintrag einzeln nach diesem Verfahren geprüft.
Alle Einträge unterliegen derselben Zieltypangabe.

#### Beispiel

Gegeben `base: wissen` und die Typdefinitionen `person` → `persons` sowie
`organisation` → `organisations`:

```yaml
# in wissen/persons/ada-lovelace.md
employer: "[[wissen/organisations/analytical-society|Analytical Society]]"
```

| Schritt | Ergebnis |
|---|---|
| 1. Wikilink | Ziel `wissen/organisations/analytical-society` |
| 2. Ziel | vollständiger Pfad, konform zu §3.6 |
| 3. Basispfad `wissen` abziehen | Notiz-ID `organisations/analytical-society` |
| 4. Mediendatei? | nein, `organisations` ist kein Medienverzeichnis |
| 5. Typverzeichnis | `organisations` |
| 6. Tatsächlicher Typ | `organisation` |
| 7. Vergleich mit `hkf-link:organisation` | erfüllt |

#### Fehlerfälle

| Fall | Befund |
|---|---|
| Wert ist kein reiner Wikilink | Formfehler an der Notiz |
| Ziel ohne Verzeichnis, obwohl die Zieldatei nicht in der Wurzel liegt, oder Ziel mit `./`, `../`, `.md` | Verstoß gegen §3.6 an der Notiz |
| Ziel ist eine Mediendatei, der Typ ist `hkf-link` | Verweis auf eine Mediendatei statt auf eine Notiz |
| Ziel ist **keine** Mediendatei, der Typ ist `hkf-file` | Verweis auf eine Notiz statt auf eine Mediendatei |
| `hkf-file`-Ziel ohne Dateiendung oder mit `.md` | keine Mediendatei |
| Medienart des Verzeichnisses nicht unter den geforderten | Medienartfehler an der Notiz |
| Verzeichnis unmittelbar unter `media_base` ist keines der vier | Verstoß gegen §3.2.1 an der Ablage |
| Kein Typverzeichnis ist Präfix der Notiz-ID | Ziel ist keine Notiz — etwa `hkb.md` oder eine Datei außerhalb der Typverzeichnisse |
| Zieldatei existiert nicht | toter Verweis; der Zieltyp gilt trotzdem als geprüft, weil er aus dem Pfad folgt |
| Tatsächlicher Typ nicht unter den Zieltypen | Zieltypfehler an der Notiz |
| Genannter Zieltyp ist in der Ablage nicht registriert | Fehler an der **Typdefinition**, nicht an der Notiz |
| `:` an einer Wertform oder an einem anderen Property-Typ | Fehler an der Typdefinition |

Zieltypen gelten ausschließlich für Properties. Wikilinks im Body sind an
keinen Typ gebunden; sie müssen nur §3.6 erfüllen und auflösbar sein.

Was in einem Code-Span oder Codeblock steht, ist kein Verweis. Obsidian
verlinkt es nicht, und `hk-lint` prüft es nicht. Beispiel-Wikilinks in
erläuterndem Text — etwa in einer `proptype`-Notiz — gehören deshalb in
Backticks; sonst sind sie echte Verweise und müssen auflösbar sein.

### 3.7.2 Alternativen

Manche Properties dürfen auf zwei verschiedene Weisen belegt sein. Ein
Porträt etwa liegt entweder als Bild in der Ablage oder es steht im Netz. Für
solche Fälle nennt die Typ-Spalte mehrere Property-Typen, getrennt durch
` / ` — mit Leerzeichen, damit der Schrägstrich nicht als Pfadtrenner gelesen
wird:

```text
| portrait | hkf-file:image / hkf-url | nein | als Datei in der Ablage oder als Adresse im Netz |
```

**Die Beschreibung nennt die Alternativen in Worten.** Das ist keine Zierde:
Eine Typdefinition soll den vollständigen Vertrag ihres Typs tragen, ohne dass
man die Grammatik dieser Spezifikation kennt. Wer nur die Tabelle liest, muss
aus der Beschreibungsspalte erfahren, dass beides zulässig ist.

```yaml
portrait: "[[media/images/portraet-ada.png|portraet-ada.png]]"   # erste Alternative
portrait: https://example.org/ada.jpg                           # zweite Alternative
```

Ein Werkzeug liest den Trenner auch ohne Leerzeichen; geschrieben wird er mit.
`hk-lint --fix` ergänzt sie.

**Prüfung.** Die Alternativen werden der Reihe nach durchprobiert. Erfüllt der
Wert eine davon vollständig, ist die Property gültig. Erfüllt er keine, meldet
`hk-lint` einen Befund, der alle Alternativen nennt — er rät nicht, welche
gemeint war.

**Einschränkung.** Alle Alternativen MÜSSEN dieselbe Wertform haben. Obsidian
ordnet einem Property-Namen genau einen Property-Typ zu; eine Property, die
mal `text` und mal `number` wäre, ließe sich dort nicht führen.

- `hkf-file:image / hkf-url` ist zulässig — beide sind `text`.
- `hkf-file-list:image / hkf-url-list` ist zulässig — beide sind `list`.
- `hkf-url / hkf-year` ist unzulässig — `text` gegen `number`.
- `hkf-file:image / hkf-url-list` ist unzulässig — `text` gegen `list`.

Damit ergibt sich die Wertform der Property eindeutig aus jeder ihrer
Alternativen. Ein Verstoß ist ein Fehler an der Typdefinition, nicht an der
Notiz.

Eine Alternative ist kein Ersatz für zwei Properties. Sie ist am Platz, wenn
beide Formen **dasselbe** bezeichnen und sich ausschließen. Bezeichnen sie
Verschiedenes — etwa die Fundstelle einer Quelle und ihr beigelegtes
Dokument —, gehören sie in zwei Properties.

## 3.8 Kern-Typen

Jede Ablage registriert mindestens diese drei Typen. Die Vorgabe für `dir`
ergibt genau die drei Pflichtverzeichnisse aus §3.2.

| Typ | Verzeichnis | Zweck |
|---|---|---|
| `typedef` | `typedefs` | Registriert einen Typ und legt sein Verzeichnis fest. |
| `proptype` | `proptypes` | Schränkt eine Wertform ein. |
| `bundle` | `bundles` | Beschreibt eine Lieferung. |

Ihre Typdefinitionen und die erlaubten Properties stehen in Anhang A, dort
zusammen mit den Properties der Wurzeldateien und den notizübergreifenden
Properties.

Mehr definiert dieses Dokument nicht. Jede Ablage ergänzt die Typen, die sie
braucht; ein verbreitetes Vokabular liefert **HKF Base**.

Die drei Kern-Typen und die zwölf Property-Typen aus §3.5.1 bilden zusammen
die **Grundausstattung** einer HKB. Sie entsteht mit der Wissensbasis und wird
nicht geliefert: Ohne den Typ `typedef` ließe sich keine Typdefinition
ablegen, ohne `bundle` keine Lieferung verbuchen, ohne `proptype` kein
Property-Typ einordnen. Ein Import setzt sie voraus.

---

# 4. HKF — das Bundle-Format

Ein Bundle ist eine übertragbare, für sich lesbare Auswahl von Notizen. Es
folgt vollständig dem Kern aus §3, mit drei Festlegungen:

1. Die Wurzeldatei heißt `hbundle.md` und ist zugleich die Bundle-Notiz.
2. `base` ist immer leer. Die Typverzeichnisse liegen direkt in der Wurzel.
3. Das Bundle enthält **jede** Typdefinition und jeden Property-Typ, den
   seine Notizen verwenden, sowie jede Mediendatei, auf die sie verweisen.
   Zwei Ausnahmen, und beide beruhen darauf, dass die Sache garantiert
   vorhanden ist:

   - die **Grundausstattung** aus §3.8, die jede HKB führt;
   - alles, was ein **vorausgesetztes Bundle** liefert (§4.1). Wer `hkf-base`
     voraussetzt, darf die Typen aus HKF Base weglassen.

   Ohne eine solche Voraussetzung liefert ein Bundle auch die zugeladenen
   Typen mit, die es benutzt: Eine HKB muss sie nicht führen, ein Bundle darf
   sich ungefragt nicht auf sie verlassen.

```text
biografie-2026/                 ← base: "", media_base: media
  hbundle.md
  typedefs/person.md
  typedefs/organisation.md
  proptypes/hkf-url.md          ← optional, jede HKB kennt ihn
  media/images/portraet-ada.png
  media/documents/notes-on-the-analytical-engine.pdf
  persons/ada-lovelace.md
  organisations/analytical-society.md
```

## 4.1 Die Bundle-Notiz

```markdown
---
hkf: "1.0"
type: bundle
id: biografie-2026
base: ""
media_base: media
title: Biografische Notizen, Ausgabe 2026
source: https://example.org/biografie.git
version: "4c73e21"
---

Kurzbeschreibung des Inhalts.

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| person | persons | Ein Mensch. |
| organisation | organisations | Eine Körperschaft. |
```

- `id` ist Pflicht und eine stabile Kennung der Lieferreihe. Sie ist
  `kebab-case`: Kleinbuchstaben, Ziffern und Bindestriche, beginnend mit einem
  Buchstaben.

  Das ist keine Formsache. Die `id` wird in der aufnehmenden Wissensbasis zum
  Dateinamen `bundles/<id>.md` (§5.1), und in `required_bundles` trennt ein
  Leerzeichen sie von der Fassungsbedingung. Eine `id` mit Leerzeichen zerlegt
  also den Eintrag, der sie voraussetzt; eine mit `/` beansprucht ein
  Verzeichnis; eine mit Großbuchstaben kollidiert auf einem Dateisystem, das
  Groß- und Kleinschreibung nicht unterscheidet. Innerhalb einer Wissensbasis
  ist sie damit auch eindeutig — sie ist ja der Dateiname.
- `description` ist Pflicht: ein Satz darüber, was die Lieferung enthält.
- `required_bundles` nennt Bundles, die vor diesem importiert sein sollen.
  Optional.
- `version` bezeichnet die konkrete gelieferte Fassung: Versionsname,
  Commit-Hash oder eine andere unveränderliche Kennung. Pflicht.
- `source` und `title` sind optional.
- Weil die Bundle-Notiz zugleich Wurzeldatei ist, trägt sie `hkf`, `base` und
  `media_base` aus §3.1 und die Typtabelle im Body.

Ein Bundle enthält keine Bundle-Notizen anderer Bundles. Verschachtelte
Lieferungen gibt es nicht.

### Voraussetzungen

Ein Bundle darf verlangen, dass andere Bundles bereits in der Wissensbasis
liegen:

```yaml
required_bundles:
  - hkf-base >= 1.0
  - firmenglossar
```

Jeder Eintrag ist ein Text aus der `id` des vorausgesetzten Bundles und einer
optionalen Fassungsbedingung, getrennt durch ein Leerzeichen.

- **Ohne Bedingung** genügt jede Fassung. Das ist die allgemein anwendbare
  Form.
- **`>= X.Y`** ist erfüllt, wenn die vorhandene Fassung dieselbe Zahl vor dem
  Punkt trägt und die Zahl dahinter mindestens `Y` ist. `>= 1.0` wird also von
  `1.0` und `1.7` erfüllt, nicht von `0.9` und nicht von `2.0`.

`>=` ist der einzige Operator. Eine Obergrenze gibt es nicht: Ein Bundle kann
sinnvoll einen Mindeststand verlangen, aber nicht wissen, was künftige
Fassungen bringen. Dass die Zahl vor dem Punkt übereinstimmen muss, vertritt
die Obergrenze — sie wird erhöht, wenn eine Fassung Bestehendes bricht.

**Eine Fassungsbedingung ist nur zulässig, wenn beide Fassungen die Form
`Zahl.Zahl` haben.** Für `version` lässt §4.1 auch einen Versionsnamen oder
einen Commit-Hash zu; über solche Werte gibt es keine Ordnung, und ein
Werkzeug darf sie nicht raten. Ein Bundle, das mit Hashes versioniert wird,
lässt sich nur ohne Bedingung voraussetzen.

Ein Bundle darf sich nicht selbst voraussetzen, und Voraussetzungen dürfen
keinen Kreis bilden.

Eine unerfüllte Voraussetzung hält den Import nicht auf. Sie wird gemeldet,
und die Typen, die das fehlende Bundle definiert hätte, bleiben so lange
vorläufig (§5.5, §6.1). Eine Voraussetzung sagt also, in welcher Reihenfolge
zu laden ist, nicht, was ohne sie unmöglich wäre.

## 4.2 Zugehörigkeit

Notizen eines Bundles tragen **keine** Markierung ihrer Zugehörigkeit. Sie
liegen im Bundle, also gehören sie dazu. Ein Manifest gibt es nicht; das
Dateisystem ist das Manifest.

Erst beim Import in eine HKB entsteht daraus mehr: die Zugehörigkeit als
Property jeder Notiz (§5.2), der Importnachweis in der Bundle-Notiz (§5.1)
und die Verknüpfung mit dem Bestand (§5.7). Die erste sagt, was jetzt gilt;
der zweite, was damals geliefert wurde; die dritte, wie die Lieferung mit dem
zusammenhängt, was schon da war. Keines davon steht im Bundle, weil keines
die Lieferung beschreibt.

---

# 5. HKB — die Knowledge Base

Eine HKB ist eine Ablage nach §3 in einem Obsidian-Vault, mit diesen
Zusätzen:

1. Ihre Wurzeldatei heißt `hkb.md` und liegt in ihrem Wurzelverzeichnis. Das
   darf die Vault-Wurzel sein, muss es aber nicht: Eine HKB darf ebenso gut
   in einem Unterverzeichnis liegen, dann ist dessen Pfad ihr Ablagepfad.
2. `base` darf gesetzt sein und verschiebt alle Typverzeichnisse innerhalb
   der HKB dorthin.
3. Sie enthält die Standard-Property-Typen aus §3.5.1.
4. Sie führt `bundles/` mit einer Notiz je importiertem oder exportierbarem
   Bundle.
5. Sie stellt die Methoden aus §6 bereit.

```markdown
---
hkf: "1.0"
name: Henni Knowledge Base
base: ""
media_base: media
timezone: Europe/Berlin
---

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| typedef | typedefs | Registriert einen Typ. |
| proptype | proptypes | Schränkt eine Wertform ein. |
| bundle | bundles | Beschreibt eine Lieferung. |
| person | persons | Ein Mensch. |
```

`name` ist ein freier Anzeigename und Pflicht. `timezone` ist optional.

Beispiel mit `base: wissen`:

```text
hkb.md
wissen/typedefs/person.md
wissen/proptypes/hkf-url.md
wissen/bundles/biografie-2026.md
wissen/persons/ada-lovelace.md
media/images/portraet-ada.png
```

`base` und `media_base` sind voneinander unabhängig. Die Medienverzeichnisse
liegen hier neben dem Basispfad, nicht darin.

## 5.1 Bundle-Notizen in der HKB

Ein importiertes Bundle wird als `<base>/bundles/<id>.md` abgelegt. Es ist
dieselbe Notiz wie `hbundle.md` im Bundle, mit zwei Unterschieden:

- Die Wurzeldatei-Properties `hkf`, `base` und `media_base` sowie die
  Typtabelle im Body entfallen, weil sie in der HKB von `hkb.md` kommen.
- `imported` (datetime) hält den Zeitpunkt der Übernahme fest.

```markdown
---
type: bundle
id: biografie-2026
title: Biografische Notizen, Ausgabe 2026
source: https://example.org/biografie.git
version: "4c73e21"
imported: 2026-08-27T11:00:00
---

Kurzbeschreibung des Inhalts.
```

Der Dateiname entspricht der `id`. Eine HKB darf beliebig viele Bundles
importieren.

### Der Importnachweis

Der Body der Bundle-Notiz hält fest, was eine Lieferung **zum Zeitpunkt ihres
Imports** enthielt. Je übernommener Fassung entsteht ein Abschnitt
`# Import <version>`, die neueste zuerst:

```markdown
# Import a3f9c21

Übernommen am 2026-08-27T12:45:00.

| Notiz | Typ | Zustand |
|---|---|---|
| [[persons/ada-lovelace\|Ada Lovelace]] | person | neu |
| [[persons/charles-babbage\|Charles Babbage]] | person | neu |
| [[places/london\|London]] | place | aktualisiert |

| Mediendatei | Medienart | Zustand |
|---|---|---|
| [[media/images/portraet-ada.png\|portraet-ada.png]] | image | neu |

| Verweis | Gegenstelle | Grund |
|---|---|---|
| [[persons/ada-lovelace\|Ada Lovelace]] | [[places/london\|London]] | beide nennen einander |
```

- Die erste Spaltenüberschrift unterscheidet die drei Tabellen: `Notiz`,
  `Mediendatei` und `Verweis`. Eine Tabelle entfällt, wenn die Lieferung
  nichts der Art hervorgebracht hat.
- Die dritte Tabelle hält fest, was die Verknüpfung angelegt hat (§5.7).
  Sie ist die einzige Stelle, an der ein Import nachweist, dass er eine
  Notiz **außerhalb** der Lieferung angefasst hat; die Gegenstelle steht
  darum ausdrücklich dabei.
- Die Einträge sind qualifizierte Wikilinks nach §3.6, also die Pfade **in
  der HKB**, nicht die der Lieferung.
- `Zustand` ist `neu`, `aktualisiert` oder `übersprungen` — was der Import mit
  dem Eintrag getan hat.
- Ein Abschnitt wird **einmal** geschrieben, wenn seine Fassung zum ersten Mal
  ankommt. Ein wiederholter Import derselben `version` lässt ihn unverändert;
  sonst stünde beim zweiten Lauf überall `übersprungen` und der Nachweis
  bezeichnete nicht mehr den Zeitpunkt des Imports.
- Das Frontmatter nennt mit `version` und `imported` immer die **neueste**
  übernommene Fassung.

Der Importnachweis ist ein **Protokoll, keine Zugehörigkeitsangabe**. Was
aktuell zu einem Bundle gehört, sagt allein die Property `bundles` der Notizen
(§5.2). Beide können auseinanderlaufen, und das ist beabsichtigt: Eine später
gelöschte oder aus dem Bundle genommene Notiz bleibt im Nachweis der Fassung
stehen, in der sie geliefert wurde. `hk-lint` prüft darum nur die Form des
Nachweises; ein Eintrag ohne vorhandenes Ziel ist ein Hinweis, kein Fehler.

## 5.2 Zugehörigkeit in der HKB

Weil in der HKB alle Notizen typbezogen zusammenliegen, geht die Trennung
nach Lieferung verloren. Sie wird deshalb als Property geführt:

```yaml
bundles:
  - "[[bundles/biografie-2026|Biografische Notizen, Ausgabe 2026]]"
```

`bundles` hat den Typ `hkf-link-list:bundle` (§3.7.1). Eine Notiz
darf zu mehreren Bundles gehören. Notizen ohne `bundles` sind eigener Bestand
der HKB und werden von keinem Export erfasst.

Damit ist der Inhalt eines Bundles jederzeit abfragbar, ohne dass eine Liste
gepflegt oder geparst werden muss.

## 5.3 Grundausstattung und Zuladung

Eine HKB entsteht mit ihrer **Grundausstattung**: den zwölf Property-Typen aus
§3.5.1 und den drei Kern-Typen `typedef`, `proptype` und `bundle`. Sie wird
nicht geliefert, sondern angelegt, denn ein Import setzt sie voraus — er muss
Typdefinitionen ablegen, Property-Typen einordnen und die Lieferung verbuchen
können, bevor er irgendetwas anderes tut. Damit ist die Wissensbasis konform,
wenn auch leer.

Alles Weitere wird zugeladen. Das nächstliegende Bundle ist `hkf-base`, das
Vokabular aus **HKF Base**: neun Typdefinitionen und die beiden Property-Typen,
die nur mit ihnen Sinn ergeben. Notizen, Mediendateien, die Kern-Typen und die
Property-Typen der Grundausstattung enthält es nicht — die hat die
Wissensbasis bereits.

Der Import ist **freiwillig**. Eine Wissensbasis, die keine Personen und Orte
verwaltet, kommt ohne ihn aus und definiert stattdessen eigene Typen. Wer aber
einen Typ dieses Namens führt, führt ihn in der Fassung aus HKF Base — nur so
bleiben Bundles austauschbar.

Warum die Grundausstattung nicht ebenfalls ein Bundle ist: Sie zu importieren
setzte voraus, dass sie schon da ist. Der Typ `typedef` müsste sich selbst
ablegen, bevor er registriert wäre. Diese Schleife lässt sich zwar durch die
Vorgaberegel aus §3.7 auflösen — Verzeichnis gleich Typname mit angehängtem
`s` —, aber sie zu vermeiden ist einfacher, als sie zu beschreiben.

Fortschreibung ist ein erneuter Import. Bringt eine spätere Fassung einen
neuen Typ oder eine geänderte Property-Tabelle, entscheidet der Vergleich aus
§6.1 Schritt 5 je Notiz: geänderte werden übernommen, unveränderte
übersprungen. Welche Fassung eine HKB führt, sagt die `version` ihrer
Bundle-Notiz `bundles/hkf-base.md`.

Weder die Grundausstattung noch einen zugeladenen Typ darf eine HKB
abwandeln. Wer
eigene Typen oder Property-Typen braucht, legt sie daneben — dafür sind §3.5
und §3.7 da.

Ein Bundle ohne eigene Typdefinitionen nennt die benutzten Typen samt
Verzeichnis in der Typtabelle seiner Wurzeldatei. Sie ist dort nicht bloß eine
Zusammenfassung, sondern die Schnittstelle zur aufnehmenden Wissensbasis: Ein
Werkzeug liest Typname und Verzeichnis und schlägt die Definition im eigenen
Bestand nach.

## 5.4 Einstieg für Werkzeuge

Ein Modell, das einen Vault öffnet, sieht zunächst nur Markdown-Dateien.
Dass `hkb.md` der Einstieg ist, steht in dieser Spezifikation — die es weder
kennt noch findet. Die Ablage kann noch so sparsam aufgebaut sein; sie nützt
nichts, wenn niemand den ersten Satz sagt.

Eine HKB SOLLTE deshalb neben ihrer Wurzeldatei eine `AGENTS.md` führen: die
verbreitete Konvention für Anweisungen an Werkzeuge. Sie ist keine Notiz und
gehört nicht zur Ablage (§3.2); sie wird weder geprüft noch ausgeliefert.
Ihr Inhalt ist zum größten Teil abgeleitet — die Regeln sind für jede HKB
dieselben, die Typtabelle stammt aus der Wurzeldatei — und `hk-lint --fix`
darf sie neu erzeugen. Ein Abschnitt für von Hand geschriebene Hinweise bleibt
dabei erhalten.

Zwei Dinge sind dabei zu beachten. Sie liegt **neben der Wurzeldatei**, nicht
in der Vault-Wurzel, denn sie beschreibt genau eine Ablage. Und sie verweist
nach §3.6 **relativ zu sich selbst** und nennt keinen Ablagepfad, sonst
überstünde sie kein Verschieben der Wissensbasis.

Der Umfang ist der eigentliche Entwurfszwang: Die Datei wird bei jedem Start
geladen. Sie nennt die wenigen Regeln, deren Verletzung tatsächlich Schaden
anrichtet, und verweist für alles Übrige auf die Spezifikation.

## 5.5 Vorläufige Typdefinitionen

Ein Bundle bringt jede Typdefinition mit, die seine Notizen verwenden (§4).
Zwei Fälle durchbrechen das: Ein vorausgesetztes Bundle liegt noch nicht vor
(§4.1), oder das Bundle hält sich nicht an §7.1. In beiden kommt eine Notiz
an, deren Typ die Wissensbasis nicht kennt.

Sie wird trotzdem übernommen. Eine Notiz trägt als einzige Pflicht ihren
`type` (§3.3); mehr braucht es nicht, um sie abzulegen. Der Import legt dafür
eine **vorläufige Typdefinition** an:

```markdown
---
type: typedef
provisional: true
description: Vorläufig beim Import von biografie-2026 angelegt; keine Typdefinition geliefert.
created: 2026-08-27
modified: 2026-08-27T12:45:00
modified_by: hk-import
---
```

- `provisional: true` kennzeichnet sie. Das ist die einzige Property, die eine
  vorläufige Typdefinition von einer endgültigen unterscheidet.
- `dir` bleibt weg, es gilt also die Vorgabe aus §3.7: der Typname mit
  angehängtem `s`. Die Regel ist mechanisch und kein Sprachgefühl —
  `werkstoff` wird zu `werkstoffs`. Genau darauf kommt es an: Sie liefert
  denselben Ort, den auch die nachgereichte Typdefinition beansprucht, solange
  diese kein abweichendes `dir` setzt.
- Sie trägt **keinen** Abschnitt `# Properties`. Eine Property-Tabelle sichert
  zu (§3.7); eine vorläufige Typdefinition weiß nichts, was sie zusichern
  könnte.
- Sie trägt **kein** `bundles`. Sie wurde nicht geliefert, sondern beim Import
  erfunden; sie gehört der Wissensbasis, nicht der Lieferung.
- Ist das errechnete Verzeichnis bereits von einem anderen Typ belegt, lässt
  sie sich nicht anlegen, ohne §3.2 zu verletzen. Das ist ein Konflikt, und
  der Import wird abgewiesen (§6.1 Schritt 2).

Damit bleibt die Ablage vollständig: Jede Notiz hat genau eine Typdefinition,
die Typtabelle der Wurzeldatei nennt den Typ samt Verzeichnis wie jeden
anderen, die Auflösung eines Verweises über den Pfad (§3.7.1) findet ihn, und
`hkf-link:werkstoff` lässt sich prüfen. Was fehlt, ist allein die Bedeutung —
und die fehlt sichtbar.

**Ablösung.** Kommt die endgültige Typdefinition später an — meist mit dem
nachgeladenen vorausgesetzten Bundle —, ersetzt sie die vorläufige
vollständig. Das ist kein Konflikt nach §6.1 Schritt 3: Eine vorläufige
Typdefinition sichert nichts zu, also kann sie nichts bestreiten. Setzt die
ankommende ein `dir`, das vom errechneten Verzeichnis abweicht, MÜSSEN die
Notizen dorthin verschoben und alle Verweise mitgezogen werden (§3.2 Regel 5).

**Export.** Eine vorläufige Typdefinition wird nicht ausgeliefert (§6.2). Sie
behauptet nichts über den Typ; ein Bundle, das sie mitschriebe, gäbe eine
Vermutung als Vertrag aus. Der Export meldet sie stattdessen — das Bundle ist
dann in seinen Typen nicht geschlossen und braucht die richtige Typdefinition,
bevor es weitergegeben wird.

Eine vorläufige Typdefinition ist ein offener Posten, kein Dauerzustand.
`hk-lint` meldet jede als Hinweis, mit Verzeichnis und der Zahl der Notizen,
die daran hängen.

## 5.6 Gleicher Name, gleiche Bedeutung

HKF kennt keine Namensräume. Ein Typ heißt `person`, und ob damit ein Mensch
gemeint ist oder der Datensatz einer Personalverwaltung, steht nicht im Namen.
Solange eine Wissensbasis für sich bleibt, ist das gleichgültig. Beim Import
wird es zur Frage: Zwei gleichnamige Typen werden zu einem, und was einmal in
einem Verzeichnis zusammenliegt, lässt sich nur Notiz für Notiz wieder
trennen.

**Wann die Frage entfällt.** In zwei Lagen ist die Gleichheit zugesichert und
wird nicht geprüft:

1. Der Typ kommt aus einem **vorausgesetzten Bundle, das vorliegt** (§4.1).
   Genau dafür gibt es `required_bundles`: Beide Seiten beziehen sich auf
   dieselbe Lieferung, also auf dieselbe Definition.
2. Das Bundle liefert eine Typdefinition mit, die der vorhandenen **in der
   Sache gleicht** — gleiche `description` und gleiche Property-Tabelle. Dann
   steht die Übereinstimmung schwarz auf weiß.

Damit ist der Regelfall abgedeckt. Ein Import, dem beide Seiten dasselbe
Vokabular zugrunde legen, läuft ohne Rückfrage durch.

**Wann sie gestellt wird.** Bleibt der Name gleich und die Zusicherung aus,
geht der Übernahme eine **Bedeutungsprüfung** voraus:

- Das Bundle liefert eine abweichende Typdefinition für einen Namen, den die
  Wissensbasis führt, und kein vorliegendes vorausgesetztes Bundle deckt ihn.
- Das Bundle liefert für diesen Namen gar keine Typdefinition, und das Bundle,
  das sie liefern müsste, fehlt.
- Der vorhandene Typ ist selbst **vorläufig** (§5.5). Er sichert nichts zu,
  also kann er nichts bestätigen.

**Wie sie entschieden wird.** Nicht mechanisch. Ein Werkzeug legt die
Unterlagen vor — die `description` beider Seiten, ihre Property-Tabellen, die
Konventionen im Body und eine Stichprobe der ankommenden Notizen —, und ein
Mensch oder ein Sprachmodell urteilt. Ein Sprachmodell prüft dabei genau die
Frage, die die Typdefinition stellt: Sind die ankommenden Notizen Menschen im
Sinne der hinterlegten Beschreibung von `person`, oder etwas anderes, das nur
so heißt?

Es gibt drei Ausgänge, und nur einer führt weiter:

| Urteil | Folge |
|---|---|
| gleich | Die Typen werden zusammengeführt; der Import läuft weiter (§6.1 Schritt 3). |
| verschieden | Der Import wird abgewiesen. |
| nicht entscheidbar | Der Import wird abgewiesen. |

**Im Zweifel wird abgewiesen.** Zwei Typen zusammenzulegen, die nicht dasselbe
meinen, vermischt zwei Bestände in einem Verzeichnis, und jede Notiz darin
trägt danach denselben `type`; wer sie trennen will, muss jede einzeln
beurteilen. Ein abgewiesener Import kostet dagegen einen zweiten Anlauf.

Der Ausweg ist in beiden Fällen ein anderer Name. Wer das Bundle herausgibt,
benennt seinen Typ um und liefert neu; wer es empfängt, benennt seinen eigenen
um und zieht die Verweise mit (§3.2 Regel 5). Beides ist die Entscheidung
eines Menschen, und `--force` ersetzt sie nicht.

## 5.7 Verknüpfung

Eine Lieferung kommt als Insel an. Ihre Notizen verweisen aufeinander, aber
nichts im Bestand verweist auf sie, und sie verweisen auf nichts, was schon da
war. Wer die Wissensbasis von irgendeiner anderen Notiz aus durchläuft, findet
sie nicht.

Die Verknüpfung schließt diese Lücke. Sie ist der Teil des Imports, der aus
zwei Beständen einen macht — und der einzige, der eine Notiz anfasst, die gar
nicht zur Lieferung gehört. Darum ist sie hier ausführlicher beschrieben als
das Schreiben der Notizen selbst.

### Der Abschnitt `# Siehe auch`

Verweise, die nicht aus dem Text hervorgehen, stehen am Ende des Body in einem
eigenen Abschnitt:

```markdown
# Siehe auch

- [[organisations/analytical-society|Analytical Society]] — beide Notizen nennen einander
- [[persons/charles-babbage|Charles Babbage]] — im Body dieser Notiz genannt
- [[places/london|London]] — mit der Lieferung biografie-2026 als Wirkungsort gekommen
```

- Der Abschnitt heißt `# Siehe auch` und ist der **letzte** der Notiz.
- Jede Zeile ist ein Listenpunkt aus einem qualifizierten Wikilink nach §3.6,
  dann ` — `, dann **der Grund**: ein Halbsatz, warum der Verweis dasteht.
- **Der Grund ist Pflicht.** Ohne ihn wäre der Abschnitt nur eine zweite,
  schlechtere Backlink-Ansicht — die hat Obsidian schon. Mit ihm sieht der
  nächste Leser, Mensch oder Modell, ob der Verweis noch trägt, ohne beide
  Notizen zu öffnen. Der Grund sagt, **warum** verlinkt wurde, nicht, was am
  Ziel steht.
- Die Einträge stehen alphabetisch nach Anzeigetext. Damit löst ein Nachtrag
  keinen Ordnungswechsel aus und ein Textunterschied zeigt genau die eine neue
  Zeile.

### Was Maschinen dürfen

**Eine Maschine fügt hinzu und entfernt nie.** Das ist die ganze Absicherung,
die der Abschnitt braucht: Was ein Mensch hineingeschrieben oder umformuliert
hat, übersteht jeden weiteren Lauf, weil kein Lauf etwas herausnimmt.

Entfernen ist eine menschliche Handlung. Soll ein Verweis dauerhaft weg und
nicht beim nächsten Import wiederkehren, nennt die Notiz sein Ziel in
`rejected_links`:

```yaml
rejected_links:
  - "[[places/london|London]]"
```

`rejected_links` hat den Typ `hkf-link-list` und ist in jeder Notiz erlaubt
(A.2). Ein Ziel, das dort steht, wird nie wieder selbsttätig verlinkt — weder
in `# Siehe auch` noch in einer Property. Die Property hält die **Absicht**
fest, nicht den Textunterschied: Dass dieser Verweis nicht gewollt ist, gilt
weiter, auch wenn beide Notizen sich seither geändert haben.

Wer den Verweis später doch will, nimmt sein Ziel aus `rejected_links` und
setzt ihn. Beides zugleich wäre widersprüchlich, und `hk-lint` meldet es als
Fehler (§6.3).

**Eine Ablehnung gilt dem Paar, nicht der Richtung.** Es genügt, sie auf einer
Seite zu vermerken: Ein Eintrag entsteht ohnehin nur beidseitig, also fällt mit
der einen Richtung auch die andere. Das ist keine Bequemlichkeit, sondern
notwendig — die andere Seite gehört womöglich zur Grundausstattung oder zu
einer Lieferung, die man nicht anfassen will, und ein Vermerk dort verließe die
Wissensbasis beim nächsten Export ohnehin (§6.2). Wer die Ablehnung dennoch
auf beiden Seiten notiert, schadet nichts.

**Verknüpfen ändert `modified` nicht.** Ein Eintrag unter `# Siehe auch` sagt
nichts über den Gegenstand der Notiz, sondern darüber, wie die Wissensbasis
verdrahtet ist. Zählte er als Änderung, wäre jede gelieferte Notiz gleich nach
ihrer Ankunft jünger als die Lieferung, aus der sie stammt — und der Vergleich
aus §6.1 Schritt 5 lehnte sie beim nächsten Import derselben Fassung ab. Dass
eine Notiz verknüpft wurde, steht im Importnachweis (§5.1), nicht in ihren
Zeitangaben.

Das gilt allein für die Verknüpfung. Wer eine Notiz sonst maschinell ändert,
setzt `modified` und `modified_by` wie immer (§3.3).

### Gegenseitigkeit

Ein Verweis wird **in beide Richtungen** geführt. Bekommt die ankommende Notiz
einen Eintrag auf eine bestehende, bekommt die bestehende einen zurück, mit
ihrem eigenen Grund. Sonst wäre die Lieferung von innen erreichbar und von
außen nicht, und genau das soll die Verknüpfung beheben.

Der Preis ist, dass eine viel genannte Notiz Rückverweise sammelt. Ein Ort, den
jede zweite Lieferung streift, trägt nach einer Weile eine lange Liste. Dagegen
hilft kein Automatismus — welcher Verweis noch trägt, weiß nur, wer die Notiz
kennt. Es hilft der Grund: Eine Zeile, die sagt, warum sie dasteht, lässt sich
in zwei Sekunden beurteilen und streichen. Was gestrichen bleiben soll, kommt
in `rejected_links`.

### Der zweite Ort: unbelegte Properties

Eine leere Property, deren Property-Tabelle einen Zieltyp fordert, ist die
andere Stelle, an der eine Verknüpfung landet:

```text
| employer | hkf-link:organisation | nein | Arbeitgeber |
```

Steht `employer` leer und liegt im Bestand eine `organisation`, die in Frage
kommt, ist das ein Kandidat. **Gesetzt wird er nie selbsttätig.** Eine Property
behauptet eine bestimmte Beziehung — dass diese Person dort gearbeitet hat —,
ein Eintrag unter `# Siehe auch` nur, dass zwei Notizen miteinander zu tun
haben. Das erste ist eine Tatsachenbehauptung und verlangt ein Urteil; das
zweite ist ein Fingerzeig und kommt mit einem Namensvergleich aus.

Eine bereits belegte Property wird nicht angerührt, auch nicht, wenn ein
besserer Kandidat auftaucht.

### Was nicht geschieht

Erwähnungen im laufenden Text werden **nicht** zu Wikilinks gemacht. Gewachsener
Text ist die Stelle, an der Handarbeit am ehesten verlorengeht, und der Gewinn
wäre klein: Derselbe Verweis steht bereits unter `# Siehe auch`, dort mit
seinem Grund und an einem Ort, den man gefahrlos neu schreiben kann.

---

# 6. Methoden

Jede HKB stellt drei Methoden bereit, als Befehl oder als gleichwertige
Schnittstelle. Ein Bundle stellt keine Methoden bereit.

## 6.1 `hk-import <bundle-pfad>`

Übernimmt ein HKF-Bundle in die HKB.

1. `hkf`-Version und Bundle-Notiz prüfen. Dann jeden Eintrag aus
   `required_bundles` gegen die Bundle-Notizen der HKB halten. Fehlt eines
   oder ist seine Fassung zu niedrig, ist das eine **Warnung**, kein Abbruch:
   Der Import läuft weiter, und der Befund nennt das fehlende Bundle samt der
   Aufforderung, es nachzuladen und den Import zu wiederholen.

   Der naheliegende Einwand — ein Bundle, das sich auf fremde Typdefinitionen
   verlässt, hinterließe Notizen in Verzeichnissen ohne Typ — trägt nicht: Ein
   Typ ohne Definition bekommt eine vorläufige (§5.5), und die Notiz liegt
   damit in einem registrierten Verzeichnis. Was fehlt, ist die Bedeutung, und
   die steht im Befund.

   Ein Werkzeug weiß nicht, welche Typen ein Bundle mitbrächte, das es nicht
   hat. Der Befund nennt deshalb das fehlende Bundle, nicht die Typen, die
   von ihm zu erwarten wären — auch dann nicht, wenn es `hkf-base` ist. Core
   kennt das Vokabular von Base nicht und nennt es nicht.
2. **Typen abgleichen.** Bevor irgendetwas geschrieben wird, wird jeder Typ
   bestimmt, den die Lieferung verwendet: aus den mitgelieferten
   Typdefinitionen und aus dem `type` jeder Notiz. Für jeden gilt:

   | Lage | Folge |
   |---|---|
   | Die HKB kennt den Namen nicht | Der Typ wird angelegt — aus der gelieferten Typdefinition, sonst vorläufig (§5.5). |
   | Die HKB kennt ihn, die Gleichheit ist zugesichert (§5.6) | Der Typ wird zusammengeführt (Schritt 3). |
   | Die HKB kennt ihn, die Gleichheit ist offen | **Bedeutungsprüfung** (§5.6). |

   Fällt eine Bedeutungsprüfung nicht auf „gleich", **wird der Import
   abgewiesen** — ohne dass eine Notiz geschrieben wird. `--force` hebt das
   nicht auf: Ob zwei Typen dasselbe meinen, ist keine Frage, die ein
   Kennzeichen beantwortet.

   Ebenso abgewiesen wird ein Import, dessen vorläufiges Verzeichnis bereits
   einem anderen Typ gehört (§5.5).
3. Typdefinitionen und Property-Typen des Bundles übernehmen. Nicht jede
   Abweichung ist ein Konflikt — eine Property-Tabelle schränkt nicht ein,
   sondern sichert zu (§3.7), und Zusicherungen lassen sich zusammenführen:

   - Fehlt ein Typ oder ein Property-Typ in der HKB, wird er angelegt.
   - Für einen Typ, den keine Typdefinition beschreibt, entsteht eine
     vorläufige (§5.5). Eine schon vorhandene vorläufige Typdefinition wird
     von einer gelieferten vollständig ersetzt; weicht deren `dir` vom
     errechneten Verzeichnis ab, ziehen die Notizen mit (§3.2 Regel 5).
   - Ein abweichendes `dir` ist ein **Konflikt**. Die Ablage der HKB hängt
     daran; sie darf nicht stillschweigend umziehen.
   - Property-Tabellen werden **zusammengeführt**. Eine Zeile, die die HKB
     noch nicht kennt, wird ergänzt. Eine Zeile, die dieselbe Property mit
     anderer Typ-Angabe oder anderer Pflichtangabe belegt, ist ein
     **Konflikt**.
   - Bei einem Property-Typ ist jede Abweichung in `form`, `pattern`,
     `values`, `unit`, `min` oder `max` ein **Konflikt**.
   - Die Standard-Property-Typen aus §3.5.1 darf ein Bundle nicht
     umdefinieren.
   - `title`, `description` und der übrige Body einer vorhandenen
     Typdefinition bleiben unverändert. Weichen sie ab, wird das gemeldet,
     ist aber kein Konflikt.

   Bei einem Konflikt hält das Werkzeug an und meldet ihn; ein Mensch
   entscheidet. Nichts wird stillschweigend zusammengelegt.
4. Jede Notiz nach `<base>/<dir des typs>/<dateiname>` schreiben.
5. Existiert die Ziel-Notiz-ID bereits, ist es dieselbe Notiz. Welche Fassung
   gilt, entscheidet `modified`:

   | Ankommende Fassung | Verhalten |
   |---|---|
   | `modified` jünger als in der HKB | übernehmen, Zustand `aktualisiert` |
   | gleich | überspringen; weicht der Inhalt ab, melden |
   | älter | **ablehnen**, die Fassung der HKB bleibt |
   | `modified` fehlt auf einer der beiden Seiten | ablehnen, weil nicht vergleichbar |

   Eine Ablehnung ist ein gemeldeter Befund, kein Abbruch: Die übrigen Notizen
   der Lieferung werden weiter verarbeitet. `--force` übernimmt die ankommende
   Fassung in allen vier Fällen — auch die ältere und die unvergleichbare.
   Ohne dieses Kennzeichen verliert ein Import niemals eine neuere Fassung.
6. `bundles` jeder übernommenen Notiz um den Wikilink auf die Bundle-Notiz
   ergänzen. Fehlt `created`, `modified` oder `modified_by`, wird es gesetzt:
   `created` auf den Tag des Imports, `modified` auf seinen Zeitpunkt,
   `modified_by` auf den Namen des importierenden Werkzeugs. Vorhandene Werte
   bleiben unangetastet — sie beschreiben die Notiz, nicht die Lieferung, und
   ein Zurücksetzen auf den Importzeitpunkt zerstörte den Vergleich aus
   Schritt 5.
7. Mediendateien aus dem `media_base` des Bundles in den `media_base` der HKB
   übernehmen, unter derselben Medienart und demselben Pfad darunter. Trifft
   ein Pfad auf eine vorhandene Datei mit abweichendem Inhalt, ist das ein
   Konflikt: melden und ohne `--force` nicht überschreiben. Mediendateien
   tragen kein `modified`; für sie entscheidet allein das Kennzeichen.
8. Wikilinks in Body und Properties auf die Pfade der HKB umschreiben. Bei
   Notizen wird der Präfix der HKB aus Ablagepfad und `base` vorangestellt,
   bei Mediendateien Ablagepfad und `media_base` der HKB anstelle des
   `media_base` des Bundles. Unauflösbare Ziele bleiben unverändert und werden
   gemeldet.
9. **Verknüpfen.** Die übernommenen Notizen mit dem Bestand verbinden (§5.7).
   Kandidaten entstehen aus drei mechanischen Beobachtungen:

   | Beobachtung | Folge |
   |---|---|
   | `title` oder ein `aliases`-Eintrag der einen Notiz kommt im Body der anderen wörtlich vor | Eintrag in `# Siehe auch`, beidseitig, mit dem Grund „im Body genannt" beziehungsweise „nennt diese Notiz"; nennen beide einander, „beide nennen einander" |
   | Beide tragen dieselbe `hkf-wikidata`-Kennung | **kein** Verweis, sondern ein Zusammenführungskandidat: Sie meinen denselben Gegenstand, und zwei Notizen darüber gehören zusammengelegt, nicht verlinkt (§6.3) |
   | Eine leere Property fordert einen Zieltyp, und im Bestand liegt eine Notiz dieses Typs | Vorschlag; nie selbsttätig gesetzt (§5.7) |

   Selbsttätig geschrieben wird allein die erste Zeile, und auch sie nur, wenn
   das Ziel nicht in `rejected_links` steht. Alles Übrige wird vorgelegt: Ein
   Mensch oder ein Sprachmodell entscheidet und schreibt den Grund dazu. Die
   Arbeitsteilung ist dieselbe wie bei der Bedeutungsprüfung (§5.6) —
   mechanisch, was mechanisch geht; geurteilt, was nicht.

   Ein Sprachmodell darf über die drei Beobachtungen hinausgehen und
   Zusammenhänge vorschlagen, die kein Namensvergleich findet. Es trägt dann
   seinen Modellnamen in `modified_by` ein wie bei jeder anderen Änderung
   (A.2), und der Grund in der Zeile ist seine Begründung.

   Dieser Schritt lässt `modified` und `modified_by` unangetastet, auch an
   den Notizen des Bestands (§5.7). Sonst wäre jede Lieferung nach ihrem
   eigenen Import veraltet.

   `--no-link` überspringt den Schritt. Eine Lieferung, die unverändert
   liegenbleiben soll, kommt so an.
10. Bundle-Notiz nach §5.1 als `<base>/bundles/<id>.md` anlegen oder
   aktualisieren: `version` und `imported` auf die eben übernommene Fassung
   setzen und den Importnachweis `# Import <version>` mit allen Notizen und
   Mediendateien voranstellen, dazu die angelegten Verweise samt Gegenstelle
   und Grund. Ist die Fassung schon nachgewiesen, bleibt ihr Abschnitt
   unverändert. Anschließend die Typtabelle in `hkb.md` neu erzeugen.

Der Vorgang ist wiederholbar: dieselbe `id` mit derselben `version` erzeugt
keine zusätzlichen Notizen. Das Ergebnis nennt die Zahl der angelegten,
aktualisierten, übersprungenen und fehlerhaften Notizen.

### `--check`

`hk-import --check <bundle-pfad>` führt den Import bis zu dem Punkt aus, an
dem er schreiben würde, und schreibt nichts. Er beantwortet drei Fragen, und
in dieser Reihenfolge wird berichtet.

**Was geschieht.** Wie viele Notizen neu angelegt, aktualisiert, übersprungen
oder abgelehnt würden; welche Typen angelegt und welche nur vorläufig angelegt
würden, jeweils mit Verzeichnis; welche Mediendateien hinzukämen.

**Was zu entscheiden ist.** Jede fällige Bedeutungsprüfung (§5.6), jeder
vorgelegte Verknüpfungskandidat (§5.7) und jeder Konflikt aus Schritt 3 —
abweichendes `dir`, widersprüchliche Zeile in einer Property-Tabelle,
abweichender Property-Typ, belegtes vorläufiges Verzeichnis, Mediendatei mit
gleichem Pfad und anderem Inhalt. Jeder Eintrag nennt **beide
Seiten**, damit er ohne Nachschlagen zu beurteilen ist.

**Was zu tun ist.** Zu jedem Befund ein Satz in der Befehlsform, der den
nächsten Schritt nennt. Das ist der eigentliche Zweck des Modus: Ein Befund,
der nur eine Lage beschreibt, lässt den Benutzer mit ihr allein.

```text
hk-import --check biografie-2026/

Was geschieht
  14 Notizen: 12 neu, 1 aktualisiert, 1 abgelehnt (ältere Fassung)
  2 Mediendateien neu
  Typ angelegt:  quelle → quellen
  Vorläufig:     werkstoff → werkstoffs (3 Notizen)
  Verknüpfung:   7 Verweise mechanisch sicher, 4 vorgelegt

Was zu entscheiden ist
  person   Gleicher Name, Bedeutung nicht zugesichert.
           hier    Ein Mensch als Gegenstand der Wissensbasis. (eigene Definition)
           Bundle  Datensatz der Personalverwaltung. (typedefs/person.md)
  place    dir weicht ab: orte (Bundle) gegen places (hier).

Was zu tun ist
  → Bedeutungsprüfung für person entscheiden. Bei „verschieden" einen der
    beiden Typen umbenennen und den Import wiederholen.
  → Für place entscheiden, welches Verzeichnis gilt. Ein Umzug zieht alle
    Verweise mit.
  → hkf-base >= 1.0 ist vorausgesetzt, aber nicht importiert. Erst hkf-base
    importieren, dann diesen Import wiederholen; werkstoff bleibt bis dahin
    vorläufig.
  → persons/ada-lovelace ist hier neuer als in der Lieferung. Prüfen, ob die
    Lieferung veraltet ist; sonst nichts tun.
  → 4 Verknüpfungen entscheiden, darunter employer an zwei Personen. Was
    nicht gewollt ist, gehört nach rejected_links, sonst kommt es beim
    nächsten Import wieder.

Nichts wurde geschrieben.
```

Der Abschnitt „Was geschieht" rechnet damit, dass jede offene Entscheidung auf
Übernahme fällt. Er sagt also, was höchstens geschähe — fällt eine
Bedeutungsprüfung auf „verschieden", geschieht gar nichts (Schritt 2).

Ein Import ohne `--check` gibt dieselben drei Abschnitte aus, bezogen auf das,
was tatsächlich geschehen ist. Der Modus ändert nicht, was geprüft wird,
sondern nur, ob geschrieben wird.

## 6.2 `hk-export <bundle-id> <zielpfad>`

Schreibt ein HKF-Bundle heraus.

1. Alle Notizen sammeln, deren `bundles` auf `<base>/bundles/<bundle-id>`
   verweist.
2. Jede Notiz nach `<zielpfad>/<dir des typs>/<dateiname>` schreiben, die
   Properties `bundles` und `rejected_links` dabei entfernen (§4.2). Beide
   beschreiben, wie **diese** Wissensbasis die Lieferung einsortiert und
   beurteilt hat; beim Empfänger bezeichnen sie nichts.
3. Die Typdefinitionen und Property-Typen mitschreiben, die von diesen
   Notizen verwendet werden; die Standard-Property-Typen aus §3.5.1 dürfen
   entfallen. Eine vorläufige Typdefinition (§5.5) wird **nicht**
   mitgeschrieben, sondern gemeldet: Das Bundle ist in seinen Typen dann nicht
   geschlossen und braucht die richtige Typdefinition, bevor es weitergegeben
   wird.
4. Jede Mediendatei mitschreiben, auf die diese Notizen verweisen — aus dem
   `media_base` der HKB in den `media_base` des Bundles, unter derselben
   Medienart und demselben Pfad darunter.
5. Wikilinks anpassen: bei Notizen den Präfix der HKB aus Ablagepfad und
   `base` entfernen, bei Mediendateien Ablagepfad und `media_base` der HKB
   durch den `media_base` des Bundles ersetzen.
6. Die Bundle-Notiz nach §4.1 als `<zielpfad>/hbundle.md` schreiben, mit
   `hkf`, `base: ""`, dem gewählten `media_base` und frisch erzeugter
   Typtabelle. `imported` und die Importnachweise entfallen — sie beschreiben
   die Geschichte der abgebenden HKB, nicht die Lieferung.
7. Aus jedem Abschnitt `# Siehe auch` die Einträge entfernen, die aus dem
   Bundle hinausweisen (§5.7). Sie zeigten beim Empfänger ins Leere, und der
   Abschnitt ist maschinell gepflegt — was hier wegfällt, entsteht dort beim
   Import neu. Bleibt kein Eintrag übrig, entfällt der Abschnitt.
8. Wikilinks im übrigen Body und in Properties, die auf Notizen außerhalb des
   Bundles zeigen, melden. Sie bleiben unverändert erhalten — das Bundle ist
   dann in seinen Typen, aber nicht in allen Verweisen geschlossen.

Der Export gibt den aktuellen Stand wieder. Ein bytegleicher historischer
Stand erfordert ein Archiv der jeweiligen Fassung.

**Der Rundlauf ist damit nicht mehr buchstäblich.** Ein Bundle, das importiert
und sofort wieder exportiert wird, kommt nicht byte-gleich zurück: Verweise
zwischen zwei Notizen **derselben** Lieferung überstehen Schritt 7 und stehen
im Ergebnis unter `# Siehe auch`. Das ist gewollt — der Import hat etwas
erkannt, was in der Lieferung nicht stand, und ein Export, der es wieder
wegwürfe, verlöre Arbeit. Verweise in den Bestand hinein fallen dagegen weg,
denn sie gelten nur hier.

## 6.3 `hk-lint [--fix]`

Prüft eine Ablage, ohne sie zu verändern. Anwendbar auf eine HKB und auf ein
Bundle; die letzten vier Punkte gelten nur für eine HKB.

- Wurzeldatei vorhanden, `hkf` gesetzt, `base` und `media_base` auflösbar,
- `typedefs`, `proptypes` und `bundles` im Basispfad vorhanden,
- jede Notiz hat `type`, und der Typ passt zu ihrem Verzeichnis,
- jeder `type` hat genau eine Typdefinition; `dir`-Werte sind wohlgeformte
  relative Pfade, eindeutig und nicht ineinander verschachtelt,
- jede vorläufige Typdefinition ist ein Hinweis, kein Fehler; die Meldung
  nennt ihr Verzeichnis und die Zahl der Notizen darin (§5.5),
- `provisional` steht nur an einer Typdefinition und nur mit dem Wert `true`;
  eine vorläufige Typdefinition trägt weder einen Abschnitt `# Properties`
  noch `bundles`,
- Dateinamen innerhalb eines Typverzeichnisses eindeutig,
- alle Frontmatter-Werte entsprechen §3.4, keine verschachtelten Werte,
- jeder Property-Typ hat eine gültige `form`; kein Property-Typ für eine
  native Wertform; kein eigener Property-Typ endet auf `-list`; die
  Standard-Property-Typen entsprechen §3.5.1,
- jede in einer Property-Tabelle aufgeführte Property erfüllt ihren Typ:
  Wertform, `pattern`, `values`, `min`, `max`, und bei `hkf-link` und
  `hkf-file` Zieltyp beziehungsweise Medienart nach §3.7.1; bei mehreren
  Alternativen genügt eine (§3.7.2),
- alle Alternativen einer Typ-Angabe haben dieselbe Wertform,
- jede als Pflicht markierte Property ist vorhanden,
- jeder in einer Property-Tabelle genannte Typ existiert als Wertform, als
  Property-Typ oder als dessen Listenform nach §3.5.2, jeder genannte Zieltyp
  ist registriert, und der `:`-Zusatz steht nur an `hkf-link` oder
  `hkf-link-list`,
- alle internen Verweise sind qualifizierte Wikilinks nach §3.6 und auflösbar;
  in der Wurzeldatei ohne Ablagepfad, in Notizen mit,
- interne Verweise tragen einen Alias — fehlt er, ist das ein Hinweis, kein
  Fehler (§3.6),
- `modified` liegt nicht vor `created`,
- in einer HKB trägt jede Notiz `created` und `modified` — fehlt eines, ist
  das ein Hinweis, kein Fehler,
- unmittelbar unter `media_base` liegen nur `images`, `videos`, `audios` und
  `documents`; kein Typverzeichnis liegt unter `media_base`,
- jeder `hkf-file`-Wert zeigt auf eine vorhandene Datei in einem
  Medienverzeichnis, trägt eine Dateiendung, endet nicht auf `.md` und
  erfüllt die geforderte Medienart,
- die Typtabelle der Wurzeldatei stimmt mit den Typdefinitionen überein,
- alle Standard-Property-Typen aus §3.5.1 sind vorhanden,
- jede Bundle-Notiz hat eine `id` gleich ihrem Dateinamen, in der Form aus
  §4.1, dazu eine `version` und eine `description`,
- jeder Eintrag in `required_bundles` hat die Form aus §4.1, setzt nicht das
  eigene Bundle voraus und bildet keinen Kreis; eine Fassungsbedingung steht
  nur an einer Fassung der Form `Zahl.Zahl`,
- jeder Importnachweis hat die Form aus §5.1; ein Eintrag ohne vorhandenes
  Ziel ist ein Hinweis, kein Fehler,
- jeder Wikilink in `bundles` zeigt auf eine vorhandene Bundle-Notiz,
- keine zwei Notizen tragen denselben Wert in einer Property vom Typ
  `hkf-wikidata` — sie bezeichnen dann denselben Gegenstand und sind ein
  Zusammenführungskandidat; das ist ein Hinweis, kein Fehler,
- jeder Abschnitt `# Siehe auch` hat die Form aus §5.7: ein Listenpunkt je
  Zeile aus qualifiziertem Wikilink, ` — ` und einem Grund. Ein fehlender
  Grund ist ein Fehler; eine gestörte alphabetische Ordnung und ein Abschnitt,
  der nicht der letzte ist, sind Hinweise,
- kein Ziel steht zugleich unter `# Siehe auch` und in `rejected_links` —
  das ist ein Fehler, weil beide einander widersprechen,
- jeder Eintrag unter `# Siehe auch` hat einen Gegeneintrag in der Zielnotiz;
  fehlt er, ist das ein Hinweis (§5.7),
- eine Notiz, auf die kein einziger Verweis zeigt, ist ein Hinweis: Sie ist
  über die Wissensbasis nicht erreichbar,
- keine Notiz trägt `bundles` oder `rejected_links` mit leerer Liste.

Jeder Befund nennt Datei, Zeile soweit bestimmbar, Schweregrad und eine
verständliche Meldung.

`--fix` darf ausschließlich:

- die Typtabelle der Wurzeldatei neu erzeugen,
- fehlende Standard-Property-Typen anlegen,
- einen verzeichnislosen Wikilink auf eine Notiz in einem Typverzeichnis
  qualifizieren, **wenn genau ein Ziel existiert**,
- einen fehlenden Alias aus dem `title` des Ziels ergänzen,
- die Leerzeichen um einen Alternativen-Trenner ` / ` ergänzen,
- einen `datetime`-Wert ohne Uhrzeit auf den Tagesbeginn ausschreiben,
- fehlendes `created` und `modified` in einer HKB ergänzen; `modified_by`
  bleibt dabei leer, weil der Linter nicht weiß, wer geändert hat,
- die Einträge eines Abschnitts `# Siehe auch` alphabetisch ordnen und den
  Abschnitt ans Ende der Notiz stellen,
- leere Properties und `null`-Werte entfernen.

Bei mehrdeutigen oder unbekannten Zielen wird nicht geraten. Nach einem
Korrekturlauf wird erneut geprüft.

`--fix` ergänzt keinen Eintrag unter `# Siehe auch` und entfernt keinen. Es
ordnet nur, was dasteht: Verknüpfen ist Sache des Imports (§6.1 Schritt 9),
Entfernen Sache eines Menschen (§5.7).

`--fix` legt keine vorläufige Typdefinition an und entfernt keine. Sie
entsteht beim Import, und sie vergeht, wenn die richtige Typdefinition
nachgeliefert wird (§5.5); dazwischen liegt eine Entscheidung über Bedeutung,
und die trifft kein Linter.

### `--strict`

`hk-lint --strict` meldet zusätzlich **undeklarierte Properties**: jede
Property einer Notiz, die weder in der Property-Tabelle ihres Typs steht noch
zu den notizübergreifenden Properties gehört (Anhang A.2).

Diese Befunde sind **Hinweise, keine Fehler**. Sie ändern nichts an §3.3:
zusätzliche flache Properties bleiben zulässig, und eine Notiz wird davon
nicht unkonform. Der Modus macht nur sichtbar, was die Property-Tabelle nicht
abdeckt — sonst bliebe es unbemerkt, etwa ein versehentlich im Editor
gesetztes `country` an einer `person`.

Die Ausgabe wird **je Typ und Property-Name zusammengefasst**, mit der Zahl
der betroffenen Notizen:

```text
person: country in 1 von 2 Notizen
source: isbn_alt in 4 von 4 Notizen
```

Diese Zusammenfassung trennt die beiden Fälle, die hinter einer undeklarierten
Property stecken können:

- **Wenige Notizen** — meist ein Versehen. Die Property gehört entfernt.
- **Fast alle Notizen eines Typs** — die Property hat sich eingebürgert und
  gehört in die Property-Tabelle des Typs.

`--strict` verändert nichts. `--fix` legt keine Tabellenzeilen an; welcher der
beiden Fälle vorliegt, entscheidet ein Mensch.

---

# 7. Konformität

## 7.1 Ein HKF-Bundle ist konform, wenn

1. `hbundle.md` in seiner Wurzel liegt und §4.1 erfüllt, einschließlich `id`,
   `version` und `description`,
2. `base` leer ist,
3. `typedefs` und `proptypes` jede verwendete Typdefinition und jeden
   verwendeten Property-Typ enthalten, die nicht zur Grundausstattung aus
   §3.8 gehören — ein leeres Verzeichnis darf fehlen —, und
   die Medienverzeichnisse jede referenzierte Mediendatei enthalten,
4. jede Notiz `type` trägt und im passenden Typverzeichnis liegt,
5. alle Frontmatter-Werte den Wertformen aus §3.4 entsprechen und die
   Property-Tabellen ihrer Typen erfüllen,
6. alle internen Verweise qualifizierte Wikilinks nach §3.6 sind,
7. kein Standard-Property-Typ umdefiniert wird,
8. keine Notiz die Property `bundles` oder `rejected_links` trägt,
9. `hbundle.md` keinen Importnachweis enthält,
10. jeder Eintrag in `required_bundles` §4.1 erfüllt, und
11. keine Typdefinition `provisional: true` trägt (§5.5).

## 7.2 Eine HKB ist konform, wenn

1. `hkb.md` mit `hkf: "1.0"` und `name` im Wurzelverzeichnis der HKB liegt
   und keine weitere Ablage darunter liegt,
2. `typedefs`, `proptypes` und `bundles` im Basispfad existieren, soweit sie
   nicht leer wären, und unter `media_base` nur die vier Medienverzeichnisse
   aus §3.2.1 liegen,
3. die Grundausstattung aus §3.8 vorhanden ist — die Kern-Typen `typedef`,
   `proptype` und `bundle` sowie die zwölf Property-Typen aus §3.5.1,
4. jeder geführte Typ aus HKF Base dessen Fassung entspricht,
5. jede Notiz `type` trägt und im passenden Typverzeichnis liegt,
6. alle Frontmatter-Werte den Wertformen aus §3.4 entsprechen und die
   Property-Tabellen ihrer Typen erfüllen,
7. alle internen Verweise qualifizierte Wikilinks nach §3.6 sind, jeder
   `hkf-file`-Wert auf eine vorhandene Mediendatei der geforderten Art zeigt
   und jeder Abschnitt `# Siehe auch` §5.7 erfüllt,
8. jede Bundle-Notiz §5.1 samt Importnachweis erfüllt und jeder
   `bundles`-Eintrag auflösbar ist,
   und
9. `hk-import`, `hk-export` und `hk-lint` verfügbar sind.

Unbekannte zusätzliche Properties und freie Markdown-Struktur machen eine
Notiz nicht ungültig. Vorläufige Typdefinitionen machen eine HKB nicht
unkonform: Der Typ ist registriert, seine Notizen liegen am richtigen Ort und
seine Verweise sind prüfbar — ungeklärt ist allein die Bedeutung (§5.5). Ein
Bundle darf eine solche Typdefinition dagegen nicht enthalten (§7.1).

---

# 8. Versionierung

Diese Fassung ist **HKF Core 1.0**. Minor-Versionen ergänzen Regeln, ohne
bestehende Bundles oder HKBs ungültig zu machen. Eine Major-Version darf
Identität, Wertformen, die Standard-Property-Typen oder die Ablagestruktur
ändern.

**Core und Base werden getrennt fortgeschrieben.** Die Property `hkf` in der
Wurzeldatei nennt die Fassung von Core und sonst nichts. Welche Fassung des
Vokabulars eine Wissensbasis führt, steht in der `version` der zugehörigen
Bundle-Notiz — dort, wo jede andere Lieferung auch verbucht wird. Base darf
damit Typen und Werte ergänzen, ohne dass Core eine neue Nummer bekommt; und
Core darf sich ändern, ohne dass jede Wissensbasis ihr Vokabular neu lädt.
Base 1.0 setzt Core 1.0 voraus.

Erkennt eine HKB die `hkf`-Version eines Bundles nicht, liest sie die Dateien,
leitet aber keine Identitäten ab und importiert nicht.

---

# Anhang A — Kern-Typen und allgemeine Properties

Dieser Anhang beantwortet abschließend, welche Properties wo erlaubt sind: in
den Wurzeldateien, in jeder Notiz unabhängig vom Typ, und in den drei
Kern-Typen aus §3.8.

## A.1 Wurzeldateien

`hkb.md` und `hbundle.md` sind keine Notizen (§3.1). Sie tragen ausschließlich
diese Properties:

| Property | Typ | `hkb.md` | `hbundle.md` | Beschreibung |
|---|---|---|---|---|
| `hkf` | text | Pflicht | Pflicht | Formatversion, in dieser Fassung `"1.0"` |
| `name` | text | Pflicht | — | Anzeigename der HKB |
| `base` | text | optional | optional, immer leer | Basispfad der Typverzeichnisse |
| `media_base` | text | optional | optional | Basispfad der Medienverzeichnisse |
| `timezone` | text | optional | optional | IANA-Zonenname für Zeiten ohne Versatz |
| `spec` | text | optional | optional | Wo die geltende Spezifikation steht |

`spec` sagt, **wo** die Spezifikation zu lesen ist; `hkf` sagt, **welche
Fassung** von Core gilt. Der Wert ist entweder ein Wikilink auf eine Notiz vom Typ
`specification` oder eine URL — dieselbe Alternative wie in §3.7.2, beide
Formen sind `text`. Als Wikilink verweist er nach §3.6 relativ zur
Wurzeldatei, also ohne Ablagepfad:

```yaml
spec: "[[specifications/hkf-core-1.0|HKF Core 1.0]]"
spec: https://example.org/hkf/1.0
```

Die Wikilink-Form setzt voraus, dass die Wissensbasis den Typ `specification`
führt — er kommt aus HKF Base oder wird selbst definiert. Eine Wissensbasis,
die nur Core erfüllt, kennt ihn nicht und schreibt eine URL.

`hbundle.md` ist zugleich die Bundle-Notiz und trägt darum zusätzlich alle
Properties des Typs `bundle` aus A.5.

Der Body beider Dateien enthält den Abschnitt `# Typen` (§3.1).

## A.2 Notizübergreifende Properties

Diese Properties sind in **jeder** Notiz erlaubt, gleich welchen Typs. Sie
brauchen keinen Eintrag in einer Property-Tabelle.

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `type` | text | ja | Typ der Notiz; MUSS zum Verzeichnis passen (§3.2) |
| `title` | text | nein | Anzeigetitel; ohne ihn gilt der Dateiname |
| `description` | text | nein | Einzeiler zum Inhalt |
| `tags` | list | nein | Obsidian-eigen |
| `aliases` | list | nein | Obsidian-eigen; auch für Synonyme |
| `cssclasses` | list | nein | Obsidian-eigen |
| `status` | text | nein | Bearbeitungsstand |
| `created` | date | nein | Tag der Entstehung |
| `modified` | datetime | nein | Zeitpunkt der letzten Änderung |
| `modified_by` | text | nein | Wer zuletzt geändert hat |
| `bundles` | hkf-link-list:bundle | nein | Zugehörigkeit; nur in einer HKB (§5.2) |
| `rejected_links` | hkf-link-list | nein | Ziele, die nicht selbsttätig verlinkt werden; nur in einer HKB (§5.7) |

### Die drei Zeitangaben

`created` ist ein Tag, `modified` ein Zeitpunkt. Die Asymmetrie ist gewollt:
Für die Entstehung genügt der Tag, für die Reihenfolge zweier Fassungen nicht.
Ein `modified` ohne Uhrzeit bezeichnet den Tagesbeginn (§3.4).

`modified_by` nennt, wer die Notiz zuletzt geändert hat. **Ein Sprachmodell
MUSS dort seinen Modellnamen eintragen**, etwa `claude-opus-5`; ein Werkzeug
seinen eigenen Namen, etwa `hk-import`. Bei einer Änderung von Hand bleibt das
Feld dem Menschen überlassen — Obsidian setzt es nicht, und `hk-lint` kann es
nicht nachprüfen. Der Wert ist deshalb keine Zusicherung über den letzten
Bearbeiter, sondern eine Selbstauskunft der Maschinen: Er sagt verlässlich,
*dass* eine Maschine zuletzt geschrieben hat, und welche.

In einem Bundle sind alle drei freigestellt (§4). In einer HKB werden sie
geführt: Fehlt eines beim Import oder beim Anlegen, wird es gesetzt (§6.1);
`hk-lint` meldet ein fehlendes als Hinweis und `--fix` ergänzt es.

Die Property-Tabelle eines Typs darf eine dieser Properties **verschärfen**,
also als Pflicht führen — so verlangt `bundle` eine `description` (A.5). Was
hier steht, ist die Vorgabe, nicht die Obergrenze.

Darüber hinaus darf jede Notiz weitere flache Properties tragen; sie werden
nicht geprüft und müssen erhalten bleiben (§3.3). `hk-lint --strict` listet
sie als Hinweis auf (§6.3). Wer `status` auf feste Werte
festlegen will, definiert dafür einen eigenen Property-Typ mit `values` — HKF
schreibt keine vor, weil die Werte sich je Wissensbasis unterscheiden.

## A.3 `typedef`

```markdown
---
type: typedef
title: Typdefinition
description: Registriert einen Typ und legt sein Verzeichnis fest.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| description | text | ja | Einzeiliger Zweck; erscheint in der Typtabelle der Wurzeldatei |
| dir | text | nein | Verzeichnis der Instanzen; Vorgabe ist der Typname mit angehängtem `s` |
| provisional | checkbox | nein | Beim Import angelegt, weil niemand den Typ definiert hat (§5.5) |

# Konventionen

Der Dateiname ist der Typname (§3.7). Der Body trägt die Property-Tabelle und
die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit
`/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und
abschließenden `/` und ohne `.`- oder `..`-Abschnitte; er darf nicht unter
`media_base` liegen.

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB — ein Bundle enthält keine vorläufige Typdefinition (§7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.
```

## A.4 `proptype`

```markdown
---
type: typedef
title: Property-Typ
description: Schränkt eine Wertform ein.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| form | text | ja | Eine der sechs Wertformen aus §3.4 |
| pattern | text | nein | Regulärer Ausdruck; nur bei `text` und `list`, dort je Eintrag |
| values | list | nein | Erlaubte Werte; als Text geführt, auch wenn sie wie Zahlen aussehen |
| unit | text | nein | Maßeinheit; beschreibend, nicht geprüft |
| min | number | nein | Kleinster zulässiger Wert; nur bei `form: number` |
| max | number | nein | Größter zulässiger Wert; nur bei `form: number` |

# Konventionen

Der Dateiname ist der Name des Property-Typs (§3.5) und endet nicht auf
`-list`. Für eine der sechs Wertformen wird kein Property-Typ angelegt. `min`
und `max` gibt es nur für Zahlen: Obsidian ordnet einem Property-Namen genau
eine Wertform zu, sie könnten also nicht zugleich Datumsgrenzen sein.
```

Die Tabelle beschreibt die Properties **einer** `proptype`-Notiz. Die
Typdefinition selbst liegt als `typedefs/proptype.md` und trägt wie jede
Typdefinition `type: typedef`.

## A.5 `bundle`

```markdown
---
type: typedef
title: Bundle
description: Beschreibt eine Lieferung.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| id | text | ja | Kennung der Lieferreihe in `kebab-case` (§4.1); in der HKB gleich dem Dateinamen |
| version | text | ja | Unveränderliche Kennung der gelieferten Fassung |
| description | text | ja | Ein Satz darüber, was die Lieferung enthält |
| required_bundles | list | nein | Bundles, die vorher importiert sein sollen (§4.1) |
| source | text | nein | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | Zeitpunkt der Übernahme; nur in der HKB (§5.1) |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die
Wurzeldatei-Properties aus A.1 und die Typtabelle im Body; `imported` entfällt
dort. In der HKB liegt sie als `bundles/<id>.md` ohne diese Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder
ein Datenträger als Herkunft in Frage kommt.

`description` ist bei einer Bundle-Notiz **Pflicht**, obwohl sie nach A.2 sonst
freigestellt ist: Wer eine Lieferung vor sich hat, muss ohne sie den Body lesen
oder die Dateien zählen, um zu erfahren, worum es geht. Sie ist zudem die
einzige Angabe, die in der Bundle-Liste einer Wissensbasis abfragbar ist.
```
