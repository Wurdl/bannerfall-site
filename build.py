#!/usr/bin/env python3
"""Erzeugt die statischen Seiten von bannerfall-tinybattle.com (Englisch im Wurzelordner, Deutsch unter /de/).
Aufruf: python3 build.py  – danach committen und pushen (GitHub Pages)."""
import hashlib
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTACT = "ehmannjakob@gmail.com"
# Kennung der style.css im Link, damit Browser nach Änderungen nicht die alte Fassung aus dem Zwischenspeicher nehmen.
CSS_VERSION = hashlib.sha1(open(os.path.join(ROOT, "style.css"), "rb").read()).hexdigest()[:8]
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
<link rel="stylesheet" href="{p}style.css?v={CSS_VERSION}">
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



# Einheiten-Vorstellung: (id, Name DE, Name EN, Seltenheit 0–4, Fernkampf, Text DE, Text EN, [(Fähigkeit DE, EN, Text DE, Text EN)])
RARITY = {"de": ["Normal", "Selten", "Episch", "Legendär", "Mystisch"], "en": ["Common", "Rare", "Epic", "Legendary", "Mythic"]}
UNITS = [
    ("peasant", "Bauer", "Peasant", 0, False,
     "Billig, schnell auf dem Feld und in der Masse gefährlich. Mit der Mistgabel gegen alles, was kommt.",
     "Cheap, quick on the field and dangerous in numbers. Pitchfork versus everything.",
     [("Verstärkung", "Reinforcement", "Es kommen immer zwei Bauern", "Two peasants always come"),
      ("Dorfgemeinschaft", "Village Spirit", "+12 % Schaden für jeden Bauern in der Nähe", "+12 % damage for each nearby peasant")]),
    ("knight", "Ritter", "Knight", 0, False,
     "Der verlässliche Frontkämpfer. Hält die Linie und schlägt zurück.",
     "The reliable front-liner. Holds the line and strikes back.",
     [("Parade", "Parry", "Wehrt jeden 3. Hieb ab und schlägt sofort zurück", "Parries every 3rd blow and strikes back at once"),
      ("Kriegsbanner", "War Banner", "Verbündete in der Nähe machen 20 % mehr Schaden", "Nearby allies deal 20 % more damage")]),
    ("archer", "Bogenschütze", "Archer", 0, True,
     "Schießt aus der zweiten Reihe und holt auch Flieger vom Himmel.",
     "Shoots from the back row and brings down flyers too.",
     [("Salve", "Volley", "Jeder Schuss trifft einen zweiten Gegner", "Every shot hits a second enemy"),
      ("Pfeilregen", "Arrow Rain", "Jeder 4. Schuss lässt Pfeile auf ein ganzes Gebiet regnen", "Every 4th shot rains arrows on a whole area")]),
    ("spearman", "Speerträger", "Spearman", 0, False,
     "Stürmt mit Anlauf in die Gegner und durchbohrt ganze Reihen.",
     "Charges into the enemy and skewers whole lines.",
     [("Durchbohren", "Pierce", "Jeder 3. Stich trifft auch die Gegner dahinter", "Every 3rd thrust also hits the enemies behind"),
      ("Speerwurf", "Spear Throw", "Wirft einen Speer auf einen fernen Gegner", "Throws a spear at a distant enemy")]),
    ("mage", "Magier", "Mage", 0, True,
     "Feuer, Eis oder Blitz – der Magier macht Flächenschaden und setzt ganze Gruppen in Brand.",
     "Fire, ice or lightning – the mage deals area damage and sets whole groups on fire.",
     [("Feuerball", "Fireball", "Explodiert und setzt alle Getroffenen in Brand", "Explodes and sets everyone hit on fire"),
      ("Meteor", "Meteor", "Ein Meteor schlägt ein: dreifacher Flächenschaden", "A meteor strikes: triple area damage")]),
    ("monk", "Mönch", "Monk", 0, False,
     "Flink, zäh und schwer zu treffen. Heilt sich mitten im Kampf selbst.",
     "Quick, tough and hard to hit. Heals himself in the middle of the fight.",
     [("Schlaghagel", "Flurry", "Jeder 3. Angriff ist eine Serie aus drei Schlägen", "Every 3rd attack is a series of three blows"),
      ("Ausweichen", "Evasion", "Weicht jedem 4. Nahkampfhieb aus", "Dodges every 4th melee blow")]),
    ("priest", "Priester", "Priest", 0, True,
     "Hält deine Armee am Leben: Heilung, Schutzschilde und sogar Wiederauferstehung.",
     "Keeps your army alive: healing, shields and even resurrection.",
     [("Heilwelle", "Healing Wave", "Heilt alle Verbündeten ringsum", "Heals all allies around"),
      ("Wiederauferstehung", "Resurrection", "Gefallene Verbündete stehen wieder auf", "Fallen allies rise again")]),
    ("templar", "Grenzwächter", "Border Warden", 0, False,
     "Ein Schild auf zwei Beinen. Betäubt Gegner und schützt die Truppe vor Geschossen.",
     "A shield on two legs. Stuns enemies and protects the troops from projectiles.",
     [("Schildschlag", "Shield Bash", "Jeder 3. Schlag mit dem Schild betäubt", "Every 3rd shield blow stuns"),
      ("Schildmauer", "Shield Wall", "Verbündete nehmen 40 % weniger Schaden von Geschossen", "Allies take 40 % less damage from projectiles")]),
    ("hoplite", "Hoplit", "Hoplite", 1, False,
     "Bronzeschild und Speer: im Verbund kaum zu brechen, angeschlagen am gefährlichsten.",
     "Bronze shield and spear: almost unbreakable in formation, most dangerous when wounded.",
     [("Phalanx", "Phalanx", "Seite an Seite mit Verbündeten: 30 % weniger Schaden", "Side by side with allies: 30 % less damage"),
      ("Spartanischer Zorn", "Spartan Fury", "Greift schneller an, je weniger Leben er hat", "Attacks faster the less health he has")]),
    ("assassin", "Assassine", "Assassin", 1, False,
     "Schlägt aus dem Schatten zu, vergiftet und erledigt angeschlagene Gegner.",
     "Strikes from the shadows, poisons and finishes off wounded enemies.",
     [("Schattenschleier", "Shadow Veil", "Wird unsichtbar, der nächste Stich trifft dreifach", "Turns invisible, the next stab hits for triple damage"),
      ("Giftklinge", "Poison Blade", "Jeder Stich vergiftet, Gift stapelt sich", "Every stab poisons, poison stacks")]),
    ("berserker", "Berserker", "Berserker", 1, False,
     "Je länger der Kampf, desto wilder. Heilt sich durch Schaden und gibt nicht auf.",
     "The longer the fight, the wilder he gets. Heals through damage and never gives up.",
     [("Blutdurst", "Bloodthirst", "Heilt sich um 30 % des verursachten Schadens", "Heals for 30 % of the damage dealt"),
      ("Unsterbliche Wut", "Undying Rage", "Überlebt einen tödlichen Treffer", "Survives a lethal hit")]),
    ("dwarf", "Zwerg", "Dwarf", 1, False,
     "Klein, stur und mit einem Hammer, der den Boden beben lässt.",
     "Small, stubborn and armed with a hammer that shakes the ground.",
     [("Erdstoß", "Earth Shock", "Schaden und Betäubung ringsum", "Damage and stun all around"),
      ("Donnerhammer", "Thunder Hammer", "Ein Blitz springt auf drei Gegner über", "Lightning jumps to three enemies")]),
    ("shaman", "Schamane", "Shaman", 1, True,
     "Ruft Geisterblitze und Ahnenheilung, verhext und verlangsamt Gegner.",
     "Calls spirit lightning and ancestral healing, hexes and slows enemies.",
     [("Geisterblitz", "Spirit Bolt", "Springt auf drei weitere Gegner über", "Jumps to three more enemies"),
      ("Heiltotem", "Healing Totem", "Ein Totem heilt Verbündete ringsum", "A totem heals nearby allies")]),
    ("necromancer", "Nekromant", "Necromancer", 2, True,
     "Lässt Skelette für dich kämpfen und wird mit jedem gefallenen Gegner stärker.",
     "Makes skeletons fight for you and grows stronger with every fallen enemy.",
     [("Gruftruf", "Call of the Crypt", "Ruft ein Skelett neben dem Ziel herbei", "Summons a skeleton next to the target"),
      ("Totenheer", "Army of the Dead", "Zwei Skelette erheben sich", "Two skeletons rise")]),
    ("paladin", "Paladin", "Paladin", 2, False,
     "Heiliger Krieger: betäubt, heilt seine Verbündeten und ist kaum totzukriegen.",
     "Holy warrior: stuns, heals his allies and is hard to bring down.",
     [("Weihe", "Consecration", "Gegner brennen, Verbündete heilen", "Enemies burn, allies heal"),
      ("Hammer des Gerichts", "Hammer of Judgment", "Ein Lichthammer fällt: Flächenschaden und Betäubung", "A hammer of light falls: area damage and stun")]),
    ("druid", "Druidin", "Druid", 2, True,
     "Hält Gegner mit Wurzeln fest, ruft Mondfeuer und lässt Heilhaine wachsen.",
     "Holds enemies in place with roots, calls moonfire and grows healing groves.",
     [("Wurzelgriff", "Root Grip", "Wurzeln halten Gegner fest", "Roots hold enemies in place"),
      ("Mondfeuer", "Moonfire", "Ein Mondstrahl: +60 % Schaden, verlangsamt", "A moonbeam: +60 % damage, slows")]),
    ("samurai", "Samurai", "Samurai", 2, False,
     "Der Klingenmeister: ein Hieb, der Reihen spaltet, und tödlich gegen Angeschlagene.",
     "The blade master: one strike splits lines, deadly against the wounded.",
     [("Iaido", "Iaido", "Erster Hieb: doppelter Schaden und Rückstoß", "First blow: double damage and knockback"),
      ("Tausend Schnitte", "Thousand Cuts", "Schnitte durch bis zu fünf Gegner", "Cuts through up to five enemies")]),
    ("ent", "Uralter Ent", "Ancient Ent", 4, False,
     "Ein wandelnder Baumriese. Lässt den Boden beben, hält ganze Wellen mit Wurzeln fest und wächst nach.",
     "A walking giant tree. Shakes the ground, holds whole waves in place with roots and grows back.",
     [("Zorn des Waldes", "Wrath of the Forest", "Wurzeln brechen weit ringsum hervor", "Roots burst out far around"),
      ("Entwurzeln", "Uproot", "Packt das Ziel und schleudert es weit zurück", "Grabs the target and hurls it far back")]),
]

