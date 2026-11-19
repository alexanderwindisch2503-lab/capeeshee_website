"""Inhalte und Vorlage der Leistungsseiten (/webdesign/, /corporate-design/, ...).
Wird von tools/build_seiten.py eingebunden. Texte hier ändern, dann veröffentlichen.
Regeln: Sie-Ansprache, keine Gedankenstriche, Tennis nur im Bild, im Matchplan-Titel und im Zitat.
"""
import json
from html import escape

STANDORT = 'Agentur aus Augsburg · Projekte in Deutschland, Österreich und der Schweiz'
ZITAT_VON = 'Alexander Windisch'
ZITAT_ZEILE = 'Inhaber · Deutscher Meister, mehrfacher Europameister, ehemals Nr. 1 der Senioren-Weltrangliste'

SEITEN = [
  {
    'slug': 'webdesign', 'nr': '08', 'kurz': 'Webdesign',
    'titel': 'Webdesign Augsburg | Websites & Online-Shops | Agentur Capeeshee',
    'beschreibung': 'Webdesign aus Augsburg: Websites und Online-Shops, schnell, barrierefrei und für Google und KI-Suchen gebaut. Für Unternehmen in Deutschland, Österreich und der Schweiz.',
    'eyebrow': 'Leistung 08 · Websites & Shops',
    'h1': 'Webdesign, <span>das Anfragen bringt.</span>',
    'lead': 'Wir gestalten und programmieren Websites und Online-Shops für den Mittelstand. Schnell, barrierefrei, für Smartphones zuerst gebaut und so aufgebaut, dass Google und KI-Suchen Sie finden.',
    'bild': 'webdesign', 'alt': 'Ballwurf beim Tennisaufschlag vor blauem Himmel, darunter der Sandplatz',
    'cta': 'Website anfragen',
    'k_titel': 'Das bekommen <span>Sie von uns</span>',
    'k_sub': 'Von der einfachen Unternehmensseite bis zum B2B-Shop mit Schnittstellen. Alles aus einer Hand, ohne dass Sie zwischen Designer, Programmierer und Texter vermitteln müssen.',
    'karten': [
      ('Responsive Webdesign', 'Gestaltet für Smartphone, Tablet und Desktop. Ihr Corporate Design wird konsequent ins Netz übertragen.'),
      ('Programmierung', 'WordPress oder moderne Frameworks, je nachdem, was zu Ihnen passt. Mit individuellen Funktionen, wo Standard nicht reicht.'),
      ('Online-Shops', 'B2B- und B2C-Shops mit Warenwirtschaft, Kundenpreisen und Zahlungsanbietern.'),
      ('Barrierefreiheit', 'Nach aktuellen Standards. Für Online-Shops ist sie seit Juni 2025 vielfach gesetzlich vorgeschrieben.'),
      ('Gefunden werden', 'Saubere Technik, strukturierte Daten und Texte, die Google und KI-Suchen verstehen.'),
      ('Betreuung und Hosting', 'Updates, Sicherheit, Änderungen. Auf Wunsch als monatliche Pauschale.'),
    ],
    'zitat': 'Ein Ball, der zwei Zentimeter hinter der Linie aufkommt, ist genauso aus wie einer, der zwei Meter danebenfliegt. Bei Websites ist es nicht anders: Finden Besucher die Antwort auf ihre Frage nur fast, sind sie trotzdem weg. Deshalb bauen wir jede Seite so, dass der entscheidende Ball im Feld landet: die Anfrage.',
    's_titel': 'Ihr Matchplan: <span>So entsteht Ihre Website</span>',
    's_sub': 'Klare Schritte, ein fester Ansprechpartner, ein Festpreis.',
    'schritte': [
      ('Gespräch', 'Ziele, Zielgruppen, Umfang. Persönlich bei Ihnen oder per Video.'),
      ('Konzept und Entwurf', 'Struktur, Texte und Gestaltung. Sie sehen die Seite, bevor programmiert wird.'),
      ('Umsetzung', 'Programmierung, Inhalte, Tests auf allen Geräten.'),
      ('Start und Betreuung', 'Veröffentlichung, Google-Einrichtung, laufende Pflege.'),
    ],
    'r_titel': 'Websites, die wir <span>gebaut haben</span>',
    'refs': [(30, 'Sportkind', 'Website und Onlineshop'), (74, 'Setima Watches', 'Markenwebsite'), (190, 'Tannenhof Resort', 'Hotelwebsite')],
    'faq_titel': 'zum Webdesign',
    'faq': [
      ('Was kostet eine Website?', 'Das hängt vom Umfang ab: Anzahl der Seiten, Funktionen, Shop oder nicht. Nach einem kurzen Gespräch bekommen Sie ein Festpreisangebot, ohne versteckte Folgekosten.'),
      ('Wie lange dauert es bis zur fertigen Website?', 'Das hängt vom Umfang ab und davon, wie schnell Texte und Bilder vorliegen. Den Zeitplan legen wir zu Beginn gemeinsam und verbindlich fest. Bei Texten und Bildern unterstützen wir Sie, damit das Projekt nicht daran hängt.'),
      ('Kann ich die Inhalte selbst pflegen?', 'Ja. Auf Wunsch bauen wir Ihre Website mit einem Redaktionssystem wie WordPress, in dem Sie Texte, Bilder und Neuigkeiten selbst ändern. Wir zeigen Ihnen, wie es geht. Wenn Sie lieber nichts selbst machen möchten, übernehmen wir die Pflege.'),
      ('Muss meine Website barrierefrei sein?', 'Seit dem 28. Juni 2025 gilt das Barrierefreiheitsstärkungsgesetz. Es verpflichtet viele Anbieter, die online Produkte oder Dienstleistungen an Verbraucher verkaufen, etwa Online-Shops oder Buchungsportale, zur Barrierefreiheit. Kleinstunternehmen, die Dienstleistungen anbieten, sind ausgenommen. Unabhängig von der Pflicht lohnt sich Barrierefreiheit: Mehr Menschen können Ihre Seite nutzen, und Suchmaschinen verstehen sie besser. Wir prüfen gern, was für Sie gilt.'),
      ('Übernehmen Sie auch Hosting und Betreuung?', 'Ja. Wir kümmern uns um Hosting bei einem deutschen Anbieter, Sicherheitsupdates, Datensicherung und kleine Änderungen, auf Wunsch als monatliche Pauschale. Sie haben einen festen Ansprechpartner, wenn etwas zu tun ist.'),
    ],
    'dazu': ['corporate-design', 'werbung-print', 'seo', 'marketing'],
  },
  {
    'slug': 'corporate-design', 'nr': '04', 'kurz': 'Corporate Design',
    'titel': 'Corporate Design Augsburg | Logo & Markenauftritt | Agentur Capeeshee',
    'beschreibung': 'Corporate Design aus Augsburg: Logo, Farben, Schriften, Geschäftsausstattung und Markenhandbuch. Ein Auftritt, an dem man Sie erkennt, gedruckt wie online.',
    'eyebrow': 'Leistung 04 · Marke & Design',
    'h1': 'Corporate Design, <span>an dem man Sie erkennt.</span>',
    'lead': 'Innerhalb von rund 50 Millisekunden entscheiden Ihre Kunden, ob ihnen Ihr Auftritt gefällt. Wir entwickeln Logos und Erscheinungsbilder, die hochwertig wirken und auf jedem Medium wiedererkannt werden, vom Briefbogen bis zur Website.',
    'bild': 'corporate-design', 'alt': 'Makroaufnahme der geschwungenen Naht eines Tennisballs im warmen Studiolicht',
    'cta': 'Corporate Design anfragen',
    'k_titel': 'Das bekommen <span>Sie von uns</span>',
    'k_sub': 'Für Neugründungen den kompletten Markenauftritt. Für gewachsene Unternehmen eine behutsame Modernisierung, die das Bewährte erhält.',
    'karten': [
      ('Logo und Signet', 'Ein Zeichen, das funktioniert: groß auf dem Messestand, klein als App-Symbol, in Farbe und in Schwarzweiß.'),
      ('Farben, Schriften, Bildsprache', 'Die gestalterische Linie, die alle Medien zusammenhält und Ihr Unternehmen unverwechselbar macht.'),
      ('Geschäftsausstattung', 'Briefbogen, Visitenkarten, E-Mail-Signatur und Word-Vorlagen, druckfertig und sofort einsetzbar.'),
      ('Markenhandbuch mit KI-Vorgaben', 'Klare Regeln für Ihr Team, Dienstleister und KI-Werkzeuge, damit Ihr Auftritt einheitlich bleibt.'),
      ('Firmenpräsentationen', 'PowerPoint- und Keynote-Vorlagen in Ihrem Design, die Ihr Team selbst befüllen kann.'),
      ('Arbeitgebermarke', 'Ein Auftritt, der auch Fachkräfte überzeugt, von der Stellenanzeige bis zur Karriereseite.'),
    ],
    'zitat': 'Gute Spieler erkennt man am Aufschlag, lange bevor man ihr Gesicht sieht. Das kommt nicht von einem einzelnen Schlag, sondern von tausenden Wiederholungen. Eine Marke funktioniert genauso: Sie wird erkannt, wenn sie überall gleich auftritt, jeden Tag.',
    's_titel': 'Ihr Matchplan: <span>So entsteht Ihr Corporate Design</span>',
    's_sub': 'Erst verstehen, dann gestalten. Sie entscheiden bei jedem Schritt mit.',
    'schritte': [
      ('Analyse', 'Wofür steht Ihr Unternehmen, wer sind Ihre Kunden, wie treten Wettbewerber auf?'),
      ('Entwürfe', 'Mehrere Richtungen für Logo und Gestaltung, gezeigt an echten Anwendungen.'),
      ('Ausarbeitung', 'Die gewählte Richtung wird verfeinert und auf alle Medien übertragen.'),
      ('Übergabe', 'Alle Dateien, Vorlagen und das Markenhandbuch. Auf Wunsch begleiten wir die Einführung.'),
    ],
    'r_titel': 'Marken, die wir <span>entwickelt haben</span>',
    'refs': [(193, 'Hotel Kloster Holzen', 'Corporate Design'), (161, 'Tannenhof Resort', 'Corporate Design'), (53, 'Setima Watches', 'Marke und Produktdesign')],
    'faq_titel': 'zum Corporate Design',
    'faq': [
      ('Was gehört alles zu einem Corporate Design?', 'Logo, Farben, Schriften und Bildsprache bilden die Grundlage. Daraus entstehen Geschäftsausstattung, Vorlagen und Regeln für alle weiteren Medien. Welche Bausteine Sie brauchen, klären wir im ersten Gespräch.'),
      ('Kann ich nur ein neues Logo bekommen?', 'Ja. Wir entwickeln auch einzelne Bausteine wie ein Logo oder eine Geschäftsausstattung. Ein Logo wirkt allerdings erst richtig, wenn Farben, Schriften und Anwendungen dazu passen. Auf Wunsch legen wir deshalb die wichtigsten Grundregeln gleich mit fest.'),
      ('Wie lange dauert die Entwicklung?', 'Das hängt vom Umfang ab. Ein Logo mit Geschäftsausstattung entsteht schneller als ein komplettes Erscheinungsbild mit Markenhandbuch. Den Zeitplan stimmen wir zu Beginn gemeinsam mit Ihnen ab.'),
      ('Was ist ein Markenhandbuch mit KI-Vorgaben?', 'Ein Markenhandbuch legt fest, wie Ihr Auftritt aussieht: Logo, Farben, Schriften, Bildsprache und Tonalität. Mit KI-Vorgaben ergänzen wir Anweisungen für KI-Werkzeuge, zum Beispiel Beschreibungen Ihres Bildstils und Ihrer Sprache. So passen auch Texte und Bilder, die Ihr Team mit KI erstellt, zu Ihrer Marke.'),
      ('Erhalte ich alle Rechte und offenen Dateien?', 'Nach Abschluss erhalten Sie die vereinbarten Nutzungsrechte und alle Dateien in den gängigen Formaten für Druck und Bildschirm. Den Umfang der Rechte halten wir im Angebot klar fest.'),
    ],
    'dazu': ['webdesign', 'werbung-print', 'social-media', 'marketing'],
  },
  {
    'slug': 'werbung-print', 'nr': '05', 'kurz': 'Werbung & Print',
    'titel': 'Werbung & Print Augsburg | Broschüren, Kataloge, Kampagnen | Agentur Capeeshee',
    'beschreibung': 'Werbung und Print aus Augsburg: Broschüren, Kataloge, Plakate, Verpackungen, Beschilderung und Kampagnen. Gestaltet aus einem Guss und bis zur Druckabnahme betreut.',
    'eyebrow': 'Leistung 05 · Werbung & Kampagnen',
    'h1': 'Werbung und Print, <span>die man gern in die Hand nimmt.</span>',
    'lead': 'Broschüren, Kataloge, Plakate, Verpackungen und Kampagnen. Gestaltet aus einem Guss mit Ihrem Auftritt und bis zur Druckabnahme betreut. Print und Online denken wir zusammen, damit jede Maßnahme dort wirkt, wo sie am meisten bringt.',
    'bild': 'werbung-print', 'alt': 'Tennisball springt vom Sandplatz ab, sein Abdruck liegt knapp neben der weißen Linie',
    'cta': 'Projekt anfragen',
    'k_titel': 'Das bekommen <span>Sie von uns</span>',
    'k_sub': 'Von der einzelnen Anzeige bis zur kompletten Kampagne über alle Kanäle.',
    'karten': [
      ('Broschüren und Kataloge', 'Imagebroschüren, Produktkataloge und Preislisten, auch mit über hundert Seiten.'),
      ('Flyer, Plakate, Anzeigen', 'Für Print und Online, in allen Formaten und abgestimmt auf Ihre Kampagne.'),
      ('Verpackung und Produkt', 'Verpackungsdesign, Etiketten und Produktgestaltung, die im Regal auffallen.'),
      ('Beschilderung und Leitsysteme', 'Außen- und Innenbeschilderung, Orientierung im Gebäude, Fahrzeugbeschriftung.'),
      ('Messe und Event', 'Messestände, Roll-ups, Einladungen und alles, was vor Ort gebraucht wird.'),
      ('Druck und Produktion', 'Papierwahl, Veredelung, Druckerei und Farbabnahme. Sie bekommen das fertige Produkt.'),
    ],
    'zitat': 'Ein bisschen aus gibt es nicht. Eine Kampagne, die ihre Zielgruppe knapp verfehlt, ist genauso verloren wie eine, die völlig danebengeht. Deshalb klären wir vor jedem Entwurf genau, wen sie treffen soll, wo und in welchem Moment.',
    's_titel': 'Ihr Matchplan: <span>So entsteht Ihr Werbemittel</span>',
    's_sub': 'Von der Idee bis zur Lieferung, mit einem festen Ansprechpartner.',
    'schritte': [
      ('Briefing', 'Ziel, Zielgruppe, Format, Auflage und Termin.'),
      ('Konzept und Gestaltung', 'Idee, Text und Layout. Sie sehen den Entwurf in Originalgröße.'),
      ('Reinzeichnung', 'Druckfertige Daten, Farbprüfung und Korrekturen.'),
      ('Druck und Lieferung', 'Wir steuern Druckerei und Veredelung bis zur Auslieferung.'),
    ],
    'r_titel': 'Drucksachen, die wir <span>gestaltet haben</span>',
    'refs': [(1, 'Sportkind', 'Katalog'), (197, 'Hotel Kloster Holzen', 'Imagebroschüre'), (61, 'Setima Watches', 'Plakatkampagne')],
    'faq_titel': 'zu Werbung und Print',
    'faq': [
      ('Lohnt sich Print heute noch?', 'In vielen Situationen ja: im Verkaufsgespräch, auf der Messe, am Point of Sale oder als Imagebroschüre. Gedrucktes bleibt liegen und wird wieder in die Hand genommen. Wir setzen es gezielt dort ein, wo es mehr bewirkt als eine Online-Maßnahme.'),
      ('Übernehmen Sie auch den Druck?', 'Ja. Wir holen Angebote ein, wählen Papier und Veredelung mit Ihnen aus, prüfen die Druckdaten und begleiten auf Wunsch die Farbabnahme. Sie bekommen das fertige Produkt geliefert.'),
      ('Können Sie mit unserem bestehenden Design arbeiten?', 'Selbstverständlich. Wir halten uns genau an Ihre Gestaltungsrichtlinien, damit sich jedes neue Werbemittel nahtlos in Ihren Auftritt einfügt und ihn stärkt.'),
      ('Wie lange dauert ein Katalog?', 'Das hängt vor allem von Umfang, Produktdaten und Bildern ab. Bei größeren Katalogen arbeiten wir mit klaren Abläufen für Daten, Korrekturen und Freigaben. Den Zeitplan legen wir gemeinsam vom Liefertermin aus rückwärts fest.'),
      ('Bekomme ich auch Dateien für Online?', 'Ja. Auf Wunsch erhalten Sie zu jeder Drucksache eine Fassung für Website, E-Mail und soziale Medien, zum Beispiel als blätterbares PDF oder als Motive in den passenden Formaten.'),
    ],
    'dazu': ['corporate-design', 'webdesign', 'social-media', 'marketing'],
  },
  {
    'slug': 'seo', 'nr': '10', 'kurz': 'SEO & Online-Werbung',
    'titel': 'SEO Augsburg | Suchmaschinenoptimierung & Google-Anzeigen | Agentur Capeeshee',
    'beschreibung': 'SEO und Online-Werbung aus Augsburg: gefunden werden bei Google, auf Google Maps und in KI-Suchen. Suchmaschinenoptimierung, Google-Anzeigen, Unternehmensprofil und klare Auswertungen.',
    'eyebrow': 'Leistung 10 · Online-Werbung & SEO',
    'h1': 'Gefunden werden, <span>ohne große Budgets.</span>',
    'lead': 'Wir sorgen dafür, dass Ihre Kunden Sie bei Google, auf Google Maps und in KI-Suchen finden. Mit sauberer Technik, guten Inhalten, gezielten Anzeigen und einem gepflegten Unternehmensprofil.',
    'bild': 'seo', 'alt': 'Läufer im Morgenlicht auf einem Sandplatz, im Vordergrund Fußspuren entlang der Linie',
    'cta': 'SEO-Check anfragen',
    'k_titel': 'Das bekommen <span>Sie von uns</span>',
    'k_sub': 'Erst prüfen, wo Sie stehen. Dann gezielt das verbessern, was die meisten Anfragen bringt.',
    'karten': [
      ('Suchmaschinenoptimierung', 'Technik, Seitenstruktur, Texte und strukturierte Daten, damit Google Ihre Seite versteht und gut einordnet.'),
      ('Sichtbar in KI-Suchen', 'Inhalte, die von ChatGPT, Gemini und anderen KI-Assistenten als Quelle genutzt werden können.'),
      ('Google-Unternehmensprofil', 'Einrichtung, Pflege und Bewertungen, damit Sie in der Kartenansicht erscheinen.'),
      ('Google- und Social-Anzeigen', 'Kampagnen mit klarem Budget und klaren Zielen, laufend ausgewertet.'),
      ('Landingpages', 'Eigene Seiten für Kampagnen und Angebote, gebaut für Anfragen.'),
      ('Auswertung', 'Ein übersichtlicher Monatsbericht mit klaren Empfehlungen statt Datenbergen.'),
    ],
    'zitat': 'Ein Fünf-Satz-Match gewinnt man nicht im ersten Spiel. Man führt, gerät in Rückstand, kämpft sich zurück. Bei Google ist es ähnlich: Vorn steht, wer dranbleibt und die entscheidenden Punkte macht. Ein Punkt bei 5:4 zählt mehr als einer bei 2:2. Deshalb setzen wir dort an, wo es um Ihre Anfragen geht.',
    's_titel': 'Ihr Matchplan: <span>So gehen wir vor</span>',
    's_sub': 'Schritt für Schritt, mit messbaren Ergebnissen.',
    'schritte': [
      ('Bestandsaufnahme', 'Wo stehen Sie bei Google, was machen Ihre Wettbewerber, wo liegen schnelle Verbesserungen?'),
      ('Grundlagen', 'Technik, Texte, Unternehmensprofil und Einträge in Verzeichnissen.'),
      ('Inhalte und Anzeigen', 'Neue Seiten, Ratgeber und gezielte Kampagnen.'),
      ('Messen und verbessern', 'Monatlich auswerten, was wirkt, und nachsteuern.'),
    ],
    'erfolg': [
      ('Mehr Anfragen', 'Kontaktformular, Anrufe und E-Mails, die über die Website kommen.'),
      ('Bessere Plätze', 'Für die Suchbegriffe, nach denen Ihre Kunden tatsächlich suchen.'),
      ('Mehr Bewertungen', 'Und damit mehr Vertrauen, bevor der erste Kontakt entsteht.'),
    ],
    'faq_titel': 'zu SEO und Online-Werbung',
    'faq': [
      ('Wie lange dauert es, bis SEO wirkt?', 'Erste Verbesserungen sind oft nach einigen Wochen sichtbar. Spürbare Ergebnisse brauchen meist drei bis sechs Monate, je nach Branche und Wettbewerb. Anzeigen wirken dagegen sofort.'),
      ('Was kostet Suchmaschinenoptimierung?', 'Das hängt von Ausgangslage, Wettbewerb und Zielen ab. Nach einer ersten Bestandsaufnahme bekommen Sie ein Angebot, entweder als einmaliges Projekt oder als monatliche Betreuung mit klarem Leistungsumfang.'),
      ('Brauche ich SEO oder Google-Anzeigen?', 'Beides hat seinen Platz. Anzeigen bringen sofort Sichtbarkeit, kosten aber für jeden Klick. SEO braucht länger, wirkt dafür dauerhaft. Für viele Unternehmen ist eine Kombination sinnvoll: Anzeigen für den schnellen Start, SEO für die langfristige Grundlage.'),
      ('Was bedeutet Sichtbarkeit in KI-Suchen?', 'Immer mehr Menschen stellen ihre Fragen direkt an KI-Assistenten wie ChatGPT, Gemini oder Perplexity, statt bei Google zu suchen. Diese nennen bevorzugt Unternehmen, deren Informationen klar, aktuell und gut strukturiert im Netz stehen. Wir bereiten Ihre Inhalte so auf, dass sie dafür in Frage kommen.'),
      ('Können Sie meine bestehende Website optimieren?', 'Ja. Wir prüfen Technik, Inhalte und Struktur Ihrer bestehenden Website und verbessern sie gezielt. Nur wenn die Grundlage nicht mehr trägt, empfehlen wir einen Neuaufbau.'),
    ],
    'dazu': ['webdesign', 'social-media', 'marketing', 'werbung-print'],
  },
  {
    'slug': 'social-media', 'nr': '07', 'kurz': 'Social Media',
    'titel': 'Social Media Agentur Augsburg | LinkedIn, Instagram, Recruiting | Agentur Capeeshee',
    'beschreibung': 'Social Media aus Augsburg: Strategie, Redaktionsplan, Beiträge und Recruiting auf LinkedIn, Instagram, Facebook und TikTok. Mit einem Plan, der zu Ihrem Alltag passt.',
    'eyebrow': 'Leistung 07 · Social Media',
    'h1': 'Social Media, <span>das zu Ihnen passt.</span>',
    'lead': 'Sichtbar sein, wo Ihre Kunden und künftigen Mitarbeiter täglich unterwegs sind. Mit einem klaren Plan, Inhalten in Ihrem Design und einem Aufwand, der zu Ihrem Unternehmen passt.',
    'bild': 'social-media', 'alt': 'Ballkorb voller Tennisbälle auf einem Sandplatz, davor einzelne Bälle',
    'cta': 'Social Media anfragen',
    'k_titel': 'Das bekommen <span>Sie von uns</span>',
    'k_sub': 'Wir übernehmen Social Media komplett oder unterstützen Ihr Team, damit es selbst gute Beiträge veröffentlichen kann.',
    'karten': [
      ('Strategie', 'Welche Kanäle passen zu Ihnen, welche Themen, wie oft? Realistisch geplant statt überall ein bisschen.'),
      ('Redaktionsplan', 'Themen für die nächsten Monate, abgestimmt auf Saison, Messen und Angebote.'),
      ('Beiträge und Vorlagen', 'Bilder, Videos und Texte in Ihrem Design, dazu Vorlagen, die Ihr Team selbst nutzen kann.'),
      ('LinkedIn, Instagram, Facebook, TikTok', 'Jeder Kanal mit eigener Sprache und eigenem Format.'),
      ('Recruiting', 'Stellenanzeigen und Einblicke ins Unternehmen, die Fachkräfte ansprechen.'),
      ('Mitarbeitende als Botschafter', 'Schulung und Leitfaden, damit Ihr Team gern und sicher für Sie spricht.'),
    ],
    'zitat': 'Im Tennis gewinnt oft nicht, wer die spektakulärsten Schläge hat, sondern wer einen Ball mehr ins Feld spielt als der Gegner. In sozialen Medien ist Beständigkeit wichtiger als der eine große Auftritt. Mit einem Plan, der zu Ihrem Alltag passt, bleiben Sie im Spiel.',
    's_titel': 'Ihr Matchplan: <span>So bringen wir Sie ins Gespräch</span>',
    's_sub': 'Mit einem Plan, der auch nach drei Monaten noch funktioniert.',
    'schritte': [
      ('Bestandsaufnahme', 'Welche Kanäle gibt es schon, was funktioniert, was machen Wettbewerber?'),
      ('Strategie und Plan', 'Kanäle, Themen, Häufigkeit und Zuständigkeiten.'),
      ('Inhalte', 'Vorlagen, Bilder, Videos und Texte. Wir veröffentlichen oder Ihr Team.'),
      ('Auswerten', 'Was kommt an, was nicht? Monatlich nachsteuern.'),
    ],
    'r_titel': 'Kampagnen, die wir <span>gestaltet haben</span>',
    'r_sub': 'Motive für Anzeigen, Newsletter und soziale Medien.',
    'refs': [(20, 'Sportkind', 'Kampagnenmotiv'), (33, 'Sportkind', 'Aktion Cyber Monday'), (260, 'Hotel Kloster Holzen', 'Veranstaltung')],
    'faq_titel': 'zu Social Media',
    'faq': [
      ('Auf welchen Kanälen sollten wir aktiv sein?', 'Dort, wo Ihre Zielgruppe ist. Für B2B ist das meist LinkedIn, für Hotellerie und Handel eher Instagram und Facebook, für das Recruiting junger Fachkräfte auch TikTok. Lieber zwei Kanäle gut als fünf halbherzig.'),
      ('Wie oft sollten wir etwas veröffentlichen?', 'Regelmäßigkeit ist wichtiger als Menge. Für viele Unternehmen sind ein bis drei gute Beiträge pro Woche und Kanal ein realistischer Rhythmus. Entscheidend ist, dass Sie ihn dauerhaft halten können.'),
      ('Können wir Beiträge selbst erstellen?', 'Ja. Wir entwickeln Vorlagen in Ihrem Design und einen Themenplan und zeigen Ihrem Team, wie es damit arbeitet. Viele Unternehmen kombinieren beides: Wir übernehmen Planung und besondere Beiträge, das Team ergänzt Einblicke aus dem Alltag.'),
      ('Was kostet Social Media Betreuung?', 'Das hängt von der Zahl der Kanäle, der Häufigkeit und davon ab, wie viel Ihr Team selbst übernimmt. Sie bekommen ein Angebot mit festem monatlichem Umfang.'),
      ('Lohnt sich Social Media für Recruiting?', 'Ja. Viele Fachkräfte suchen nicht aktiv nach einer neuen Stelle, sehen aber in sozialen Medien, wie es in einem Unternehmen zugeht. Echte Einblicke und Beiträge von Mitarbeitenden wirken dabei besonders glaubwürdig.'),
    ],
    'dazu': ['werbung-print', 'seo', 'corporate-design', 'marketing'],
  },
  {
    'slug': 'marketing', 'nr': '', 'kurz': 'Marketing heute',
    'titel': 'Werbung und Marketing heute | New Marketing | Agentur Capeeshee Augsburg',
    'beschreibung': 'Werbung und Marketing haben sich verändert: Kunden informieren sich selbst, im Netz, in sozialen Medien und bei der KI. Wie New Marketing heute wirkt, erklärt die Agentur Capeeshee aus Augsburg.',
    'eyebrow': 'New Marketing · Werbung und Marketing heute',
    'h1': 'Das Spiel <span>hat sich verändert.</span>',
    'lead': 'Anzeige schalten, Prospekt drucken, abwarten: Das reicht heute nicht mehr. Kunden informieren sich selbst, im Netz, in sozialen Medien und bei der KI. Wir zeigen, wie Werbung und Marketing heute wirken und wie Sie sich gegen starke Wettbewerber durchsetzen.',
    'bild': 'marketing', 'alt': 'Hand tippt nachts unter Flutlicht einen Tennisball auf den Sandplatz',
    'cta': 'Marketing besprechen',
    'k_titel': 'Was sich in Werbung und <span>Marketing verändert hat</span>',
    'k_sub': 'Die Regeln sind andere geworden. Wer sie kennt, erreicht mit weniger Aufwand mehr.',
    'karten': [
      ('Perspektive wechseln', 'Manchmal muss man die Dinge auf den Kopf stellen. Wir schauen mit den Augen Ihrer Kunden auf Ihr Marketing, nicht mit Ihren.'),
      ('Schluss mit Einbahnstraßen-Marketing', 'Botschaften senden und hoffen, dass jemand zuhört, funktioniert nicht mehr. Dialog, Nutzen und Inhalte, die Kunden wirklich brauchen, schon.'),
      ('Dort sein, wo Kunden sind', 'Google, KI-Suche, LinkedIn, Instagram, Messe oder Briefkasten. Die Botschaft gehört in den Kanal, in dem Ihre Kunden gerade unterwegs sind.'),
      ('Zusatznutzen statt Austauschbarkeit', 'In vielen Branchen sind Produkte vergleichbar. Gewinnen wird, wer seinen Kunden etwas mehr bietet: Beratung, Service, Wissen, Erlebnis.'),
      ('Kontinuität statt Einzelaktion', 'Eine einzelne Kampagne verpufft. Sichtbar wird eine Marke erst, wenn sie dauerhaft und auf allen passenden Kanälen präsent ist.'),
      ('KI als Werkzeug', 'KI beschleunigt Texte, Bilder und Auswertungen. Erfahrung entscheidet, was davon zu Ihrer Marke passt und veröffentlicht wird.'),
    ],
    'zitat': 'Am Ende eines langen Matches entscheiden oft Nuancen: eine stabile Psyche, die richtigen Entscheidungen, der richtige Ball im richtigen Moment. Genau das habe ich in vielen Jahren Profitennis gelernt, und genau so arbeite ich heute für meine Kunden.',
    's_titel': 'Ein Produktzyklus ist <span>wie ein Fünf-Satz-Match</span>',
    's_sub': 'Führung, Rückstand, Aufholjagd. Entscheidend ist, in jeder Phase das Richtige zu tun.',
    'schritte': [
      ('Einspielen', 'Markt verstehen, Zielgruppe kennen, Auftritt vorbereiten.'),
      ('In Führung gehen', 'Markteintritt mit klarer Botschaft. Die ersten Spiele laufen gut.'),
      ('Der Gegner holt auf', 'Wettbewerber ziehen nach, das Produkt wird vergleichbar.'),
      ('Auf Stärken besinnen', 'Zusatznutzen herausarbeiten, Kanäle schärfen, dranbleiben.'),
      ('Die Big Points machen', 'Im richtigen Moment den richtigen Ball: die Kampagne, die den Unterschied macht.'),
    ],
    'faq_titel': 'zu Werbung und Marketing heute',
    'faq': [
      ('Was ist New Marketing?', 'Marketing, das vom Kunden her denkt. Statt Botschaften an möglichst viele zu senden, geht es darum, Menschen dort abzuholen, wo sie sich gerade informieren, und ihnen etwas zu bieten, das ihnen nützt. Klassische Werbung gehört weiter dazu, aber gezielt eingesetzt.'),
      ('Was bedeutet Einbahnstraßen-Marketing?', 'Werbung, die nur sendet: Anzeige, Prospekt, Plakat, ohne dass der Kunde antworten kann oder etwas davon hat. Heute erwarten Kunden Dialog und Nutzen. Wer Fragen beantwortet, hilft und zuhört, wird eher wahrgenommen als jemand, der nur lauter ruft.'),
      ('Funktioniert klassische Werbung heute noch?', 'Ja, wenn sie gezielt eingesetzt wird. Eine hochwertige Broschüre im Verkaufsgespräch, ein Plakat am richtigen Ort oder eine Anzeige im passenden Fachmedium wirken weiterhin. Entscheidend ist, dass sie Teil eines Gesamtplans sind und mit Online-Maßnahmen zusammenspielen.'),
      ('Wie hebe ich mich ab, wenn meine Produkte austauschbar sind?', 'Durch Zusatznutzen: Beratung, Service, Geschwindigkeit, Wissen oder ein besonderes Erlebnis. Wir arbeiten heraus, was Ihr Unternehmen anders macht als andere, und machen genau das sichtbar. Oft sind es Kleinigkeiten, die den Unterschied machen.'),
      ('Welche Rolle spielt KI im Marketing?', 'KI ist ein Werkzeug, das Texte, Bilder, Recherchen und Auswertungen beschleunigt. Sie ersetzt aber keine Strategie und kein Urteil darüber, was zu Ihrer Marke passt. Wir setzen KI dort ein, wo sie Zeit und Kosten spart, und prüfen jedes Ergebnis selbst.'),
    ],
    'dazu': ['webdesign', 'corporate-design', 'werbung-print', 'seo', 'social-media'],
  },
]

