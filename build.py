#!/usr/bin/env python3
"""Erzeugt die statischen Seiten von bannerfall-tinybattle.com (Englisch im Wurzelordner, Deutsch unter /de/).
Aufruf: python3 build.py  – danach committen und pushen (GitHub Pages)."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTACT = "ehmannjakob@gmail.com"
UPDATED = {"en": "October 20, 2026", "de": "20. Oktober 2026"}

T = {
    "en": {
        "nav": [("index.html", "Home"), ("support.html", "Support"), ("privacy.html", "Privacy"), ("imprint.html", "Imprint")],
        "switch": ("de/", "Deutsch"),
        "prefix": "",
        "footer": "© 2026 Jakob Ehmann · Bannerfall: Tiny Battle",
    },
    "de": {
        "nav": [("index.html", "Start"), ("support.html", "Support"), ("datenschutz.html", "Datenschutz"), ("impressum.html", "Impressum")],
        "switch": ("../index.html?en", "English"),
        "prefix": "../",
        "footer": "© 2026 Jakob Ehmann · Bannerfall: Tiny Battle",
    },
}


def page(lang, file, title, body, description=""):
    t = T[lang]
    p = t["prefix"]
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{current if href == file else ""}>{label}</a>' for href, label in t["nav"]
    )
    alt = "de/" + {"index.html": "index.html", "support.html": "support.html", "privacy.html": "datenschutz.html", "imprint.html": "impressum.html"}.get(file, "index.html") if lang == "en" else \
        "../" + {"index.html": "index.html?en", "support.html": "support.html", "datenschutz.html": "privacy.html", "impressum.html": "imprint.html"}.get(file, "index.html")
    html = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{p}favicon.png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Afacad+Flux:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
</head>
<body>
<div class="wrap">
<header class="top">
<a class="brand" href="index.html"><img src="{p}img/icon.png" alt="">Bannerfall</a>
<nav>{nav}<a href="{alt}" lang="{"de" if lang == "en" else "en"}">{t["switch"][1]}</a></nav>
</header>
{body}
</div>
<footer><div class="wrap"><span>{t["footer"]}</span><span>{" · ".join(f'<a href="{h}">{l}</a>' for h, l in t["nav"][1:])}</span></div></footer>
</body>
</html>
"""
    out = os.path.join(ROOT, "" if lang == "en" else "de", file)
    with open(out, "w") as f:
        f.write(html)


def home(lang):
    p = T[lang]["prefix"]
    if lang == "en":
        tag, lead = "Coming soon to iPhone", "Build your army, upgrade your heroes and storm the enemy castle. A cute but tactical lane battle game – easy to pick up, hard to master."
        cta = ("support.html", "Contact & beta")
        features = [
            ("Swarm battles", "Waves of goblins, orcs and the undead crash into your army. Hold the line, then break through when the battle frenzy begins."),
            ("Collect & ascend", "Unlock knights, mages, samurai and more. Level them up, equip weapons with elements and watch them transform."),
            ("Spells & hero", "Rain fire on the enemy, freeze whole waves and call your captain to rally the troops at the right moment."),
        ]
        shots_title = "Screenshots"
    else:
        tag, lead = "Bald fürs iPhone", "Stell deine Armee zusammen, werte deine Helden auf und stürme die gegnerische Burg. Ein niedliches, aber taktisches Lane-Battle-Spiel – schnell gelernt, schwer gemeistert."
        cta = ("support.html", "Kontakt & Beta")
        features = [
            ("Schwarm-Schlachten", "Wellen aus Goblins, Orks und Untoten prallen auf deine Armee. Halte die Linie und brich durch, sobald der Kampfrausch beginnt."),
            ("Sammeln & aufsteigen", "Schalte Ritter, Magier, Samurai und mehr frei. Werte sie auf, gib ihnen Waffen mit Elementen und sieh zu, wie sie sich verwandeln."),
            ("Zauber & Held", "Lass Feuer regnen, friere ganze Wellen ein und ruf deinen Hauptmann im richtigen Moment aufs Feld."),
        ]
        shots_title = "Bilder aus dem Spiel"
    feats = "".join(f'<div class="feature"><h3>{h}</h3><p>{x}</p></div>' for h, x in features)
    shots = "".join(f'<img src="{p}img/{n}.jpg" alt="Bannerfall" loading="lazy" width="506" height="900">' for n in ["battle", "units", "unit", "cards"])
    body = f"""
<main>
<section class="hero">
<div>
<span class="tag">{tag}</span>
<h1>Bannerfall</h1>
<p class="lead">{lead}</p>
<div class="cta"><a class="btn gold" href="{cta[0]}">{cta[1]}</a></div>
</div>
<div class="phone"><img src="{p}img/battle.jpg" alt="Bannerfall" width="506" height="900"></div>
</section>
<section><div class="features">{feats}</div></section>
<section><h2>{shots_title}</h2><div class="shots">{shots}</div></section>
</main>"""
    if lang == "en":
        # Deutschsprachige Browser landen auf der deutschen Startseite (Link „English“ führt mit ?en zurück).
        body += '<script>if(!location.search.includes("en")&&(navigator.language||"").toLowerCase().startsWith("de"))location.replace("de/");</script>'
    page(lang, "index.html", "Bannerfall: Tiny Battle", body, lead)


