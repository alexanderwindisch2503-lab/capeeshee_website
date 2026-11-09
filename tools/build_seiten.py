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


IMPRESSUM = '''
  <section class="legal">
    <div class="wrap">
      <p class="eyebrow">Rechtliches</p>
      <h1>Impressum</h1>
      <h2>Angaben gemäß § 5 DDG</h2>
      <p>Agentur Capeeshee<br>Inhaber: Alexander Windisch<br>Stettenstraße 8<br>86150 Augsburg</p>
      <h2>Kontakt</h2>
      <p>Telefon: +49 (0)821 31 94 99 0<br>E-Mail: info@capeeshee.com<br>Web: www.capeeshee.com</p>
      <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
      <p>Alexander Windisch<br>Stettenstraße 8<br>86150 Augsburg</p>
      <h2>Verbraucherstreitbeilegung</h2>
      <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
      <h2>Haftung für Inhalte und Links</h2>
      <p>Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität können wir jedoch keine Gewähr übernehmen. Für Inhalte externer Websites, auf die wir verlinken, sind ausschließlich deren Betreiber verantwortlich. Werden uns Rechtsverletzungen bekannt, entfernen wir die betreffenden Inhalte oder Links umgehend.</p>
      <h2>Urheberrecht und Bildnachweis</h2>
      <p>Texte, Gestaltungen, Bilder und Videos auf dieser Website sind urheberrechtlich geschützt. Eine Verwendung außerhalb der Grenzen des Urheberrechts bedarf unserer schriftlichen Zustimmung. Die als KI-generiert gekennzeichneten Bilder und Videos wurden von Capeeshee erstellt. Die gezeigten Referenzarbeiten wurden für die jeweiligen Kunden entwickelt und werden mit deren Einverständnis gezeigt.</p>
      <p class="stand">Stand: November 2026</p>
    </div>
  </section>
'''

DATENSCHUTZ = '''
  <section class="legal">
    <div class="wrap">
      <p class="eyebrow">Rechtliches</p>
      <h1>Datenschutzerklärung</h1>
      <p>Der Schutz Ihrer persönlichen Daten ist uns wichtig. Diese Website ist bewusst datensparsam aufgebaut: Wir setzen keine Cookies, keine Analyse- oder Trackingdienste und keine Inhalte von Drittanbietern ein. Im Folgenden informieren wir Sie, welche Daten beim Besuch dieser Website verarbeitet werden.</p>

      <h2>1. Verantwortlicher</h2>
      <p>Agentur Capeeshee, Inhaber Alexander Windisch<br>Stettenstraße 8, 86150 Augsburg<br>Telefon: +49 (0)821 31 94 99 0<br>E-Mail: info@capeeshee.com</p>

      <h2>2. Hosting und Server-Logfiles</h2>
      <p>Diese Website wird bei der STRATO GmbH, Otto-Ostrowski-Straße 7, 10249 Berlin, gehostet. Mit STRATO besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO. Die Server stehen in Deutschland.</p>
      <p>Beim Aufruf der Website übermittelt Ihr Browser automatisch Informationen, die in sogenannten Server-Logfiles gespeichert werden:</p>
      <ul><li>IP-Adresse</li><li>Datum und Uhrzeit des Zugriffs</li><li>aufgerufene Seite oder Datei</li><li>übertragene Datenmenge und Statusmeldung</li><li>zuvor besuchte Seite (Referrer)</li><li>Browser und Betriebssystem</li></ul>
      <p>Diese Daten sind technisch erforderlich, um die Website auszuliefern sowie Stabilität und Sicherheit zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt im sicheren und fehlerfreien Betrieb der Website. Die Logfiles werden nicht mit anderen Daten zusammengeführt und nach Ablauf der Speicherfrist des Hosters automatisch gelöscht, sofern keine längere Aufbewahrung zur Aufklärung eines Sicherheitsvorfalls erforderlich ist.</p>

      <h2>3. SSL- bzw. TLS-Verschlüsselung</h2>
      <p>Diese Website nutzt aus Sicherheitsgründen eine SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie an „https://“ in der Adresszeile Ihres Browsers.</p>

      <h2>4. Keine Cookies, kein Tracking</h2>
      <p>Wir verwenden keine Cookies und keine Dienste zur Reichweitenmessung, Analyse oder Werbung. Es findet kein Tracking statt. Ein Cookie-Banner ist deshalb nicht erforderlich.</p>

      <h2>5. Schriften, Bilder und Videos</h2>
      <p>Alle Schriften, Bilder und Videos werden direkt von unserem eigenen Server geladen. Es werden keine Daten an Drittanbieter wie Google Fonts, YouTube oder Content-Delivery-Netzwerke übertragen.</p>

      <h2>6. Kontaktaufnahme</h2>
      <p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben wie Name, Kontaktdaten und Ihre Nachricht, um Ihre Anfrage zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage mit einem Vertrag oder vorvertraglichen Maßnahmen zusammenhängt, im Übrigen Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt in der Beantwortung Ihrer Anfrage. Wir löschen die Daten, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten, etwa nach Handels- oder Steuerrecht, entgegenstehen.</p>
      <h3>Kontaktformular</h3>
      <p>Wenn Sie uns über das Kontaktformular schreiben, werden Ihr Name, Ihre E-Mail-Adresse und Ihre Nachricht über eine verschlüsselte Verbindung an unseren Server übertragen und von dort per E-Mail an info@capeeshee.com weitergeleitet. Die Angaben werden auf der Website nicht gespeichert. Zum Schutz vor Missbrauch wird Ihre IP-Adresse in gehashter, also unkenntlich gemachter Form für höchstens zwei Stunden vorübergehend verarbeitet, um mehrfache Massensendungen zu verhindern. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei Anfragen zu einem Auftrag, im Übrigen Art. 6 Abs. 1 lit. f DSGVO. Ihre E-Mail wird in unserem E-Mail-Postfach bei STRATO gespeichert und gelöscht, sobald sie nicht mehr erforderlich ist und keine Aufbewahrungspflichten bestehen.</p>

      <h2>7. Ihre Rechte</h2>
      <p>Sie haben jederzeit das Recht auf:</p>
      <ul><li>Auskunft über Ihre bei uns gespeicherten Daten (Art. 15 DSGVO)</li><li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li><li>Löschung Ihrer Daten (Art. 17 DSGVO)</li><li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li><li>Datenübertragbarkeit (Art. 20 DSGVO)</li><li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO)</li></ul>
      <h3>Widerspruchsrecht nach Art. 21 DSGVO</h3>
      <p>Beruht eine Verarbeitung auf Art. 6 Abs. 1 lit. f DSGVO, können Sie aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit Widerspruch gegen die Verarbeitung einlegen.</p>
      <p>Für die Ausübung Ihrer Rechte genügt eine formlose Nachricht an info@capeeshee.com.</p>

      <h2>8. Beschwerderecht bei der Aufsichtsbehörde</h2>
      <p>Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Für uns zuständig ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach, www.lda.bayern.de.</p>

      <h2>9. Aktualität dieser Datenschutzerklärung</h2>
      <p>Wir passen diese Datenschutzerklärung an, sobald sich die Website oder die rechtlichen Vorgaben ändern.</p>
      <p class="stand">Stand: November 2026</p>
    </div>
  </section>
'''