NAMEN = {s['slug']: s['kurz'] for s in SEITEN}

CSS = '''<style>
.lp{background:var(--bg-alt)}
.lp .w{max-width:1160px;margin:0 auto;padding:0 clamp(20px,4vw,24px)}
.lp .crumb{font-family:var(--body);font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:34px 0 0;margin:0}
.lp .crumb a{color:var(--muted);text-decoration:none}.lp .crumb a:hover{color:var(--red)}
.lp .crumb b{color:var(--ink);font-weight:600}
.lp .lp-hero{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(28px,5vw,56px);align-items:start;padding:34px 0 clamp(56px,7vw,80px)}
.lp .lp-hero .eyebrow{margin-top:0}
.lp h1{font-family:var(--display);font-weight:800;font-size:clamp(38px,5vw,60px);letter-spacing:-.045em;line-height:1.02;margin:0 0 24px;color:var(--ink)}
.lp h1 span,.lp h2 span{color:var(--red)}
.lp .lp-lead{font-size:clamp(17px,1.6vw,19px);line-height:1.6;color:var(--text);margin:0 0 18px}
.lp .lp-ort{font-family:var(--body);letter-spacing:.12em;text-transform:uppercase;font-size:12.5px;color:var(--muted);margin:0 0 28px;line-height:1.6}
.lp .lp-btns{display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.lp .lp-ln{font-family:var(--body);font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:14px;color:var(--ink);border-bottom:2px solid var(--ink);padding-bottom:3px;text-decoration:none}
.lp .lp-ln:hover{color:var(--red);border-color:var(--red)}
.lp .lp-bild img{display:block;width:100%;height:auto;aspect-ratio:5/4;object-fit:cover}
.lp section{padding:clamp(56px,7vw,84px) 0}
.lp section.wh{background:#fff}
.lp section.dk{background:var(--dark);color:#fff}
.lp h2{font-size:clamp(30px,3.6vw,44px);line-height:1.06;margin:0 0 18px;color:var(--ink)}
.lp .dk h2{color:#fff}.lp .dk h2 span{color:#d98455}
.lp .lp-sub{font-size:clamp(16px,1.4vw,18px);line-height:1.65;color:var(--text);max-width:780px;margin:0 0 40px}
.lp .dk .lp-sub{color:var(--dark-text)}
.lp .g3{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}
.lp .g3>div{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:28px 26px 30px;background:#fff}
.lp .g3 .n{font-family:var(--body);font-weight:600;color:var(--red);font-size:14px;letter-spacing:.1em}
.lp .g3 h3{font-family:var(--display);font-weight:600;font-size:20px;letter-spacing:-.01em;margin:10px 0 8px;color:var(--ink)}
.lp .g3 p{margin:0;color:var(--text);font-size:16px;line-height:1.6}
.lp .steps{display:grid;gap:24px}
.lp .steps div{border-top:3px solid #d98455;padding-top:18px}
.lp .steps i{font-style:normal;font-family:var(--body);letter-spacing:.14em;color:#d98455;font-size:13px;text-transform:uppercase}
.lp .steps b{display:block;font-family:var(--display);font-weight:600;font-size:19px;margin:6px 0 8px;color:#fff}
.lp .steps p{margin:0;color:var(--dark-text);font-size:16px;line-height:1.6}
.lp .zit{max-width:900px}
.lp .zit .eyebrow{margin-bottom:22px}
.lp .zq{font-family:var(--display);font-weight:500;font-size:clamp(21px,2.3vw,27px);line-height:1.45;letter-spacing:-.01em;color:var(--ink);margin:0 0 24px;border-left:4px solid var(--red);padding-left:28px;quotes:none}
.lp .za{margin:0;padding-left:32px;color:var(--muted);font-size:14px;line-height:1.5}
.lp .za b{display:block;color:var(--ink);font-family:var(--display);font-weight:600;font-size:16px}
.lp .refs{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:30px}
.lp .refs a{background:#fff;display:block;color:inherit;text-decoration:none;transition:transform .2s}
.lp .refs a:hover{transform:translateY(-3px)}
.lp .refs img{display:block;width:calc(100% - 32px);margin:16px;aspect-ratio:16/11;object-fit:contain;height:auto}
.lp .refs p{margin:0;padding:0 20px 20px;font-family:var(--display);font-weight:600;font-size:18px;color:var(--ink)}
.lp .refs p span{display:block;font-family:var(--body);font-weight:400;letter-spacing:.12em;text-transform:uppercase;font-size:12px;color:var(--muted);margin-top:4px}
.lp .faq{max-width:860px}
.lp .faq details{border-bottom:1px solid var(--line);padding:20px 0}
.lp .faq summary{display:flex;justify-content:space-between;gap:20px;cursor:pointer;list-style:none;font-family:var(--display);font-weight:600;font-size:clamp(17px,1.6vw,19px);color:var(--ink)}
.lp .faq summary::-webkit-details-marker{display:none}
.lp .faq summary::after{content:"+";color:var(--red);font-size:24px;line-height:1}
.lp .faq details[open] summary::after{content:"\\2212"}
.lp .faq details p{margin:12px 0 0;color:var(--text);font-size:16px;line-height:1.65;max-width:72ch}
.lp .more{display:flex;flex-wrap:wrap;gap:10px}
.lp .more a{border:1px solid #cfcfca;border-radius:99px;padding:10px 16px;font-size:15px;color:var(--ink);text-decoration:none}
.lp .more a:hover{border-color:var(--red);color:var(--red)}
.lp .crumbrow{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:nowrap;padding-top:34px;min-height:20px;line-height:20px}.lp .crumbrow .crumb{line-height:20px;margin:0}
@media (max-width:700px){.lp .crumbrow .back{display:none}}.lp .crumbrow .crumb{padding-top:0}
.lp .back{font-family:var(--head);font-weight:600;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--red);text-decoration:none}.lp .back:hover{text-decoration:underline;text-underline-offset:3px}
.lp .back-unten{display:inline-block;margin-top:34px;border:2px solid var(--red);border-radius:99px;padding:13px 22px}.lp .back-unten:hover{background:var(--red);color:#fff;text-decoration:none}
.lp h2.klein{font-size:clamp(24px,2.4vw,30px)}
@media (max-width:860px){.lp .lp-hero{grid-template-columns:1fr}.lp .g3,.lp .refs{grid-template-columns:1fr}.lp .steps{grid-template-columns:1fr 1fr!important}}
@media (max-width:480px){.lp .steps{grid-template-columns:1fr!important}}
</style>'''


