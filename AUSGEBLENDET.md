# Ausgeblendete Blöcke auf capeeshee.com

Alle Blöcke sind nur mit dem Attribut `hidden` ausgeblendet und stehen weiter in `site/index.html`.
Zum Zurückholen in der genannten Zeile `hidden` entfernen (bzw. den Wrapper löschen) und veröffentlichen.
Jeder Block ist im Code mit einem Kommentar `<!-- Block „…“ vorübergehend ausgeblendet -->` markiert.

| Block | Wo im Code | Grund |
|---|---|---|
| Hero mit Enten-Video | `<section class="hero" hidden …>` (Sicherung zusätzlich im Branch `hero-enten`) | ersetzt durch Tennis-Hero |
| Unsere Botschaft | `<section id="botschaft" … hidden>` | vorübergehend ausgeblendet |
| Leistungs-Säulen (Was möchten Sie kommunizieren?, Der erste Eindruck zählt, Web Development) | `<div class="pillars" hidden>` in `#leistungen` | stand vor den Leistungskacheln im Niemandsland |
| Marketing im Wandel (Kopfstand, One Way, …) | `<section id="new-marketing" hidden>`, Menüpunkt entfernt | doppelte Botschaft zu „Über Capeeshee“, Bildsprache |
| Arbeitsweise (5 Schritte) | `<section id="arbeitsweise-alt" hidden>`, Menüpunkt entfernt | ersetzt durch die Zeitlinie „So arbeiten wir“ im Abschnitt KI als Werkzeug (Anker #arbeitsweise zeigt jetzt dorthin) |
| Wir kennen die ganze Kette (Sportkind, Setima) | `<section id="kette" hidden>` | Bilder fehlen noch |

Entfernt, aber in der Git-Historie abrufbar:
- Früherer Block „Über Capeeshee“ (Klasse `nk`) vor dem Umbau am 9. November 2026, ersetzt durch den neuen Abschnitt `.ub`.

Als „Coming soon“ markiert (sichtbar):
- Capeeshee-Check „Wie gut ist Ihr Marketing in Form?“
- „Mehr Referenzen coming soon“ unter den Referenzen

## Seitenaufbau seit 9. November 2026

Hero · Zähler · Wer wir sind · Leistungen (mit Corporate Design und Einzelleistungen) · Print · KI als Werkzeug (KI-Box, Vorteile, Zeitlinie) · Philosophie · Branchen · Referenzen · Über uns · Check (coming soon) · Kontakt
