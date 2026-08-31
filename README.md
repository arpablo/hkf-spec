# Henni Knowledge Format — Spezifikation

Das **HKF** beschreibt zwei Dinge: ein übertragbares **Bundle-Format** für
Notizen samt ihrer Typdefinitionen, und eine **Knowledge Base** als
Obsidian-Vault, der solche Bundles importiert und wieder exportiert. Beide
teilen denselben Kern — typbezogene Ablage, native Obsidian-Properties,
qualifizierte Wikilinks.

HKF ist kein Ontologiesystem. Ein Typ ist ein Verzeichnis mit einer
Beschreibung.

Die Struktur ist darauf ausgelegt, dass ein Sprachmodell eine Wissensbasis mit
möglichst wenig Kontext benutzen kann: Eine einzige Datei nennt alle Typen samt
Verzeichnis, eine weitere den vollständigen Vertrag eines Typs.

## Die beiden Dokumente

| | |
|---|---|
| [`HKF-Core-V1.0.md`](HKF-Core-V1.0.md) | Wie eine Ablage aufgebaut ist |
| [`HKF-Base-V1.0.md`](HKF-Base-V1.0.md) | Das Standardvokabular |
| [`schema/hkf-core-1.0.schema.json`](schema/hkf-core-1.0.schema.json) | Das Frontmatter als JSON Schema, normativ (Core Anhang B.4) |

**Core** beschreibt Verzeichnisse, Wertformen, Property-Typen, Verweise,
Typdefinitionen, das Bundle-Format und die drei Methoden `hk-import`,
`hk-export` und `hk-lint`. Es nennt keinen einzigen inhaltlichen Typ. Konform
ist eine Wissensbasis nach Core.

**Base** ist das Vokabular: zwölf Typdefinitionen für Person, Körperschaft,
Ort, Ereignis, Quelle, Begriff, Konzept, Vergleich, Thema, Notiz,
Spezifikation und Hinweis, dazu zwei Aufzählungen. Es wird als Bundle `hkf-base` geliefert und ist freiwillig.

Der Schnitt liegt dort, wo die Beliebigkeit anfängt. Dass eine Notiz im
Verzeichnis ihres Typs liegt, gilt für jede Wissensbasis. Dass eine Person
`born` und `died` trägt, ist eine Verabredung, die man auch anders treffen
kann — eine Wissensbasis über Werkstoffe oder Wertpapiere kommt ohne sie aus.

Beide Fassungen werden **getrennt fortgeschrieben**. Die Property `hkf` in der
Wurzeldatei einer Ablage nennt die Fassung von Core; welche Fassung des
Vokabulars eine Wissensbasis führt, steht in der `version` ihrer Bundle-Notiz.
Base 1.0 setzt Core 1.0 voraus.

## Wo der Rest liegt

Dieses Repository enthält nur die Spezifikation — keine Ablage, kein Bundle,
keine Wissensbasis, kein Werkzeug.

| Repository | Inhalt |
|---|---|
| [`hkf-kb-template`](https://github.com/arpablo/hkf-kb-template) | Vorlage für eine neue Wissensbasis: die Grundausstattung, sonst nichts. „Use this template" erzeugt daraus ein eigenes Repository. |
| [`hkf-base`](https://github.com/arpablo/hkf-base) | Das Bundle `hkf-base` mit dem Vokabular aus §3 von HKF Base |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Eine Umsetzung der drei Methoden aus §6: `hk-init`, `hk-import`, `hk-export`, `hk-lint` |

## Prüfung

Die zwölf Typdefinitionen stehen zweimal: als Markdown-Block in
`HKF-Base-V1.0.md` §3 und als ausgelieferte Datei im Bundle. Die
Spezifikation ist die normative Fassung.

```
python3 tools/check-base.py
```

Das Skript vergleicht beide Fassungen Zeile für Zeile und meldet jede
Abweichung. Es erwartet das ausgecheckte Bundle als Geschwisterverzeichnis
`HenniHKF-Base`; ein anderer Pfad lässt sich als Argument übergeben. Wer die
Spezifikation ändert, führt es aus, bevor er das Bundle für unverändert hält.