HOME = {
    "en": {
        "tag": "Coming soon to iPhone · Android to follow",
        "lead": "Build your army, upgrade your heroes and storm the enemy castle. A cute but tactical lane battle game – easy to pick up, hard to master.",
        "cta": [("support.html", "Join the beta", "gold"), ("#features", "Discover the game", "ghost")],
        "facts": [("18", "units to collect"), ("6", "worlds to conquer"), ("3", "spells to master"), ("1", "hero to lead them")],
        "how_title": "How a battle works",
        "how": [
            ("Pick your deck", "Choose up to six units before the battle – tanks up front, archers and mages behind."),
            ("Choose your cards", "Every level-up in battle offers three cards: new units, upgrades, abilities or spells. No two battles play the same."),
            ("Storm the castle", "Hold off the waves, break the enemy line and tear down their castle before yours falls."),
        ],
        "features_title": "What awaits you",
        "features": [
            ("battle", "Swarm battles", "Waves of goblins, orcs and the undead crash into your army. Hold the line, then break through when the battle frenzy begins and every castle takes extra damage."),
            ("spell", "Rain fire from the sky", "Time your spells: fire rain scorches whole groups, ice rain freezes waves in place, battle blessing drives your troops into a frenzy. Every spell grows stronger with you."),
            ("cards", "A new choice every level", "Each battle builds up differently. Do you bring in a new unit, make your samurai stronger or unlock a special ability? Rare epic choices can turn a lost battle around."),
            ("unit", "Collect, level up, ascend", "Find unit parts in battles and chests, level your units up and ascend them twice – they visibly transform and learn new abilities. Forge weapons with fire, ice, poison, lightning or light."),
            ("home", "A long campaign", "Fight through six worlds from green meadows to the land of the undead and beyond, with boss stages at the end of each chapter. Expand your village and test yourself in the boss dungeon."),
            ("victory", "Rewards that matter", "Every win brings gold, unit parts and materials. Daily quests, chests and the leaderboard keep you coming back for one more battle."),
        ],
        "fair_title": "Fair to play",
        "fair": [
            ("Free to play", "The whole campaign can be played without paying."),
            ("No forced ads", "Videos only when you choose them – for example to double a reward. Or buy “Ad-free” once."),
            ("No energy system", "Play as many battles as you like, whenever you like."),
            ("Your progress is safe", "Cloud backup and a transfer code for your next phone."),
        ],
        "shots_title": "Screenshots",
        "units_title": "Meet your army",
        "units_lead": "18 units, each with its own abilities – and every one transforms twice as it ascends. Tap a form to see it.",
        "forms": ["Base", "Ascension I", "Ascension II"],
        "ranged": ("Ranged", "Melee"),
        "prev": "Previous", "next": "Next",
        "shots": ["battle", "spell", "cards", "unit", "units", "home", "victory", "shop"],
        "faq_title": "Questions",
        "faq": [
            ("When does Bannerfall come out?", "We're currently testing the game with a small group of players on TestFlight. The App Store release follows once the feedback is in – follow along or join the beta."),
            ("Is there an Android version?", "Yes, Android is in the works and will follow shortly after the iPhone release."),
            ("Does the game cost anything?", "No. Bannerfall is free. There are optional purchases like gem packs, a battle pass and “Ad-free”, but everything can be reached by playing."),
            ("Which languages are supported?", "English and German. The game follows your device language and can be switched in the settings."),
            ("Who makes Bannerfall?", "Bannerfall is an indie game by Jakob Ehmann from Austria."),
        ],
        "end_title": "Want to play before everyone else?",
        "end_text": "Send a short email and we'll invite you to the TestFlight beta. Your feedback shapes the game.",
        "end_cta": "Join the beta",
    },
    "de": {
        "tag": "Bald fürs iPhone · Android folgt",
        "lead": "Stell deine Armee zusammen, werte deine Helden auf und stürme die gegnerische Burg. Ein niedliches, aber taktisches Lane-Battle-Spiel – schnell gelernt, schwer gemeistert.",
        "cta": [("support.html", "Beim Betatest mitmachen", "gold"), ("#features", "Spiel entdecken", "ghost")],
        "facts": [("18", "Einheiten zum Sammeln"), ("6", "Welten zum Erobern"), ("3", "Zauber zum Meistern"), ("1", "Held, der sie anführt")],
        "how_title": "So läuft ein Kampf",
        "how": [
            ("Deck wählen", "Nimm bis zu sechs Einheiten mit in den Kampf – vorne die Tanks, dahinter Bogenschützen und Magier."),
            ("Karten ziehen", "Bei jedem Stufenaufstieg im Kampf wählst du aus drei Karten: neue Einheiten, Verbesserungen, Fähigkeiten oder Zauber. Kein Kampf läuft gleich."),
            ("Burg stürmen", "Halte die Wellen auf, durchbrich die Linie des Gegners und reiß seine Burg nieder, bevor deine fällt."),
        ],
        "features_title": "Was dich erwartet",
        "features": [
            ("battle", "Schwarm-Schlachten", "Wellen aus Goblins, Orks und Untoten prallen auf deine Armee. Halte die Linie und brich durch, sobald der Kampfrausch beginnt und jede Burg mehr Schaden nimmt."),
            ("spell", "Feuer vom Himmel", "Setz deine Zauber im richtigen Moment: Feuerregen verbrennt ganze Gruppen, Eisregen friert Wellen ein, der Schlachtsegen treibt deine Truppen an. Jeder Zauber wächst mit dir."),
            ("cards", "Jede Stufe eine neue Wahl", "Jeder Kampf entwickelt sich anders. Holst du eine neue Einheit, machst du deinen Samurai stärker oder schaltest eine Spezialfähigkeit frei? Seltene epische Wahlen drehen auch verlorene Kämpfe."),
            ("unit", "Sammeln, aufwerten, aufsteigen", "Sammle Einheiten-Teile in Kämpfen und Truhen, werte deine Einheiten auf und lass sie zweimal aufsteigen – sie verwandeln sich sichtbar und lernen neue Fähigkeiten. Schmiede Waffen mit Feuer, Eis, Gift, Blitz oder Licht."),
            ("home", "Eine lange Kampagne", "Kämpf dich durch sechs Welten, von der grünen Wiese bis ins Land der Untoten und weiter, mit Bossstufen am Ende jedes Kapitels. Bau dein Dorf aus und stell dich dem Boss-Verlies."),
            ("victory", "Belohnungen, die zählen", "Jeder Sieg bringt Gold, Einheiten-Teile und Material. Tägliche Aufgaben, Truhen und die Rangliste sorgen für „nur noch einen Kampf“."),
        ],
        "fair_title": "Fair spielbar",
        "fair": [
            ("Kostenlos", "Die ganze Kampagne ist ohne Bezahlen spielbar."),
            ("Keine Zwangswerbung", "Videos nur, wenn du willst – etwa um eine Belohnung zu verdoppeln. Oder einmal „Werbefrei“ kaufen."),
            ("Kein Energiesystem", "Spiel so viele Kämpfe, wie du willst, wann du willst."),
            ("Dein Fortschritt ist sicher", "Sicherung in der Cloud und ein Übertragungscode fürs nächste Handy."),
        ],
        "shots_title": "Bilder aus dem Spiel",
        "units_title": "Deine Armee",
        "units_lead": "18 Einheiten mit eigenen Fähigkeiten – und jede verwandelt sich beim Aufstieg zweimal. Tippe auf eine Stufe, um sie zu sehen.",
        "forms": ["Basis", "Aufstieg I", "Aufstieg II"],
        "ranged": ("Fernkampf", "Nahkampf"),
        "prev": "Zurück", "next": "Weiter",
        "shots": ["battle", "spell", "cards", "unit", "units", "home", "victory", "shop"],
        "faq_title": "Fragen",
        "faq": [
            ("Wann erscheint Bannerfall?", "Gerade testen wir das Spiel mit einer kleinen Gruppe über TestFlight. Der Start im App Store folgt, sobald das Feedback eingearbeitet ist – mach mit beim Betatest."),
            ("Gibt es eine Android-Version?", "Ja, Android ist in Arbeit und folgt kurz nach dem iPhone-Start."),
            ("Kostet das Spiel etwas?", "Nein. Bannerfall ist kostenlos. Es gibt freiwillige Käufe wie Edelstein-Pakete, einen Kampfpass und „Werbefrei“, aber alles ist auch durchs Spielen erreichbar."),
            ("Welche Sprachen gibt es?", "Deutsch und Englisch. Das Spiel folgt der Sprache deines Geräts und lässt sich in den Einstellungen umstellen."),
            ("Wer steckt hinter Bannerfall?", "Bannerfall ist ein Indie-Spiel von Jakob Ehmann aus Österreich."),
        ],
        "end_title": "Willst du vor allen anderen spielen?",
        "end_text": "Schreib uns kurz, dann laden wir dich zum TestFlight-Betatest ein. Dein Feedback formt das Spiel.",
        "end_cta": "Beim Betatest mitmachen",
    },
}


