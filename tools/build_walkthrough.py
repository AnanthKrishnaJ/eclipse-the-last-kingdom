"""Build the walkthrough from docs/walkthrough.json and docs/heroine_events.json.

    node tools/heroine_events.js      # refresh heroine data from eclipse.html
    node tools/realm_list.js          # refresh the Realms of Aurel list
    python tools/build_walkthrough.py

Writes walkthrough.pdf at the repo root.
Requires: pip install reportlab
"""
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "docs" / "walkthrough.json").read_text(encoding="utf-8"))
HER = json.loads((ROOT / "docs" / "heroine_events.json").read_text(encoding="utf-8"))
REALM = json.loads((ROOT / "docs" / "realms.json").read_text(encoding="utf-8"))

INK, GOLD, GOLD_D, PAPER, NIGHT, MUTE, RULE = (HexColor(c) for c in
                                               ("#2e2014", "#c9a24a", "#8a6a2e", "#f4ead2", "#0b0a10", "#6a5030", "#c8b080"))
W, H = A4
LM = RM = 24 * mm
CW = W - LM - RM  # text column width

S = {
    "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=21, leading=25, textColor=HexColor("#4a2410"), spaceAfter=1),
    "kick": ParagraphStyle("kick", fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=GOLD_D, spaceBefore=1, spaceAfter=3),
    "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=13, leading=16, textColor=INK, spaceBefore=9, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Times-Roman", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6, alignment=TA_JUSTIFY),
    "li": ParagraphStyle("li", fontName="Times-Roman", fontSize=10.5, leading=14, textColor=INK, leftIndent=13, bulletIndent=2,
                         spaceAfter=3, alignment=TA_LEFT),
    "td": ParagraphStyle("td", fontName="Times-Roman", fontSize=9.6, leading=12.4, textColor=INK, alignment=TA_LEFT),
    "tk": ParagraphStyle("tk", fontName="Times-Bold", fontSize=9.6, leading=12.4, textColor=HexColor("#4a2410"), alignment=TA_LEFT),
    "cap": ParagraphStyle("cap", fontName="Times-Italic", fontSize=9, leading=11.5, textColor=MUTE, alignment=TA_CENTER, spaceAfter=8),
    "tip": ParagraphStyle("tip", fontName="Times-Italic", fontSize=10, leading=13.5, textColor=INK, alignment=TA_LEFT),
    "quote": ParagraphStyle("quote", fontName="Times-Italic", fontSize=10, leading=13.5, textColor=MUTE, leftIndent=10, spaceAfter=6),
    "toc0": ParagraphStyle("toc0", fontName="Times-Roman", fontSize=11.5, leading=17, textColor=INK),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- page furniture ----------
def cover(c, doc):
    c.saveState()
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cx, cy = W / 2, H * .64
    for r, col in ((132, "#24140a"), (118, "#3a1e0c"), (104, "#7a4214"), (92, "#e3923f"), (86, "#f6c46d")):
        c.setFillColor(HexColor(col))
        c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#050407"))
    c.circle(cx, cy, 82, fill=1, stroke=0)
    c.setFillColor(HexColor("#f1d48a"))
    c.setFont("Times-Bold", 50)
    c.drawCentredString(cx, H * .38, "ECLIPSE")
    c.setFont("Times-Bold", 17)
    c.drawCentredString(cx, H * .38 - 30, "THE LAST KINGDOM")
    c.setStrokeColor(GOLD)
    c.setLineWidth(.8)
    c.line(cx - 140, H * .38 - 46, cx + 140, H * .38 - 46)
    c.setFillColor(HexColor("#cbb88e"))
    c.setFont("Helvetica", 11)
    c.drawCentredString(cx, H * .38 - 66, DATA["subtitle"])
    c.setFont("Helvetica", 8.5)
    c.setFillColor(HexColor("#8a7a5e"))
    c.drawCentredString(cx, 30 * mm, "Story, bosses, side quests, every heroine event and married life")
    c.restoreState()


