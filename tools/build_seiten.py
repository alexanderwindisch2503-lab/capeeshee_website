#!/usr/bin/env python3
"""Erzeugt Unterseiten aus der Startseite site/index.html, damit Kopf, Navigation, Footer,
Schriften und Stile überall identisch sind.

  site/referenzen/index.html   Referenzen mit Galerie und Filtern

Aufruf: python3 tools/build_seiten.py   (läuft auch automatisch beim Veröffentlichen)
"""
import os, re

HIER = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HIER, '..', 'site')

REFERENZEN = '''
  <section id="referenzen" class="alt rg-page">
    <div class="wrap">
      <p class="eyebrow">Referenzen</p>
      <h1 class="rg-title">Nutzen Sie unser Know-how.</h1>
      <div class="rg" id="rg" hidden>
        <p class="lead rg-lead">Finden Sie Beispiele nach Leistung, nach Branche oder direkt nach Kunde. Viele Kunden begleiten wir seit Jahren, vom Logo bis zum Leitsystem.</p>
        <div class="rg-main" id="rgMain">
          <div class="rg-modes" role="group" aria-label="Referenzen anzeigen nach">
            <button type="button" class="rg-mode" data-mode="projekte" aria-pressed="true">Projekte</button>
            <button type="button" class="rg-mode" data-mode="leistung" aria-pressed="false">Nach Leistung</button>
            <button type="button" class="rg-mode" data-mode="branche" aria-pressed="false">Nach Branche</button>
          </div>
          <div class="rg-chips" id="rgChips"></div>
          <p class="rg-count" id="rgCount" aria-live="polite"></p>
          <div id="rgOut"></div>
        </div>
        <div class="rg-detail" id="rgDetail" hidden></div>
      </div>
      <p class="rg-leer" id="rgLeer">Die Referenzen werden gerade geladen.</p>
    </div>
  </section>
'''


def seite(start, titel, beschreibung, inhalt, aktiv):
    s = start
    # alle relativen Links und Dateien auf die Wurzel beziehen, Anker führen zur Startseite
    s = s.replace('<head>', '<head>\n<base href="/">', 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{titel}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + beschreibung, s, count=1)
    # Hauptinhalt ersetzen: alles in <main> bis auf den Kontaktbereich
    a = s.index('<main id="top">') + len('<main id="top">')
    k = s.index('<section id="kontakt"')
    s = s[:a] + '\n' + inhalt + '\n  ' + s[k:]
    s = s.replace(f'href="{aktiv}"', f'href="{aktiv}" aria-current="page"')
    return s


def main():
    with open(os.path.join(SITE, 'index.html'), encoding='utf-8') as f:
        start = f.read()
    ziel = os.path.join(SITE, 'referenzen', 'index.html')
    html = seite(start,
                 'Referenzen | Agentur Capeeshee, Werbeagentur in Augsburg',
                 'Arbeiten aus 25 Jahren Agentur Capeeshee: Corporate Design, Logos, Broschüren, Websites, Leitsysteme und Kampagnen für den Mittelstand.',
                 REFERENZEN, '/referenzen/')
    html = '<!-- Automatisch erzeugt aus index.html durch tools/build_seiten.py. Bitte nicht direkt bearbeiten. -->\n' + html
    with open(ziel, 'w', encoding='utf-8') as f:
        f.write(html)
    print('erzeugt:', os.path.relpath(ziel, SITE))


if __name__ == '__main__':
    main()