def _e(t):
    return escape(t, quote=False)


def inhalt(s):
    u = '/' + s['slug'] + '/'
    kontakt = u + '#kontakt'
    karten = ''.join(f'<div><span class="n">{i:02d}</span><h3>{_e(a)}</h3><p>{_e(b)}</p></div>' for i, (a, b) in enumerate(s['karten'], 1))
    schritte = ''.join(f'<div><i>Schritt {i}</i><b>{_e(a)}</b><p>{_e(b)}</p></div>' for i, (a, b) in enumerate(s['schritte'], 1))
    if s.get('refs'):
        refs = ''.join(f'<a href="/referenzen/"><img src="img/leistungen/ref/r{n}.jpg" alt="{_e(k)}: {_e(t)}" width="720" height="480" loading="lazy"><p>{_e(k)}<span>{_e(t)}</span></p></a>' for n, k, t in s['refs'])
        sub = f'<p class="lp-sub">{_e(s["r_sub"])}</p>' if s.get('r_sub') else ''
        refblock = f'<section><div class="w"><h2>{s["r_titel"]}</h2>{sub}<div class="refs">{refs}</div></div></section>'
    elif s.get('erfolg'):
        e = ''.join(f'<div><span class="n">{i:02d}</span><h3>{_e(a)}</h3><p>{_e(b)}</p></div>' for i, (a, b) in enumerate(s['erfolg'], 1))
        refblock = f'<section><div class="w"><h2>Woran Sie den Erfolg <span>erkennen</span></h2><p class="lp-sub">Wir arbeiten mit Zahlen, die für Ihr Geschäft zählen, nicht mit Kennzahlen, die nur gut klingen.</p><div class="g3">{e}</div></div></section>'
    else:
        refblock = ''
    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{_e(q)}</summary><p>{_e(a)}</p></details>' for i, (q, a) in enumerate(s['faq']))
    dazu = ''.join(f'<a href="/{d}/">{_e(NAMEN[d])}</a>' for d in s['dazu'])
    crumb_mitte = '<a href="/#leistungen">Leistungen</a> › ' if s['nr'] else ''
    return f'''
  <div class="lp">
    <div class="w">
      <div class="crumbrow"><p class="crumb"><a href="/">Startseite</a> › {crumb_mitte}<b>{_e(s["kurz"])}</b></p><a class="back" href="/#leistungen">← Alle Leistungen</a></div>
      <div class="lp-hero">
        <div>
          <p class="eyebrow">{_e(s["eyebrow"])}</p>
          <h1>{s["h1"]}</h1>
          <p class="lp-lead">{_e(s["lead"])}</p>
          <p class="lp-ort">{STANDORT}</p>
          <div class="lp-btns"><a class="btn" href="{kontakt}">{_e(s["cta"])}</a><a class="lp-ln" href="/referenzen/">Referenzen ansehen</a></div>
        </div>
        <figure class="lp-bild" style="margin:0"><picture><source srcset="img/leistungen/{s["bild"]}.webp" type="image/webp"><img src="img/leistungen/{s["bild"]}.jpg" alt="{_e(s["alt"])}" width="1400" height="1120" fetchpriority="high"></picture><span class="ai-cap"><b>KI</b>KI-generiert von Capeeshee</span></figure>
      </div>
    </div>
    <section class="wh"><div class="w"><h2>{s["k_titel"]}</h2><p class="lp-sub">{_e(s["k_sub"])}</p><div class="g3">{karten}</div></div></section>
    <section class="dk"><div class="w"><h2>{s["s_titel"]}</h2><p class="lp-sub">{_e(s["s_sub"])}</p><div class="steps" style="grid-template-columns:repeat({len(s["schritte"])},1fr)">{schritte}</div></div></section>
    <section class="wh"><div class="w zit"><p class="eyebrow">Vom Centre Court in die Agentur</p><blockquote class="zq">{_e(s["zitat"])}</blockquote><p class="za"><b>{ZITAT_VON}</b>{ZITAT_ZEILE}</p></div></section>
    {refblock}
    <section class="wh"><div class="w"><h2>Häufige Fragen <span>{_e(s["faq_titel"])}</span></h2><div class="faq">{faq}</div></div></section>
    <section><div class="w"><h2 class="klein">Das passt <span>dazu</span></h2><div class="more">{dazu}</div><a class="back back-unten" href="/#leistungen">← Alle Leistungen im Überblick</a></div></section>
  </div>
'''


def json_ld(s):
    u = 'https://capeeshee.com/' + s['slug'] + '/'
    g = [
        {'@type': 'Service', '@id': u + '#leistung', 'name': s['kurz'], 'serviceType': s['kurz'], 'url': u,
         'description': s['beschreibung'],
         'provider': {'@type': 'ProfessionalService', '@id': 'https://capeeshee.com/#agentur', 'name': 'Agentur Capeeshee'},
         'areaServed': [{'@type': 'Country', 'name': n} for n in ('Deutschland', 'Österreich', 'Schweiz')]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faq']]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': 'https://capeeshee.com/'},
            {'@type': 'ListItem', 'position': 2, 'name': s['kurz'], 'item': u}]},
    ]
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False) + '</script>'