def page(c, doc):
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD_D)
    c.setLineWidth(1.4)
    c.rect(12 * mm, 12 * mm, W - 24 * mm, H - 24 * mm, fill=0, stroke=1)
    c.setLineWidth(.4)
    c.rect(14 * mm, 14 * mm, W - 28 * mm, H - 28 * mm, fill=0, stroke=1)
    c.setFillColor(MUTE)
    c.setFont("Helvetica", 7.2)
    c.drawString(LM, 17 * mm, "ECLIPSE: THE LAST KINGDOM  ·  WALKTHROUGH")
    c.drawRightString(W - RM, 17 * mm, str(doc.page))
    c.setStrokeColor(RULE)
    c.setLineWidth(.4)
    c.line(LM, 20.5 * mm, W - RM, 20.5 * mm)
    c.restoreState()


class Doc(BaseDocTemplate):
    def afterFlowable(self, f):
        if getattr(f, "_toc", None):
            self.notify("TOCEntry", (0, f._toc, self.page))


# ---------- blocks ----------
def tbl(rows, kw=46 * mm, head=None):
    data = [[Paragraph(esc(k), S["tk"]), Paragraph(esc(v), S["td"])] for k, v in rows]
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), .4, RULE),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("ROWBACKGROUNDS", (0, 0), (-1, -1), [HexColor("#efe3c2"), PAPER])]
    if head:
        data.insert(0, [Paragraph(f'<font color="#f4ead2">{esc(head[0])}</font>', S["tk"]),
                        Paragraph(f'<font color="#f4ead2"><b>{esc(head[1])}</b></font>', S["td"])])
        st += [("BACKGROUND", (0, 0), (-1, 0), HexColor("#6a4a2a")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#efe3c2"), PAPER])]
    t = Table(data, colWidths=[kw, CW - kw], hAlign="LEFT", repeatRows=1 if head else 0)
    t.setStyle(TableStyle(st))
    return [t, Spacer(1, 7)]


def h2(title):
    return [CondPageBreak(48 * mm), Paragraph(esc(title), S["h2"])]


def tip(text, label="Tip."):
    t = Table([[Paragraph(f"<b>{label}</b> " + esc(text), S["tip"])]], colWidths=[CW], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HexColor("#e8d9b0")),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.5, GOLD),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return [Spacer(1, 2), t, Spacer(1, 8)]


def block_flow(b):
    if "img" in b:
        path = ROOT / b["img"]
        iw, ih = ImageReader(str(path)).getSize()
        k = min((CW - 8) / iw, 92 * mm / ih)
        im = Image(str(path), width=iw * k, height=ih * k)
        frame = Table([[im]], colWidths=[iw * k + 6], hAlign="CENTER")
        frame.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, GOLD_D), ("BACKGROUND", (0, 0), (-1, -1), NIGHT),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return [Spacer(1, 3), KeepTogether([frame, Spacer(1, 3), Paragraph(esc(b.get("cap", "")), S["cap"])])]
    if "p" in b:
        return [Paragraph(esc(b["p"]), S["p"])]
    if "h" in b:
        return h2(b["h"])
    if "list" in b:
        return [Paragraph(esc(x), S["li"], bulletText="•") for x in b["list"]] + [Spacer(1, 4)]
    if "tip" in b:
        return tip(b["tip"])
    if "table" in b:
        return tbl(b["table"])
    raise ValueError(b)


def section(title, kicker, flows, new_page=True):
    h = Paragraph(esc(title), S["h1"])
    h._toc = title
    head = [h, Paragraph(esc(kicker).upper() or "&nbsp;", S["kick"]),
            HRFlowable(width="100%", thickness=.8, color=GOLD, spaceBefore=1, spaceAfter=8)]
    out = [PageBreak()] if new_page else [CondPageBreak(95 * mm), Spacer(1, 6)]
    return out + [KeepTogether(head + flows[:1])] + flows[1:]


# ---------- heroine chapters ----------
STAGES = [("1. Stranger", "You have not spoken yet."), ("2. Acquaintance", "Talk to her once."),
          ("3. Friendship", "Friendship 30."), ("4. Close friendship", "Friendship 55 and affection 35. Dates unlock."),
          ("5. Romantic interest", "Close friendship and affection 50. Hearts float around her when she walks beside you."),
          ("6. Confession", "She said yes to your confession."), ("7. Dating", "One date after the confession."),
          ("8. Engagement", "She accepted the Promise Ring."), ("9. Marriage", "The wedding is held; she moves into your cottage."),
          ("10. Married life", "Seven days after the wedding.")]