def form_label(text):
    # Auf schmalen Bildschirmen nur „I“/„II“ zeigen, das Wort davor blendet die CSS aus.
    word, _, num = text.rpartition(" ")
    return f'<span class="long">{word} </span>{num}' if word else text


def home(lang):
    p = T[lang]["prefix"]
    h = HOME[lang]
    img = lambda n: f"{p}img/{lang}/{n}.jpg"
    beta = f"mailto:{CONTACT}?subject=" + ("Bannerfall%20Beta" if lang == "en" else "Bannerfall%20Betatest")
    ctas = "".join(f'<a class="btn {kind}" href="{beta if href == "support.html" else href}">{label}</a>' for href, label, kind in h["cta"])
    facts = "".join(f'<div class="fact"><b>{n}</b><span>{t}</span></div>' for n, t in h["facts"])
    how = "".join(f'<li class="step"><span class="num">{i + 1}</span><h3>{t}</h3><p>{x}</p></li>' for i, (t, x) in enumerate(h["how"]))
    feats = "".join(
        f'<article class="row{" flip" if i % 2 else ""}"><div class="shot"><img src="{img(n)}" alt="{t}" loading="lazy" width="720" height="1280"></div>'
        f'<div class="copy"><h3>{t}</h3><p>{x}</p></div></article>'
        for i, (n, t, x) in enumerate(h["features"])
    )
    fair = "".join(f'<div class="feature"><h3>{t}</h3><p>{x}</p></div>' for t, x in h["fair"])
    shots = "".join(f'<img src="{img(n)}" alt="Bannerfall" loading="lazy" width="720" height="1280">' for n in h["shots"])
    lang_i = 0 if lang == "de" else 1
    cards = []
    for uid, n_de, n_en, rar, ranged, t_de, t_en, abil in UNITS:
        name = n_de if lang == "de" else n_en
        forms = "".join(
            f'<button type="button" class="form{" on" if t == 0 else ""}" data-src="{p}img/units/{uid}_{t}.png" aria-pressed="{"true" if t == 0 else "false"}">{form_label(h["forms"][t])}</button>'
            for t in range(3))
        abils = "".join(f'<li><b>{a[lang_i]}</b> <span>{a[2 + lang_i]}</span></li>' for a in abil)
        cards.append(
            f'<article class="unit r{rar}"><div class="pic"><img src="{p}img/units/{uid}_0.png" alt="{name}" loading="lazy" width="360" height="360"></div>'
            f'<div class="forms">{forms}</div>'
            f'<div class="meta"><span class="rar">{RARITY[lang][rar]}</span><span class="kind">{h["ranged"][0 if ranged else 1]}</span></div>'
            f'<h3>{name}</h3><p>{t_de if lang == "de" else t_en}</p><ul>{abils}</ul></article>')
    units = "".join(cards)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in h["faq"])
    body = f"""
<main>
<section class="hero">
<div>
<span class="tag">{h["tag"]}</span>
<h1>Bannerfall</h1>
<p class="sub">Tiny Battle</p>
<p class="lead">{h["lead"]}</p>
<div class="cta">{ctas}</div>
</div>
<div class="phones">
<div class="phone back"><img src="{img("spell")}" alt="" width="720" height="1280"></div>
<div class="phone"><img src="{img("battle")}" alt="Bannerfall" width="720" height="1280"></div>
</div>
</section>
<section class="facts">{facts}</section>
<section class="slider"><div class="slider-head"><h2>{h["shots_title"]}</h2><div class="arrows"><button type="button" class="arrow" data-dir="-1" aria-label="{h["prev"]}">‹</button><button type="button" class="arrow" data-dir="1" aria-label="{h["next"]}">›</button></div></div><div class="gallery">{shots}</div></section>
<section><h2>{h["how_title"]}</h2><ol class="steps">{how}</ol></section>
<section id="features"><h2>{h["features_title"]}</h2><div class="rows">{feats}</div></section>
<section id="units"><h2>{h["units_title"]}</h2><p class="section-lead">{h["units_lead"]}</p><div class="units">{units}</div></section>
<section><h2>{h["fair_title"]}</h2><div class="features four">{fair}</div></section>
<section class="faq"><h2>{h["faq_title"]}</h2>{faq}</section>
<section class="final"><h2>{h["end_title"]}</h2><p>{h["end_text"]}</p><a class="btn gold" href="{beta}">{h["end_cta"]}</a></section>
</main>"""
    # Slider: Pfeile blättern eine Bildbreite weiter, mit der Maus lässt er sich ziehen.
    # Einheiten: Klick auf eine Stufe tauscht das Bild.
    body += """<script>
document.querySelectorAll('.slider').forEach(function (s) {
  var g = s.querySelector('.gallery');
  s.querySelectorAll('.arrow').forEach(function (b) {
    b.addEventListener('click', function () {
      var step = g.querySelector('img').getBoundingClientRect().width + 14;
      var dir = +b.dataset.dir;
      var end = g.scrollWidth - g.clientWidth - 2;
      if (dir > 0 && g.scrollLeft >= end) g.scrollTo({left: 0, behavior: 'smooth'});
      else if (dir < 0 && g.scrollLeft <= 2) g.scrollTo({left: end + 2, behavior: 'smooth'});
      else g.scrollBy({left: dir * step * 2, behavior: 'smooth'});
    });
  });
  var down = false, x0 = 0, l0 = 0, moved = false;
  g.addEventListener('pointerdown', function (e) {
    if (e.pointerType !== 'mouse') return;
    down = true; moved = false; x0 = e.clientX; l0 = g.scrollLeft; g.classList.add('drag');
  });
  window.addEventListener('pointermove', function (e) {
    if (!down) return;
    if (Math.abs(e.clientX - x0) > 4) moved = true;
    g.scrollLeft = l0 - (e.clientX - x0);
  });
  window.addEventListener('pointerup', function () { if (down) { down = false; g.classList.remove('drag'); } });
  g.addEventListener('dragstart', function (e) { e.preventDefault(); });
});
document.querySelectorAll('.unit').forEach(function (u) {
  var img = u.querySelector('.pic img');
  u.querySelectorAll('.form').forEach(function (b) {
    b.addEventListener('click', function () {
      u.querySelectorAll('.form').forEach(function (o) { o.classList.remove('on'); o.setAttribute('aria-pressed', 'false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      img.src = b.dataset.src;
    });
  });
});
</script>"""
    if lang == "en":
        # Deutschsprachige Browser landen auf der deutschen Startseite (Link „English“ führt mit ?en zurück).
        body += '<script>if(!location.search.includes("en")&&(navigator.language||"").toLowerCase().startsWith("de"))location.replace("de/");</script>'
    page(lang, "index.html", "Bannerfall: Tiny Battle", body, h["lead"])


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