def support(lang):
    if lang == "en":
        body = f"""<main class="doc">
<h1>Support</h1>
<p>Questions, feedback, a bug or a purchase problem? Write to <a href="mailto:{CONTACT}?subject=Bannerfall">{CONTACT}</a>. Please include your <strong>player ID</strong> (Settings in the game, shown at the bottom) and your device model.</p>
<h2>Frequently asked questions</h2>
<p><strong>I bought something but didn't receive it.</strong><br>Open Settings in the game and tap “Restore purchases”. If that doesn't help, email us with your player ID and the date of purchase.</p>
<p><strong>How do I move my progress to a new phone?</strong><br>On the old phone: Settings → “Transfer progress” → create a code. Enter the code on the new phone within 24 hours.</p>
<p><strong>How do I delete my data?</strong><br>Email us with your player ID and we'll delete your save, leaderboard entry and statistics. See also the <a href="privacy.html">privacy policy</a>.</p>
<p><strong>Can I join the beta?</strong><br>Yes! Send us a short email and we'll invite you to TestFlight.</p>
</main>"""
        title = "Support – Bannerfall"
    else:
        body = f"""<main class="doc">
<h1>Support</h1>
<p>Fragen, Feedback, ein Fehler oder ein Problem mit einem Kauf? Schreib an <a href="mailto:{CONTACT}?subject=Bannerfall">{CONTACT}</a>. Bitte gib deine <strong>Spieler-ID</strong> an (in den Einstellungen des Spiels ganz unten) und dein Gerätemodell.</p>
<h2>Häufige Fragen</h2>
<p><strong>Ich habe etwas gekauft, aber nicht erhalten.</strong><br>Öffne im Spiel die Einstellungen und tippe auf „Käufe wiederherstellen“. Hilft das nicht, schreib uns mit Spieler-ID und Kaufdatum.</p>
<p><strong>Wie nehme ich meinen Spielstand aufs neue Handy mit?</strong><br>Auf dem alten Handy: Einstellungen → „Spielstand übertragen“ → Code erstellen. Den Code innerhalb von 24 Stunden auf dem neuen Handy eingeben.</p>
<p><strong>Wie lösche ich meine Daten?</strong><br>Schreib uns mit deiner Spieler-ID, dann löschen wir Spielstand, Ranglisten-Eintrag und Statistik. Siehe auch die <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
<p><strong>Kann ich beim Betatest mitmachen?</strong><br>Ja! Schreib uns kurz, dann laden wir dich zu TestFlight ein.</p>
</main>"""
        title = "Support – Bannerfall"
    page(lang, "support.html", title, body)


ADDRESS = "Jakob Ehmann<br>Am Wald 7<br>8071 Hausmannstätten<br>Österreich / Austria"