def heroine_intro():
    f = [Paragraph("Four heroines live in Aurel. Each glows in her own colour (Mimi gold, Lyra ice-blue, Serah red, Noelle violet) "
                   "so you can find her in a crowd. Bonds are measured in friendship, trust and affection, each from 0 to 100, "
                   "and the Bonds tab in your journal shows all three, her ten-stage track and a diary of what you did together.", S["p"]),
         ] + h2("Daily actions")
    f += tbl([("Chat (once a day)", "She raises a topic with three answers. Every chat gives +2 friendship; once friendship is 20, "
                                    "a trust or friendship answer also gives +1 affection. Topics rotate in a fixed order."),
              ("Give a gift (once a day)", "Loved: +8 affection, +4 friendship. Liked: +4 / +2. Neutral: +1 / +1. Disliked: -5 affection, "
                                           "-1 friendship. Before she counts you as a friend, a gift gives at most +3 affection. "
                                           "Her reaction is recorded, so the gift list shows her taste next time."),
              ("Ask about her", "Below friendship 20 she talks about home. At 20 or more she tells you her past: +3 trust, written in the diary."),
              ("Ask her on a date (once a day)", "Needs Close friendship. Each date passes two hours. The first good answer at each "
                                                 "place unlocks a gallery scene."),
              ("Personal request", "At friendship 30 she says \"Is something on your mind?\" and gives her personal quest.")])
    f += h2("The ten bond stages")
    f += tbl(STAGES, head=("Stage", "How to reach it"))
    f += h2("Date places")
    f += tbl([("Sakura Hill, Plaza café, Riverside", "Always available."),
              ("Flower garden, Lakeside", "Always available."),
              ("Picnic in Dawnmeadow", "Uses one Honey Cake or Duskberry Tart from your bag (+3 affection on top)."),
              ("Stargazing", "Only at night."), ("Evening walk", "Only from 17:00.")])
    return f


def heroine_chapter(h):
    f = [Paragraph(esc(h["bio"]), S["p"])]
    f += tbl([("Age", str(h["age"])), ("Goal", h["goal"]), ("Flaw", h["flaw"]), ("Where to find her", h["where"]),
              ("Joining the party", h["join"]), ("Special in battle", h["special"])])
    if h["meet"]:
        m = h["meet"]
        f += h2("Event: first meeting")
        f += tbl([(f'"{m[0]}"', m[1]), (f'"{m[2]}"', m[3])], head=("Your answer", "Result"))
    else:
        f += h2("Event: first meeting")
        f.append(Paragraph("Talking to her the first time registers you with the guild at rank F. "
                           "From then on she also takes your bounty reports (\"Report bounties\").", S["p"]))
    f += h2("Gifts")
    f += tbl(h["gifts"])
    f += h2("Chat topics, in the order she raises them")
    f += tbl([(f"Topic {i + 1}", f"“{t}” {b}") for i, (t, b) in enumerate(h["topics"])], kw=20 * mm)
    f += h2("Event: personal quest")
    f += tbl(h["quest"], kw=24 * mm)
    f += h2("Event: dates (best answer at each place)")
    f += tbl(h["dates"], kw=44 * mm)
    f += h2("Romance events")
    f += tbl([("Lantern Festival", "Day 14 of any season, 17:00 to midnight, at Close friendship or higher: "
                                   "\"Enjoy the Lantern Festival together\". Answer \"I wished for another year of this.\" for +10 affection and a scene."),
              ("Confession", "Close friendship, affection 70, trust 60, her personal quest finished and at least one date. "
                             "Choose \"Tell her how you feel\" and answer \"I love you\". She says: “" + h["confess"] + "”"),
              ("First kiss", "While dating, after two dates since the confession, a scene starts when the date ends: “" + h["kiss"] +
               "” \"Lean in\" gives +8 affection; \"Take her hand instead\" gives +3."),
              ("Proposal", "Dating and affection 90, with a Promise Ring (500 gold from Odile): “" + h["propose"] + "”"),
              ("Wedding", "Talk to her while engaged and choose \"Plan the wedding\". Elder Maren holds the ceremony in the plaza: “" + h["wed"] + "”"),
              ("Evening together", "At home after 17:00 she asks: “" + h["eve"][0] + "” Best answer: \"" + h["eve"][1] + "\""),
              ("Anniversary", "Every 28 days after the wedding, on waking, a lakeside scene: “" + h["anniv"] + "” +8 affection and a Silk Ribbon.")],
             kw=34 * mm)
    return f


