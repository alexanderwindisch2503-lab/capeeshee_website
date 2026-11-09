# Ausgeblendete Blöcke auf capeeshee.com

Alle Blöcke sind nur mit dem Attribut `hidden` ausgeblendet und stehen weiter in `site/index.html`.
Zum Zurückholen in der genannten Zeile `hidden` entfernen (bzw. den Wrapper löschen) und veröffentlichen.
Jeder Block ist im Code mit einem Kommentar `<!-- Block „…“ vorübergehend ausgeblendet -->` markiert.

| Block | Wo im Code | Grund |
|---|---|---|
| Hero mit Enten-Video | `<section class="hero" hidden …>` (Sicherung zusätzlich im Branch `hero-enten`) | ersetzt durch Tennis-Hero |
| Unsere Botschaft | `<section id="botschaft" … hidden>` | vorübergehend ausgeblendet |
| Leistungs-Säulen (Was möchten Sie kommunizieren?, Der erste Eindruck zählt, Web Development) | `<div class="pillars" hidden>` in `#leistungen` | stand vor den Leistungskacheln im Niemandsland |
| Wir kennen die ganze Kette (Sportkind, Setima) | `<section id="kette" hidden>` | Bilder fehlen noch |

Entfernt, aber in der Git-Historie abrufbar:
- Früherer Block „Über Capeeshee“ (Klasse `nk`) vor dem Umbau am 9. November 2026, ersetzt durch den neuen Abschnitt `.ub`.

Als „Coming soon“ markiert (sichtbar):
- Capeeshee-Check „Wie gut ist Ihr Marketing in Form?“
- „Mehr Referenzen coming soon“ unter den Referenzen