def imprint(lang):
    if lang == "en":
        body = f"""<main class="doc">
<h1>Imprint</h1>
<p class="note">Information according to § 5 E-Commerce Act (ECG) and disclosure according to § 25 Media Act (MedienG), Austria.</p>
<h2>Provider</h2>
<p>{ADDRESS}</p>
<p>Email: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<h2>Business purpose</h2>
<p>Development and distribution of software (game “Bannerfall: Tiny Battle” for iOS).</p>
<h2>Editorial line (§ 25 MedienG)</h2>
<p>This website provides information about the game “Bannerfall: Tiny Battle” as well as the related legal texts and support contact.</p>
<h2>Online dispute resolution</h2>
<p>Consumers can submit complaints to the EU online dispute resolution platform: <a href="https://ec.europa.eu/consumers/odr">ec.europa.eu/consumers/odr</a>. You can also send complaints to the email address above.</p>
<h2>Copyright</h2>
<p>The contents of this website and the game (texts, graphics, design) are protected by copyright. Third-party graphics are used under license.</p>
</main>"""
        page(lang, "imprint.html", "Imprint – Bannerfall", body)
    else:
        body = f"""<main class="doc">
<h1>Impressum</h1>
<p class="note">Informationspflicht laut § 5 E-Commerce-Gesetz (ECG) und Offenlegung laut § 25 Mediengesetz (MedienG).</p>
<h2>Diensteanbieter</h2>
<p>{ADDRESS.replace(" / Austria", "")}</p>
<p>E-Mail: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<h2>Unternehmensgegenstand</h2>
<p>Entwicklung und Vertrieb von Software (Spiel „Bannerfall: Tiny Battle“ für iOS).</p>
<h2>Blattlinie / Offenlegung (§ 25 MedienG)</h2>
<p>Diese Website informiert über das Spiel „Bannerfall: Tiny Battle“ und stellt die zugehörigen Rechtstexte sowie Support-Kontaktmöglichkeiten bereit.</p>
<h2>Online-Streitbeilegung</h2>
<p>Verbraucher haben die Möglichkeit, Beschwerden an die Online-Streitbeilegungsplattform der EU zu richten: <a href="https://ec.europa.eu/consumers/odr">ec.europa.eu/consumers/odr</a>. Du kannst allfällige Beschwerden auch an die oben angegebene E-Mail-Adresse richten.</p>
<h2>Urheberrecht</h2>
<p>Die Inhalte dieser Website und des Spiels (Texte, Grafiken, Design) sind urheberrechtlich geschützt. Grafiken Dritter werden unter Lizenz verwendet.</p>
</main>"""
        page(lang, "impressum.html", "Impressum – Bannerfall", body)