def shared_chapter():
    f = [Paragraph("These events involve more than one heroine, or happen once you share a home.", S["p"]),
         ] + h2("Two hearts: a second partner") + [
         Paragraph("If you are already dating, engaged to or married to one heroine and try to confess to another, a scene starts "
                   "with your current partner first. Tell her the truth: she agrees only with trust 75 and affection 80. "
                   "Otherwise she refuses (-8 affection, -5 trust), and you can try again once the bond is stronger.", S["p"])] + h2("Campfire talks") + [
         Paragraph("Rest at a lantern with two or more heroines in your party. Once a day a campfire scene can play; each scene plays once "
                   "and needs every heroine named below in your party.", S["p"])]
    f += tbl(HER["shared"]["camp"], kw=40 * mm, head=("Party", "Opening line and choices"))
    f += h2("Banter on the road")
    f.append(Paragraph("With two or more companions, a short exchange plays every 70 to 110 seconds outside boss fights.", S["p"]))
    f += tbl(HER["shared"]["banter"], kw=40 * mm)
    f += h2("Companion reactions")
    f += tbl([("Greeting", "Each companion greets you once a day. The greeting grows warmer with the bond."),
              ("Rain, nightfall, low health", "A companion comments, and warns you when your health drops below 30%."),
              ("Treasure nearby", "A companion spots an unopened chest within range and it flashes gold."),
              ("Level up", "A companion congratulates you.")], kw=40 * mm)
    f += h2("Married life")
    f += tbl([("Her day", "From 09:00 to 19:00 she works at her usual spot; in the evening and in heavy rain she is at your cottage."),
              ("Share a meal", "At home, once a day. Restores health and mana; +5 affection if you share a Honey Cake, Duskberry Tart or Moonleaf Tea, otherwise +3."),
              ("Evening together", "At home after 17:00, once a day. One question with a best answer (see her chapter)."),
              ("Goodnight", "Sleeping at home plays a short goodnight line (+1 affection)."),
              ("Morning gift", "Each morning there is a 35% chance she leaves a Honey Cake, Moonleaf Tea, Duskberry Tart or Sunbell Bouquet."),
              ("Anniversary", "Every 28 days after the wedding: scene, +8 affection and a Silk Ribbon.")], kw=40 * mm)
    return f


# ---------- Realms of Aurel ----------
BIOME_NAME = {"meadow": "Farmland", "autumn": "Autumn forest", "swamp": "Swamp", "desert": "Desert", "coast": "Coast", "highland": "Highlands",
              "snow": "Snowfields", "jungle": "Jungle", "ash": "Volcanic ash", "crystal": "Crystal plains", "dusk": "Twilight moor", "void": "Void rift"}
FOE_NAME = {"slime": "Bog Slimes", "venom": "Venom Slimes", "wolf": "Ashen Wolves", "goblin": "Gloomfang Goblins", "skeleton": "Barrow Skeletons",
            "mage": "Umbral Acolytes", "puff": "Puffcaps", "beetle": "Horn Beetles"}


def grid(rows, widths, head):
    data = [[Paragraph(f'<font color="#f4ead2"><b>{esc(h)}</b></font>', S["td"]) for h in head]]
    data += [[Paragraph(esc(str(c)), S["tk"] if j == 0 else S["td"]) for j, c in enumerate(r)] for r in rows]
    t = Table(data, colWidths=[w * CW for w in widths], hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), .4, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), HexColor("#6a4a2a")),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#efe3c2"), PAPER]),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]))
    return [t, Spacer(1, 7)]