LEGAL_CSS = '''<style>.legal{padding-block:calc(var(--hh,72px) + clamp(40px,6vw,80px)) clamp(56px,8vw,110px)}.legal .wrap{max-width:860px}.legal h1{font-family:var(--display);font-weight:800;font-size:clamp(34px,5vw,56px);line-height:1.04;letter-spacing:-.04em;margin:0 0 28px}.legal h2{font-family:var(--display);font-weight:700;font-size:clamp(19px,2vw,23px);letter-spacing:-.02em;margin:40px 0 10px}.legal h3{font-family:var(--display);font-weight:600;font-size:17px;margin:24px 0 6px}.legal p,.legal li{max-width:70ch}.legal ul{padding-left:1.2em}.legal .stand{color:var(--muted);font-size:14px;margin-top:40px}</style>'''


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
    for ordner, titel, beschr, inhalt in [
        ('impressum', 'Impressum | Agentur Capeeshee', 'Impressum der Agentur Capeeshee, KI-powered Werbeagentur für Web & Print in Augsburg.', IMPRESSUM),
        ('datenschutz', 'Datenschutz | Agentur Capeeshee', 'Datenschutzerklärung der Agentur Capeeshee: keine Cookies, kein Tracking, Hosting in Deutschland.', DATENSCHUTZ)]:
        h = seite(start, titel, beschr, inhalt, '/' + ordner + '/').replace('</head>', LEGAL_CSS + '</head>', 1)
        os.makedirs(os.path.join(SITE, ordner), exist_ok=True)
        with open(os.path.join(SITE, ordner, 'index.html'), 'w', encoding='utf-8') as f:
            f.write('<!-- Automatisch erzeugt aus index.html durch tools/build_seiten.py. Bitte nicht direkt bearbeiten. -->\n' + h)
        print('erzeugt:', ordner + '/index.html')
    html = '<!-- Automatisch erzeugt aus index.html durch tools/build_seiten.py. Bitte nicht direkt bearbeiten. -->\n' + html
    with open(ziel, 'w', encoding='utf-8') as f:
        f.write(html)
    print('erzeugt:', os.path.relpath(ziel, SITE))


if __name__ == '__main__':
    main()