def privacy(lang):
    if lang == "en":
        rows = [
            ("Random anonymous player ID (created by Firebase Authentication)", "Assigning your save game, protection against access by others", "Art. 6(1)(b) GDPR (providing the game)"),
            ("Save game (progress, units, resources, purchases in the game), chosen language", "Cloud backup, transfer to a new device", "Art. 6(1)(b) GDPR"),
            ("Player name you choose and number of cleared stages", "Display in the public leaderboard", "Art. 6(1)(b) GDPR"),
            ("Game events (e.g. battle won/lost, stage, unit levels, spells used, purchases made yes/no), platform, app version", "Improving difficulty and game balance", "Art. 6(1)(f) GDPR (legitimate interest in a fair, balanced game)"),
            ("Advertising data processed by Google AdMob (see section 4)", "Showing optional reward videos", "Art. 6(1)(a) GDPR (consent) for personalized ads; otherwise Art. 6(1)(f) GDPR"),
        ]
        table = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
        body = f"""<main class="doc">
<h1>Privacy Policy</h1>
<p class="note">For the iOS game “Bannerfall: Tiny Battle” and this website. Last updated: {UPDATED['en']}.</p>
<h2>1. Controller</h2>
<p>{ADDRESS}<br>Email: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<h2>2. Data processed by the game</h2>
<div class="table-scroll"><table><tr><th>Data</th><th>Purpose</th><th>Legal basis</th></tr>{table}</table></div>
<p>The game does <strong>not</strong> collect your real name, email address, phone number, contacts or precise location. The game does not ask for permission to track you across apps (App Tracking Transparency); the advertising identifier (IDFA) is therefore not available to the game or to AdMob. Please don't use your real name as player name.</p>
<h2>3. Google Firebase</h2>
<p>Save games, leaderboard entries and game events are stored with Google Firebase (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland) in the data center <strong>Frankfurt am Main (europe-west3)</strong>. Google acts as processor. A transfer to third countries cannot be completely ruled out for Google services; Google relies on the EU-US Data Privacy Framework and standard contractual clauses.</p>
<h2>4. Advertising (Google AdMob)</h2>
<p>The game offers optional reward videos (e.g. to double the reward after a battle). These are provided by Google AdMob (Google Ireland Limited). When an ad is requested or shown, Google processes data such as your IP address, device and app information, the app-specific vendor identifier and your interactions with the ad, to deliver ads, measure them and prevent fraud. In the EU/EEA, the UK and Switzerland the game asks for your <strong>consent</strong> before personalized ads are shown (consent dialog by Google). Without consent, only non-personalized ads are shown. You can change your choice at any time under Settings → “Privacy settings” in the game. If you buy “Ad-free”, no ad videos are shown. More: <a href="https://policies.google.com/technologies/partner-sites">How Google uses information from apps that use its services</a>.</p>
<h2>5. In-app purchases</h2>
<p>Purchases are processed exclusively by Apple (App Store). We do not receive your payment details; we only receive confirmation of which product was bought, to credit it in the game.</p>
<h2>6. Retention</h2>
<p>Save game, leaderboard entry and game events are stored as long as the player ID is used and deleted no later than 24 months after the last use. Transfer codes expire after 24 hours.</p>
<h2>7. Your rights</h2>
<p>You have the right to access, rectification, erasure, restriction of processing, data portability and objection (Art. 15–21 GDPR), and to withdraw your consent at any time with effect for the future. To delete your data, an email with your player ID (shown in the game's settings) to <a href="mailto:{CONTACT}">{CONTACT}</a> is enough. You also have the right to lodge a complaint with a supervisory authority, in Austria the Datenschutzbehörde (<a href="https://www.dsb.gv.at">dsb.gv.at</a>).</p>
<h2>8. Children</h2>
<p>The game is not directed at children under 13. In the EU, personalized advertising requires the consent of a parent or guardian for users under 16; younger players should not consent to personalized ads.</p>
<h2>9. This website</h2>
<p>This website is hosted by GitHub Pages (GitHub Inc., USA). When you visit it, GitHub processes technical access data (e.g. IP address) to deliver the page and for security. Fonts are loaded from Google Fonts (Google Ireland Limited), which also receives your IP address. The website does not use cookies or tracking.</p>
<h2>10. Changes</h2>
<p>We will update this privacy policy when the game or the law changes. The current version is always available on this page.</p>
</main>"""
        page(lang, "privacy.html", "Privacy Policy – Bannerfall", body)
    else:
        rows = [
            ("Zufällige, anonyme Spieler-Kennung (von Firebase Authentication erzeugt)", "Zuordnung des Spielstands, Schutz vor fremdem Zugriff", "Art. 6 Abs. 1 lit. b DSGVO (Bereitstellung des Spiels)"),
            ("Spielstand (Fortschritt, Einheiten, Ressourcen, Käufe im Spiel), gewählte Sprache", "Sicherung in der Cloud, Übertragung auf ein neues Gerät", "Art. 6 Abs. 1 lit. b DSGVO"),
            ("Selbst gewählter Spielername und Anzahl geschaffter Stufen", "Anzeige in der öffentlichen Rangliste", "Art. 6 Abs. 1 lit. b DSGVO"),
            ("Spielereignisse (z. B. Kampf gewonnen/verloren, Stufe, Einheiten-Level, genutzte Zauber, schon gekauft ja/nein), Plattform, App-Version", "Verbesserung von Schwierigkeit und Spielbalance", "Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einem fairen, ausgewogenen Spiel)"),
            ("Werbedaten, verarbeitet von Google AdMob (siehe Abschnitt 4)", "Anzeige freiwilliger Belohnungs-Videos", "Art. 6 Abs. 1 lit. a DSGVO (Einwilligung) für personalisierte Werbung, sonst Art. 6 Abs. 1 lit. f DSGVO"),
        ]
        table = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
        body = f"""<main class="doc">
<h1>Datenschutzerklärung</h1>
<p class="note">Für das iOS-Spiel „Bannerfall: Tiny Battle“ und diese Website. Stand: {UPDATED['de']}.</p>
<h2>1. Verantwortlicher</h2>
<p>{ADDRESS.replace(" / Austria", "")}<br>E-Mail: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<h2>2. Welche Daten das Spiel verarbeitet</h2>
<div class="table-scroll"><table><tr><th>Daten</th><th>Zweck</th><th>Rechtsgrundlage</th></tr>{table}</table></div>
<p>Das Spiel erhebt <strong>keine</strong> echten Namen, E-Mail-Adressen, Telefonnummern, Kontakte oder genauen Standortdaten. Das Spiel fragt nicht nach der Erlaubnis, dich app-übergreifend zu verfolgen (App Tracking Transparency); die Werbe-ID (IDFA) steht dem Spiel und AdMob daher nicht zur Verfügung. Bitte verwende keinen echten Namen als Spielernamen.</p>
<h2>3. Google Firebase</h2>
<p>Spielstände, Ranglisten-Einträge und Spielereignisse werden bei Google Firebase (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) im Rechenzentrum <strong>Frankfurt am Main (europe-west3)</strong> gespeichert. Google ist Auftragsverarbeiter. Eine Übermittlung in Drittländer kann bei Google-Diensten nicht vollständig ausgeschlossen werden; Google stützt sich dafür auf das EU-US Data Privacy Framework und Standardvertragsklauseln.</p>
<h2>4. Werbung (Google AdMob)</h2>
<p>Das Spiel bietet freiwillige Belohnungs-Videos an (z. B. um die Belohnung nach einem Kampf zu verdoppeln). Diese stammen von Google AdMob (Google Ireland Limited). Beim Anfordern und Anzeigen einer Anzeige verarbeitet Google Daten wie IP-Adresse, Geräte- und App-Informationen, die app-spezifische Hersteller-Kennung und deine Interaktionen mit der Anzeige, um Anzeigen auszuliefern, zu messen und Betrug zu verhindern. In der EU/im EWR, im Vereinigten Königreich und in der Schweiz fragt das Spiel vor personalisierter Werbung nach deiner <strong>Einwilligung</strong> (Einwilligungsdialog von Google). Ohne Einwilligung werden nur nicht personalisierte Anzeigen gezeigt. Deine Auswahl kannst du jederzeit im Spiel unter Einstellungen → „Datenschutz-Einstellungen“ ändern. Mit „Werbefrei“ werden keine Werbevideos angezeigt. Mehr dazu: <a href="https://policies.google.com/technologies/partner-sites?hl=de">Wie Google Daten aus Apps verwendet</a>.</p>
<h2>5. Käufe im Spiel</h2>
<p>Käufe werden ausschließlich von Apple (App Store) abgewickelt. Wir erhalten keine Zahlungsdaten, sondern nur die Bestätigung, welches Produkt gekauft wurde, um es im Spiel gutzuschreiben.</p>
<h2>6. Speicherdauer</h2>
<p>Spielstand, Ranglisten-Eintrag und Spielereignisse werden gespeichert, solange die Spieler-Kennung genutzt wird, und spätestens 24 Monate nach der letzten Nutzung gelöscht. Übertragungscodes verfallen nach 24 Stunden.</p>
<h2>7. Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch (Art. 15–21 DSGVO) sowie das Recht, eine Einwilligung jederzeit mit Wirkung für die Zukunft zu widerrufen. Für eine Löschung genügt eine E-Mail mit deiner Spieler-Kennung (in den Einstellungen des Spiels) an <a href="mailto:{CONTACT}">{CONTACT}</a>. Außerdem kannst du dich bei einer Aufsichtsbehörde beschweren, in Österreich bei der Datenschutzbehörde (<a href="https://www.dsb.gv.at">dsb.gv.at</a>).</p>
<h2>8. Kinder</h2>
<p>Das Spiel richtet sich nicht an Kinder unter 13 Jahren. In der EU braucht personalisierte Werbung bei Nutzern unter 16 Jahren die Zustimmung eines Elternteils oder Erziehungsberechtigten; jüngere Spieler sollten personalisierter Werbung nicht zustimmen.</p>
<h2>9. Diese Website</h2>
<p>Diese Website wird von GitHub Pages (GitHub Inc., USA) bereitgestellt. Beim Aufruf verarbeitet GitHub technische Zugriffsdaten (z. B. IP-Adresse), um die Seite auszuliefern und zur Sicherheit. Schriftarten werden von Google Fonts (Google Ireland Limited) geladen; dabei wird ebenfalls deine IP-Adresse übertragen. Die Website verwendet keine Cookies und kein Tracking.</p>
<h2>10. Änderungen</h2>
<p>Wir passen diese Datenschutzerklärung an, wenn sich das Spiel oder die Rechtslage ändert. Die aktuelle Fassung findest du immer auf dieser Seite.</p>
</main>"""
        page(lang, "datenschutz.html", "Datenschutzerklärung – Bannerfall", body)


for lang in ("en", "de"):
    home(lang)
    support(lang)
    imprint(lang)
    privacy(lang)
print("ok")