def realm_intro():
    f = [Paragraph("Beyond Solmere and Eldoria lie the twelve provinces of Aurel: 108 cities, each with its own wilds and its own boss. "
                   "They are optional, open as soon as you can reach a waystone, and run from level 4 to level 50.", S["p"])]
    f += h2("Waystones")
    f.append(Paragraph("A glowing waystone stands in the plaza of Solmere, of Eldoria and of every city in the provinces. Touch one to open the "
                       "travel list and pick any city of an open province, or return to Solmere or Eldoria. A province opens once you have "
                       "defeated three bosses in the province before it; the first, the Greenreach, is always open.", S["p"]))
    f += h2("What every city has")
    f += tbl([("Adventurers' Guild", "The same bounty board and rank card as in Eldoria."),
              ("Inn", "Talk to the keeper for a free night: full health and mana."),
              ("Temple", "A priest heals you and clears poison and other ailments."),
              ("Smithy", "Sells the province's own gear and the gear of the province before it, plus Iron Sword, Chain Mail and Greater "
                         "Potions. You can forge and upgrade here."),
              ("Tavern, apothecary, general store", "Food, potions and supplies, as in Solmere."),
              ("Lantern", "Rest to heal and to set your respawn point."),
              ("Notice board", "Names the boss of the wilds and its reward."),
              ("Townsfolk", "Nine people of many peoples walk the streets, each with lines about the city and its boss.")], kw=40 * mm)
    f += h2("The wilds")
    f.append(Paragraph("Leave by the south gate. A lantern stands just inside the wilds. A road winds south to the boss lair, a ring of torches "
                       "and bones; stepping inside wakes the boss and seals the ring. Around eighteen monsters of the province roam the wilds, "
                       "and three chests hold gold and potions. In every third city the first chest also holds a piece of province gear.", S["p"]))
    f += h2("Boss families and how to beat them")
    f.append(Paragraph("No two of the 108 bosses are the same. Each has one of six bodies, its own colours and size, two adornments "
                       "(wings, crown, halo, shoulder flames, spikes, orbiting runes, a tail or chains) and two signature moves of its own.", S["p"]))
    f += tbl([("Warlords", "Orc, troll, ogre, gnoll, lizard, demon, frost giant and cinder brute. Cleaver swing at close range: dodge sideways. "
                           "Charge along a marked line: sidestep, and if it hits a wall it is stunned. Leap slam onto a marked circle. "
                           "Below half health it rages: a spinning attack, and it calls two goblins."),
              ("Beasts", "Wolves, drakes, boars, bears, lions and stags. They fight like warlords: a lunging bite, a charge, a pounce "
                         "and a tail sweep, and they howl for help below half health."),
              ("Knights", "Fallen, rime, bone, gilded, blood, thorn, shade and dune knights. The shield blocks every hit from the front, "
                          "so circle behind it. A three-hit mace combo, a shield bash along a line (it staggers if it hits a wall) "
                          "and a quake of rock circles in a line. Below half health the visor burns red and it moves faster."),
              ("Golems", "Stone, wood, ice, magma, crystal, iron and bone. They fight like knights, with fists, a shoulder charge and a "
                         "ground quake, and their armoured front blocks hits too: strike from behind."),
              ("Sorcerers", "Hollow kings, liches, frost witches, ember lords, tide priests, void prophets, sand pharaohs and bloom witches. "
                            "Fans of crystal shards, crystal rain on marked circles and rings of light: keep moving. Below 60% health it adds a "
                            "spiral of shards and blinks around the ring; below 28% it summons two acolytes."),
              ("Spirits", "Watchers, flame wisps, abyssal jellies and masked spirits. They float and fight like sorcerers.")], kw=26 * mm)
    f += h2("Signature moves")
    f += tbl([("Ring of Force", "An expanding ring: step through it, not away from it."), ("Shard Burst", "Twelve shards in every direction: stand between them."),
              ("Meteor Fall", "Five marked circles around you: leave them."), ("Starfall", "Eight circles anywhere in the ring."),
              ("Call Minions", "Two monsters of the province join the fight."), ("Shadow Step", "It appears beside you and a short ring follows."),
              ("Regenerate", "Heals 6% of its health: interrupt it with damage."), ("Ward", "Immune to damage for about two seconds."),
              ("Cross Blast", "Four lines of circles in a cross from the boss."), ("Vortex", "Pulls you toward it: dodge outward."),
              ("Seeker Orbs", "Three volleys of three orbs aimed at you."), ("Frenzy", "Moves 50% faster for four seconds."),
              ("Ring Quake", "A ring of circles around the boss: stay out of arm's reach."), ("Earth Lances", "A fast line of circles toward you: sidestep.")], kw=34 * mm)
    f += h2("Province gear")
    rows = []
    for P in REALM["provinces"]:
        L = P["lvl"] + 2
        tag = P["name"][4:] if P["name"].startswith("The ") else P["name"]
        rows.append((tag, f"ATK {round(10 + L * .9)}", f"ATK {round(5 + L * .45)}, MAG {round(6 + L * .6)}",
                     f"DEF {round(6 + L * .55)}, HP +{20 + L * 3}", f"HP +{10 + L * 2}, MP +{10 + L}", f"{150 + L * 45} g"))
    f.append(Paragraph("Each province has a Longsword, a Staff, a Mail and a Charm. Its bosses drop one of the four, and its smiths sell them.", S["p"]))
    f += grid(rows, [.22, .12, .2, .19, .17, .1], ["Province", "Longsword", "Staff", "Mail", "Charm", "Price"])
    f += h2("The twelve provinces")
    f += grid([(P["name"], BIOME_NAME[P["biome"]], f'{P["lvl"]} to {P["lvl"] + 2}', ", ".join(FOE_NAME.get(x, x) for x in P["foes"]),
                "Always open" if i == 0 else "3 bosses in " + REALM["provinces"][i - 1]["name"]) for i, P in enumerate(REALM["provinces"])],
              [.22, .14, .1, .3, .24], ["Province", "Land", "Level", "Monsters", "Opens after"])
    return f


