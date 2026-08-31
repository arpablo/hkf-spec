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
| [`HKF-Config-V1.0.md`](HKF-Config-V1.0.md) | Alle Typdefinitionen und Property-Typen |
| [`schema/hkf-core-1.0.schema.json`](schema/hkf-core-1.0.schema.json) | Das Frontmatter als JSON Schema, normativ (Core Anhang B.4) |

**Core** beschreibt Verzeichnisse, Wertformen, Verweise, Typdefinitionen als
Bauform, das Bundle-Format und die drei Methoden `hk-import`, `hk-export` und
`hk-lint`. Es nennt keine einzige konkrete Definition.

**Config** ist das Inventar: siebzehn Typdefinitionen und fünfzehn
Property-Typen. Drei Typen und dreizehn Property-Typen bilden die
Grundausstattung: Jede Ablage bekommt sie beim Anlegen, geliefert wird davon
nichts.

Der Schnitt liegt zwischen **Mechanik und Inventar**. Dass eine Notiz im
Verzeichnis ihres Typs liegt, sagt Core. Welche Typen es gibt, sagt Config.
Dass eine Person `born` und `died` trägt, ist dabei eine Verabredung, die man
auch anders treffen kann — eine Wissensbasis über Werkstoffe oder Wertpapiere
kommt ohne sie aus und führt nur die Grundausstattung.

Beide Fassungen werden **getrennt fortgeschrieben**. Die Property `hkf` in der
Wurzeldatei einer Ablage nennt die Fassung von Core, `spec` das Dokument, dem
sie folgt. Config 1.0 setzt Core 1.0 voraus.

## Wo der Rest liegt

Dieses Repository enthält nur die Spezifikation — keine Ablage, kein Bundle,
keine Wissensbasis, kein Werkzeug.

| Repository | Inhalt |
|---|---|
| [`hkf-kb-template`](https://github.com/arpablo/hkf-kb-template) | Vorlage für eine neue Wissensbasis: die Grundausstattung, sonst nichts. „Use this template" erzeugt daraus ein eigenes Repository. |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Eine Umsetzung der drei Methoden aus §6 |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Eine Umsetzung der drei Methoden aus §6: `hk-init`, `hk-import`, `hk-export`, `hk-lint` |

## Prüfung

Das Inventar steht zweimal: als Markdown-Block in `HKF-Config-V1.0.md` und als
ausgelieferte Datei in der Vorlage `hkf-kb-template`. Die Spezifikation ist
die normative Fassung.

```
python3 tools/grundausstattung.py
```

Das Skript liegt im [`hkf-harness`](https://github.com/arpablo/hkf-harness),
weil es die Vorlage prüft, die dort entsteht. Es vergleicht beide Fassungen
Zeile für Zeile und meldet jede Abweichung. Wer die Spezifikation ändert,
führt es aus, bevor er die Vorlage für unverändert hält.