def province_chapter(P):
    f = [Paragraph(f'{BIOME_NAME[P["biome"]]}. Levels {P["lvl"]} to {P["lvl"] + 2}. Monsters: '
                   + ", ".join(FOE_NAME.get(x, x) for x in P["foes"]) + ".", S["p"])]
    f += grid([(c["city"], c["boss"] + ", " + c["role"], c["lvl"], f'{c["hp"]} / {c["atk"]:g} / {c["def"]}', " and ".join(c["sig"]), f'{c["xp"]} XP, {c["gold"]} g')
               for c in P["cities"]], [.14, .27, .06, .16, .21, .16], ["City", "Boss", "Lv", "HP / ATK / DEF", "Signature moves", "Reward"])
    f.append(Paragraph("Each boss waits at the end of the road through its city's wilds: " + ", ".join(c["wild"] for c in P["cities"]) + ".", S["cap"]))
    return f


# ---------- build ----------
def build_pdf(out):
    doc = Doc(str(out), pagesize=A4, title="Eclipse: The Last Kingdom — Walkthrough", author="Ananth Krishna J",
              leftMargin=LM, rightMargin=RM, topMargin=24 * mm, bottomMargin=25 * mm)
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f", leftPadding=0, rightPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [fr], onPage=cover), PageTemplate("page", [fr], onPage=page)])
    toc = TableOfContents(dotsMinLevel=0)
    toc.levelStyles = [S["toc0"]]
    story = [NextPageTemplate("page"), PageBreak(), Paragraph("Contents", S["h1"]),
             HRFlowable(width="100%", thickness=.8, color=GOLD, spaceBefore=4, spaceAfter=10), toc]
    for s in DATA["sections"]:
        if s.get("generated") == "realms":
            story += section("The Realms of Aurel", "108 cities, 108 bosses, twelve provinces", realm_intro())
            for P in REALM["provinces"]:
                story += section(P["name"], f'{BIOME_NAME[P["biome"]]} · levels {P["lvl"]} to {P["lvl"] + 2}', province_chapter(P), new_page=False)
            continue
        if s.get("generated") == "heroines":
            story += section("The Heroines", "Bonds, stages and dates", heroine_intro())
            for h in HER["heroines"]:
                story += section(h["name"], h["title"], heroine_chapter(h))
            story += section("Shared Heroine Events", "Two hearts, campfires, banter, married life", shared_chapter())
            continue
        flows = [f for b in s["blocks"] for f in block_flow(b)]
        story += section(s["title"], s.get("kicker", ""), flows, new_page=s.get("newPage", True))
    doc.multiBuild(story)


if __name__ == "__main__":
    build_pdf(ROOT / "walkthrough.pdf")
    print("Wrote walkthrough.pdf")
