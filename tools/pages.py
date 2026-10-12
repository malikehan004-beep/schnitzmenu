"""Page content + Elementor layouts for schnitzmenu.com.

Rules from the blueprint: original wording, Australian spelling, every price
marked (approx.), an H1 with the main keyword, intro in the first 150 words,
jump navigation, tables, FAQ, related links, disclaimer (added site-wide by the theme).
"""
from elementor import (BRAND, GREY, NAVY, TINT, button, container, heading, html, shortcode, text)

UPDATED = "[sm_updated]"


# ---------------------------------------------------------------------------
# Reusable blocks
# ---------------------------------------------------------------------------

def hero(h1, intro, buttons=(), min_height=220, image=None, alt=""):
    kids = [
        text(f"<p>{UPDATED}</p>", classes="sm-hero-badge"),
        heading(h1, "h1", color="#FFFFFF", size=40 if not image else 36),
        text(f"<p>{intro}</p>", color="#FFDDD0", size=18),
    ]
    if buttons:
        row = [button(label, url, bg="#FFFFFF", fg=BRAND) if i == 0 else
               button(label, url, bg=NAVY, fg="#FFFFFF") for i, (label, url) in enumerate(buttons)]
        kids.append(container(row, inner=True, direction="row", gap=12, pad=(6, 0, 0, 0)))
    if not image:
        return container(kids, classes="sm-hero", bg=BRAND, pad=(44, 40, 44, 40), min_height=min_height)
    alt_attr = f" alt='{alt}'" if alt else ""
    media = shortcode(f"[sm_image name='{image}' eager='yes' sizes='(max-width: 767px) 92vw, 460px' class='sm-hero-img'{alt_attr}]")
    return container([
        container(kids, inner=True, width=55, pad=(0, 0, 0, 0)),
        container([media], inner=True, width=41, pad=(0, 0, 0, 0), classes="sm-hero-media"),
    ], classes="sm-hero", bg=BRAND, pad=(44, 40, 44, 40), min_height=min_height, direction="row", gap=28, align="center")


def section(h2, body_html="", *extra, element_id="", tint=False, tag="h2"):
    kids = [heading(h2, tag)]
    if body_html:
        kids.append(text(body_html))
    kids.extend(extra)
    return container(kids, element_id=element_id, classes="sm-band" if tint else "",
                     bg=TINT if tint else None, pad=(30, 24, 30, 24) if tint else (24, 0, 16, 0))


def toolbar():
    return container([shortcode("[sm_menu_search]"), shortcode("[sm_print]")],
                     inner=False, pad=(10, 0, 0, 0), gap=10)


def faq(title, limit=0):
    sc = "[sm_faq set='main']" if not limit else f"[sm_faq set='main' limit='{limit}']"
    return section(title, "<p>Quick answers to the questions Australians search most about Schnitz.</p>",
                   shortcode(sc), element_id="faq")


def related(title, pages):
    return section(title, "", shortcode(f"[sm_related pages='{pages}']"))


def order_strip():
    return container([
        heading("Hungry? Order Schnitz near you", "h2", align="center", color="#FFFFFF", size=28),
        text("<p>Order for pickup or delivery, or browse the full menu first.</p>", align="center", color="#E8E8F0"),
        shortcode("[sm_order]"),
    ], classes="sm-band-dark sm-center", bg=NAVY, pad=(36, 30, 36, 30))


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

ICONS = {
    "menu": "<path d='M4 4h16v16H4z'/><path d='M8 8h8M8 12h8M8 16h5'/>",
    "tag": "<path d='M3 12V3h9l9 9-9 9z'/><circle cx='7.5' cy='7.5' r='1.5'/>",
    "apple": "<path d='M12 7c-2-2-7-1.5-7 4 0 4 3 9 5 9 1 0 1.5-.5 2-.5s1 .5 2 .5c2 0 5-5 5-9 0-5.5-5-6-7-4z'/><path d='M12 7c0-2 1-4 3-4'/>",
    "alert": "<path d='M12 3l10 18H2z'/><path d='M12 10v5M12 18h.01'/>",
}


def card(icon, title, body, label, url):
    svg = ("<span class='sm-card__icon'><svg class='sm-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
           f"stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'>{ICONS[icon]}</svg></span>")
    return container([
        html(svg),
        heading(title, "h3", size=20),
        text(f"<p>{body}</p>"),
        button(label, url),
    ], inner=True, width=23, classes="sm-card", bg="#FFFFFF", pad=(24, 22, 24, 22))


def home():
    return [
        hero("Schnitz Menu Australia 2026 &#8211; Full Menu with Prices &amp; Calories",
             "The complete unofficial Schnitz menu guide for Australia. Prices, calories, allergen information "
             "and the best deals &#8211; checked and updated every month.",
             buttons=(("View the Full Menu", "/schnitz-menu/"), ("See 2026 Prices", "/schnitz-menu-prices/")),
             min_height=420, image="hero-schnitzel-plate"),
        container([
            heading("Find what you need in one tap", "h2", align="center"),
            container([
                card("menu", "Full Menu", "Wraps, burgers, plates, salads, tenders, kids meals and sides.", "View Menu", "/schnitz-menu/"),
                card("tag", "Prices 2026", "Every item with an approximate AUD price, sortable by cost.", "See Prices", "/schnitz-menu-prices/"),
                card("apple", "Calories", "Calorie and kilojoule counts plus a top-10 chart.", "Nutrition Info", "/schnitz-calories/"),
                card("alert", "Allergens", "Gluten, wheat, egg, milk, soy and sesame by crumb.", "Allergen Guide", "/schnitz-allergen-menu/"),
            ], inner=True, direction="row", gap=20, pad=(10, 0, 0, 0)),
        ], classes="sm-band-grey", bg=GREY, pad=(48, 24, 48, 24)),
        container([
            heading("Browse the Schnitz Menu by Category", "h2"),
            text("<p>Pick a category to jump straight to its prices and calories.</p>"),
            shortcode("[sm_category_grid]"),
        ], pad=(44, 24, 10, 24)),
        container([
            heading("Schnitz Prices at a Glance", "h2"),
            shortcode("[sm_price_stats]"),
        ], pad=(24, 24, 10, 24)),
        container([
            heading("Popular Schnitz Plates &amp; Prices", "h2"),
            text("<p>Here are the classic plates most people order. Tap <strong>+</strong> to add items to your meal and "
                 "see the total price and calories.</p>"),
            shortcode("[sm_price_table cat='plates' intro='no' image='no']"),
            button("See every price", "/schnitz-menu-prices/"),
        ], pad=(44, 24, 20, 24)),
        container([
            container([
                heading("What Is Schnitz?", "h2"),
                text(
                    "<p>Schnitz is an Australian fast-casual chain that does one thing really well: fresh, hand-crumbed "
                    "schnitzels. The first store opened in Melbourne in 2002, and the brand has since grown to dozens of "
                    "locations across Victoria, New South Wales, Queensland, South Australia and beyond.</p>"
                    "<p>Every schnitzel is crumbed in store and cooked to order. You can choose chicken, beef or a "
                    "plant-based schnitzel, pick a crumb or a crumb-free flavour, and have it as a burger, a wrap, a "
                    "salad or a plate with chips. That mix-and-match approach is why the menu can feel huge the first "
                    "time you visit &#8211; and why a clear guide like this one is handy.</p>"
                    "<p>SchnitzMenu.com is an independent fan guide. We collect prices from public sources, store "
                    "listings and delivery apps, mark every price as approximate, and refresh the data every month.</p>"),
                button("Read the full menu guide", "/schnitz-menu/"),
            ], inner=True, width=58, pad=(0, 0, 0, 0)),
            container([shortcode("[sm_image name='cat-plates' sizes='(max-width: 767px) 100vw, 440px']")], inner=True, width=38, pad=(0, 0, 0, 0)),
        ], direction="row", gap=32, align="center", pad=(40, 24, 40, 24)),
        container([
            heading("Latest Schnitz Deals", "h2"),
            text("<p>Schnitz runs regular bundles and limited-time deals. These are the most recent ones we have "
                 "seen &#8211; check the app or your local store for what is on right now.</p>"),
            shortcode("[sm_deals]"),
        ], classes="sm-band", bg=TINT, pad=(36, 30, 36, 30)),
        container([faq_block_home()], pad=(40, 24, 20, 24)),
        container([
            heading("Find Your Local Schnitz Restaurant", "h2", align="center", color="#FFFFFF", size=32),
            text("<p>Schnitz has stores across Australia. Check opening hours and order online before you head out.</p>",
                 align="center", color="#E8E8F0"),
            button("View All Australian Locations", "https://schnitz.com.au/", align="center", bg="#FFFFFF", fg=BRAND),
        ], classes="sm-band-dark", bg=NAVY, pad=(52, 30, 52, 30)),
    ]


def faq_block_home():
    return container([
        heading("Schnitz FAQ", "h2"),
        shortcode("[sm_faq set='main' limit='6']"),
        button("More Schnitz questions answered", "/schnitz-menu/#faq"),
    ], inner=True, pad=(0, 0, 0, 0))


# ---------------------------------------------------------------------------
# Main menu (pillar page)
# ---------------------------------------------------------------------------

def schnitz_menu():
    return [
        hero("Schnitz Menu 2026 &#8211; Full Menu with Prices &amp; Calories (Australia)",
             "Every item on the Schnitz menu in one place: wraps and burgers, schnitzel plates, salads, tenders, "
             "kids meals, chips and drinks. Updated monthly. Unofficial guide &#8211; not affiliated with Schnitz International.", image="hero-schnitzel-plate"),
        container([
            shortcode("[sm_breadcrumbs]"),
            text(
                "<p>Looking at the Schnitz menu for the first time can be a little overwhelming. You pick a protein, a "
                "crumb or flavour, then decide whether you want it in a burger, a wrap, on a plate or on a salad. This "
                "guide lays the whole menu out category by category, with an approximate Australian price and calorie "
                "count wherever one is publicly available.</p>"
                "<p>Use the search box to find an item fast, tap a column heading to sort by price or calories, or press "
                "<strong>+</strong> next to any item to build a meal and see the running total. Prices are typical "
                "pickup prices &#8211; delivery apps usually charge more, and some stores (airports, stadiums, CBD "
                "food courts) price higher again.</p>"),
            shortcode("[sm_jump_nav]"),
            toolbar(),
        ], pad=(24, 0, 0, 0)),
        section("How to Order at Schnitz",
                "<ol><li><strong>Choose your schnitzel.</strong> Chicken is the classic. Beef and plant-based schnitzels "
                "are available in most wraps and burgers.</li>"
                "<li><strong>Pick a crumb or flavour.</strong> Traditional crumbs, spicy crumbs, a buttermilk breader, or "
                "a crumb-free flavour such as lemon pepper or Moroccan spices.</li>"
                "<li><strong>Pick a format.</strong> Burger, wrap, plate with chips, or salad.</li>"
                "<li><strong>Add sides and a drink.</strong> Chips, sweet potato chips, slaw, dips and soft drinks.</li></ol>",
                tint=True),
        section("Schnitz Wraps &amp; Burgers Prices 2026", "", shortcode("[sm_price_table cat='wraps-burgers']")),
        section("Schnitz Schnitzel Plates Prices 2026", "", shortcode("[sm_price_table cat='plates']")),
        section("Schnitz Schnacks &amp; Tenders Prices", "", shortcode("[sm_price_table cat='tenders-schnacks']")),
        section("Schnitz Salads Menu", "", shortcode("[sm_price_table cat='salads']")),
        section("Schnitz Kids Menu (Little Rascals)", "", shortcode("[sm_price_table cat='kids']")),
        section("Schnitz Chips, Sides &amp; Dips", "", shortcode("[sm_price_table cat='chips-dips']")),
        section("Schnitz Drinks Menu", "", shortcode("[sm_price_table cat='drinks']")),
        section("Schnitz Calories &#8211; Highest Calorie Items",
                "<p>If you are watching your energy intake, the plates with chips are the big ones. A loaded schnitzel "
                "with chips can pass 1,000 calories on its own. Calorie figures below come from third-party nutrition "
                "databases and should be treated as estimates.</p>",
                shortcode("[sm_calorie_chart top='8']"),
                button("Full calorie guide", "/schnitz-calories/"),
                element_id="calories", tint=True),
        section("Schnitz Allergen Information",
                "<p>The chicken itself is listed with no allergens &#8211; it is the coating that matters. Traditional "
                "crumbs contain wheat, gluten, egg, milk, soy and sesame. See the full matrix before you order if "
                "you have a food allergy.</p>",
                button("Open the allergen guide", "/schnitz-allergen-menu/"),
                element_id="allergens"),
        section("About Schnitz in Australia",
                "<p>Schnitz started in Melbourne in 2002 with a simple idea: take the pub schnitzel, crumb it fresh in "
                "front of the customer, and serve it fast. More than twenty years later the chain has stores in "
                "shopping centres, high streets and food courts across several states.</p>"
                "<p>What makes Schnitz different from other fast food chains is the cooking method. Schnitzels are "
                "crumbed by hand during service rather than arriving pre-crumbed and frozen, which is why the queue "
                "moves a little slower at lunch &#8211; and why fans think it is worth the wait.</p>"
                "<p>The menu changes regularly with limited-time burgers, seasonal specials and family bundles. We "
                "check prices and new items at the start of every month and update this page.</p>",
                tint=True),
        section("Schnitz Value Deals &amp; Bundles", "", shortcode("[sm_deals]"),
                button("All deals and coupons", "/schnitz-coupons/")),
        faq("Schnitz Menu FAQ"),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("More Schnitz Guides", "schnitz-menu-prices,schnitz-calories,schnitz-allergen-menu,schnitz-kids-menu,schnitz-coupons"),
        container([shortcode("[sm_menu_schema]")], pad=(0, 0, 0, 0)),
    ]


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------

def prices():
    return [
        hero("Schnitz Menu Prices 2026 &#8211; Full Price List (Australia)",
             "Approximate Australian prices for every Schnitz wrap, burger, plate, tender, kids meal and side. "
             "Sort by price, search the list and build a meal to see your total.", image="cat-wraps-burgers"),
        container([
            shortcode("[sm_breadcrumbs]"),
            text(
                "<p>How much does Schnitz cost? In most Australian stores a schnitzel wrap or burger sits between about "
                "<strong>$14 and $17 (approx.)</strong>, while a schnitzel plate with chips costs roughly <strong>$19.50 "
                "to $25.50 (approx.)</strong>. Kids meals start around <strong>$11 (approx.)</strong> and a dip is about "
                "<strong>$2 (approx.)</strong>.</p>"
                "<p>The prices below are typical pickup prices collected from public sources and store listings. They "
                "change between states and stores, and delivery apps such as Uber Eats and DoorDash usually add a "
                "mark-up. Where we could not confirm a price, the table says <em>Varies</em> rather than guessing.</p>"),
            shortcode("[sm_price_stats]"),
            shortcode("[sm_jump_nav]"),
            toolbar(),
        ], pad=(24, 0, 0, 0)),
        section("Schnitz Wraps &amp; Burgers Prices", "", shortcode("[sm_price_table cat='wraps-burgers' intro='no' image='no']")),
        section("Schnitz Plates Prices", "", shortcode("[sm_price_table cat='plates' intro='no' image='no']")),
        section("Schnitz Tenders &amp; Schnacks Prices", "", shortcode("[sm_price_table cat='tenders-schnacks' intro='no' image='no']")),
        section("Schnitz Salads Prices", "", shortcode("[sm_price_table cat='salads' intro='no' image='no']")),
        section("Schnitz Kids Menu Prices", "", shortcode("[sm_price_table cat='kids' intro='no' image='no']")),
        section("Schnitz Chips, Sides &amp; Dips Prices", "", shortcode("[sm_price_table cat='chips-dips' intro='no' image='no']")),
        section("Schnitz Drinks Prices", "", shortcode("[sm_price_table cat='drinks' intro='no' image='no']")),
        section("Why Schnitz Prices Differ Between Stores",
                "<ul><li><strong>Location.</strong> Airport, stadium and CBD stores often charge more to cover higher rent.</li>"
                "<li><strong>Pickup vs delivery.</strong> Delivery menus are commonly 15&#8211;30% higher than in-store prices.</li>"
                "<li><strong>State.</strong> Wages and supply costs vary between states, so do prices.</li>"
                "<li><strong>Deals.</strong> App-only and limited-time bundles can be much cheaper than ordering items separately.</li></ul>"
                "<p>Tip: if you are feeding a family, compare the bundle price against ordering items one by one using "
                "the meal builder on this page.</p>", tint=True),
        section("Cheapest Items on the Schnitz Menu",
                "<p>The cheapest things you can buy at Schnitz are a dipping sauce (about $2 approx.) and a small serve of "
                "tenders (about $7.90 approx.). For a full meal on a budget, look out for value deals that bundle a "
                "small wrap, mini chips and a drink, which have sold for around $10 in the past.</p>"),
        faq("Schnitz Prices FAQ", limit=8),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("Related Schnitz Guides", "schnitz-menu,schnitz-coupons,schnitz-calories,schnitz-kids-menu"),
    ]


# ---------------------------------------------------------------------------
# Calories
# ---------------------------------------------------------------------------

def calories():
    return [
        hero("Schnitz Calories &amp; Nutrition Guide 2026 (Australia)",
             "How many calories are in a Schnitz schnitzel? Calorie and kilojoule counts for popular Schnitz items, "
             "a top-10 chart and tips for a lighter order.", image="cat-salads"),
        container([shortcode("[sm_breadcrumbs]"), 
            text(
                "<p>Schnitz meals are hearty. A classic <strong>Schnitzel &amp; Chips</strong> comes in at roughly "
                "<strong>779 calories (3,259 kJ)</strong>, a <strong>Parma &amp; Chips</strong> at about <strong>897 "
                "calories</strong>, and a <strong>Loaded Schnitzel &amp; Chips</strong> can reach around <strong>1,150 "
                "calories</strong>. For comparison, the average Australian adult daily intake used on food labels is "
                "8,700 kJ (about 2,080 calories).</p>"
                "<p>The figures on this page come from third-party nutrition databases and public sources. They are "
                "estimates &#8211; serving sizes, crumbs and sauces change the numbers. Where we do not have a reliable "
                "figure we leave it blank instead of guessing.</p>"),
        ], pad=(24, 0, 0, 0)),
        section("Schnitz Calorie Chart &#8211; Top Items", "", shortcode("[sm_calorie_chart top='10']"), tint=True),
        section("Schnitz Nutrition Table (Calories &amp; Kilojoules)",
                "<p>Tap a column heading to sort. Kilojoules are calculated from calories (1 kcal = 4.184 kJ).</p>",
                shortcode("[sm_nutrition_table]")),
        section("How to Order a Lighter Meal at Schnitz",
                "<ul><li><strong>Swap chips for salad.</strong> Chips add several hundred calories to any plate.</li>"
                "<li><strong>Go for a salad with schnitzel.</strong> You still get the schnitzel without the bun or wrap.</li>"
                "<li><strong>Try a crumb-free flavour.</strong> Lemon pepper or Moroccan spices skip the crumb coating.</li>"
                "<li><strong>Watch the sauces.</strong> Creamy mayo and aioli add up quickly. Ask for sauce on the side.</li>"
                "<li><strong>Share the tenders.</strong> One original tender is about 152 calories.</li>"
                "<li><strong>Choose water.</strong> A 600ml soft drink can add around 250 calories.</li></ul>", tint=True),
        section("Which Schnitz Item Has the Most Calories?",
                "<p>Based on available data, the <strong>Loaded Schnitzel &amp; Chips</strong> is the highest-calorie "
                "single item at around 1,150 calories (approx.). Large tender packs meant for sharing will be higher "
                "in total, but they are designed to split between two or more people.</p>"),
        faq("Schnitz Nutrition FAQ", limit=6),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("Related Schnitz Guides", "schnitz-allergen-menu,schnitz-menu,schnitz-menu-prices"),
    ]


# ---------------------------------------------------------------------------
# Allergens
# ---------------------------------------------------------------------------

def allergens():
    return [
        hero("Schnitz Allergen Menu 2026 &#8211; Gluten, Egg, Milk, Soy &amp; Sesame",
             "A clear allergen guide for the Schnitz menu in Australia, organised by crumb and coating. Always confirm "
             "with your local store before ordering.", image="cat-tenders-schnacks"),
        container([shortcode("[sm_breadcrumbs]"), 
            text(
                "<p><strong>Important:</strong> this guide summarises publicly available allergen information to help "
                "you plan. It is not medical advice. Schnitz kitchens handle wheat, egg, milk, soy and sesame, so "
                "cross-contact is possible. If you have a serious allergy or coeliac disease, speak to the staff and "
                "check the official allergen chart before you order.</p>"
                "<p>The key thing to understand about Schnitz allergens is that the <strong>protein itself (plain "
                "chicken) is listed with no allergens</strong>. Most allergens come from the crumb, the breader and the "
                "sauces. Choosing a different coating changes what you are eating.</p>"),
        ], pad=(24, 0, 0, 0)),
        section("Schnitz Allergen Matrix by Crumb", "", shortcode("[sm_allergens]"), tint=True),
        section("Is Schnitz Gluten Free?",
                "<p>Traditional crumbed schnitzels are <strong>not gluten free</strong> &#8211; the flour, egg wash and "
                "breadcrumbs all contain gluten. Even the crumb-free lemon pepper flavour is listed as containing gluten. "
                "Schnitz does list a gluten free wrap on its allergen chart, but because gluten is everywhere in the "
                "kitchen, people with coeliac disease should ask staff how it is prepared before ordering.</p>"
                "<p>In Australia a product can only be labelled gluten free if it contains no detectable gluten under "
                "the Food Standards Code, which is a very high bar for a busy fast food kitchen.</p>"),
        section("Schnitz Egg, Milk, Soy and Sesame Allergies",
                "<ul><li><strong>Egg:</strong> used in traditional crumbing. Ask about crumb-free options.</li>"
                "<li><strong>Milk:</strong> present in traditional crumbs, the buttermilk breader, cheese and many sauces.</li>"
                "<li><strong>Soy:</strong> listed in traditional crumbs and some sauces.</li>"
                "<li><strong>Sesame:</strong> listed in traditional crumbs and often in burger buns.</li></ul>", tint=True),
        section("Plant-Based and Vegan Options",
                "<p>Schnitz offers a plant-based schnitzel in many burgers and wraps. Plant-based does not always mean "
                "vegan or allergen free: crumbs, buns and sauces may contain egg or milk. Check the official chart for "
                "the exact combination you want.</p>"),
        faq("Schnitz Allergen FAQ", limit=6),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("Related Schnitz Guides", "schnitz-calories,schnitz-menu,schnitz-kids-menu"),
    ]


# ---------------------------------------------------------------------------
# Kids menu
# ---------------------------------------------------------------------------

def kids():
    return [
        hero("Schnitz Kids Menu 2026 &#8211; Little Rascals Meals &amp; Prices",
             "What is on the Schnitz kids menu, how much it costs and what comes in each pack.", image="cat-kids"),
        container([shortcode("[sm_breadcrumbs]"), text(
            "<p>The Schnitz kids menu, called <strong>Little Rascals</strong>, was refreshed with two main options: the "
            "<strong>Kiddy Schnugget Pack</strong> and the <strong>Teeny Weeny</strong>. Both come as a complete meal "
            "with mini chips and a drink, which makes them an easy choice for younger eaters.</p>"
            "<p>The Kiddy Schnugget Pack launched at around <strong>$11 (approx.)</strong>. Prices vary between stores, "
            "so check with your local Schnitz.</p>")], pad=(24, 0, 0, 0)),
        section("Schnitz Kids Menu Prices", "", shortcode("[sm_price_table cat='kids']"), tint=True),
        section("What Comes in a Schnitz Kids Meal?",
                "<ul><li><strong>Kiddy Schnugget Pack</strong> &#8211; bite-size schnitzel pieces (schnuggets), mini chips and a drink.</li>"
                "<li><strong>Teeny Weeny</strong> &#8211; a small burger or wrap with schnitzel, tomato sauce and cheese, plus mini chips and a Pop Top.</li></ul>"
                "<p>Kids meals use the same crumbs as the main menu, so the same allergen rules apply. See the allergen "
                "guide if your child has a food allergy.</p>"),
        section("Tips for Ordering for Kids",
                "<ul><li>Ask for sauce on the side for fussy eaters.</li>"
                "<li>Family bundles can be cheaper than separate kids meals for larger groups.</li>"
                "<li>Swap the soft drink for water where offered.</li></ul>", tint=True),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("Related Schnitz Guides", "schnitz-menu,schnitz-allergen-menu,schnitz-coupons"),
    ]


# ---------------------------------------------------------------------------
# Deals
# ---------------------------------------------------------------------------

def deals():
    return [
        hero("Schnitz Deals &amp; Coupons 2026 &#8211; Bundles and Specials",
             "The latest Schnitz meal deals, family bundles and limited-time specials we have seen in Australia.", image="cat-chips-dips"),
        container([shortcode("[sm_breadcrumbs]"), text(
            "<p>Schnitz regularly runs value deals through its app and in store &#8211; from cheap lunch bundles to "
            "family feasts. Deals are usually limited-time and may only run in some states, so treat the list below "
            "as a guide to what to look for, and check the official app for what is on today.</p>")], pad=(24, 0, 0, 0)),
        section("Recent Schnitz Deals", "", shortcode("[sm_deals]"), tint=True),
        section("How to Save Money at Schnitz",
                "<ul><li><strong>Order pickup, not delivery.</strong> Delivery app prices are often higher.</li>"
                "<li><strong>Use the official app.</strong> App-only deals and specials appear there first.</li>"
                "<li><strong>Buy a bundle.</strong> Family and race-day bundles cost less than ordering items separately.</li>"
                "<li><strong>Watch for one-day specials.</strong> Schnitz has run $5 schnitzel days in the past.</li></ul>"),
        container([shortcode("[sm_author]")], pad=(10, 0, 10, 0)),
        related("Related Schnitz Guides", "schnitz-menu-prices,schnitz-menu,schnitz-kids-menu"),
    ]


# ---------------------------------------------------------------------------
# Legal / trust pages
# ---------------------------------------------------------------------------

def simple(h1, intro, *sections):
    out = [hero(h1, intro, min_height=180)]
    for h2, body in sections:
        out.append(section(h2, body))
    return out


def about():
    return simple(
        "About SchnitzMenu.com",
        "Who runs this site, why it exists and how we keep the information accurate.",
        ("Why We Built This Guide",
         "<p>SchnitzMenu.com is an independent, unofficial guide to the Schnitz menu in Australia. We built it because "
         "finding simple answers &#8211; how much a parma costs, how many calories are in a wrap, which crumbs contain "
         "egg &#8211; meant digging through delivery apps, PDFs and old forum posts. We wanted one clear, fast page "
         "that answered those questions properly.</p>"),
        ("Who We Are",
         "<p>The site is run by RK Mohsin, a website publisher focused on helpful, easy-to-read food guides. We are fans "
         "of the food, not employees of the company. We are not affiliated with, endorsed by or sponsored by Schnitz "
         "International Pty Ltd.</p>"),
        ("How We Collect and Check Prices",
         "<ul><li>We gather prices from public sources, store listings and delivery apps.</li>"
         "<li>Every price is marked <em>(approx.)</em> because prices vary between stores, states and ordering methods.</li>"
         "<li>Where we cannot confirm a price or calorie figure, we say so instead of guessing.</li>"
         "<li>We review the data at the start of every month and update the date shown on each page.</li></ul>"),
        ("Corrections",
         "<p>Spotted a price that has changed or a new menu item? Please let us know through the "
         "<a href='/contact/'>contact page</a> and we will update the guide.</p>"),
        ("How This Site Is Funded",
         "<p>SchnitzMenu.com is free to use. We may earn money from advertising (such as Google AdSense) and from "
         "affiliate links to food delivery services. This never changes the prices or information we publish.</p>"),
    )


def contact():
    return simple(
        "Contact SchnitzMenu.com",
        "Questions, corrections or partnership enquiries &#8211; we would love to hear from you.",
        ("Get in Touch",
         "<p>Email us at <a href='mailto:hello@schnitzmenu.com'>hello@schnitzmenu.com</a>. We usually reply within two "
         "business days.</p>"
         "<p><strong>Please note:</strong> we are an independent guide and cannot help with orders, refunds or store "
         "complaints. For those, contact Schnitz directly through the official website or app.</p>"),
        ("Report a Price Change",
         "<p>If a price, item or allergen detail on this site is out of date, tell us the item, the store and the "
         "price you paid. Every correction helps keep the guide accurate for everyone.</p>"),
    )


def privacy():
    return simple(
        "Privacy Policy",
        "How SchnitzMenu.com collects, uses and protects your information.",
        ("Overview",
         "<p>This policy explains how SchnitzMenu.com (we, us) handles personal information. We follow the Australian "
         "Privacy Principles in the Privacy Act 1988 (Cth). By using this site you agree to this policy.</p>"),
        ("Information We Collect",
         "<ul><li><strong>Information you give us</strong> &#8211; such as your name and email when you contact us or "
         "subscribe to updates.</li>"
         "<li><strong>Usage information</strong> &#8211; pages visited, device and browser type, and approximate location, "
         "collected through cookies and analytics tools such as Google Analytics.</li></ul>"),
        ("Cookies and Advertising",
         "<p>We use cookies to understand how the site is used and to show advertising. Third-party vendors, including "
         "Google, use cookies to serve ads based on your previous visits to this and other websites. Google's use of "
         "advertising cookies enables it and its partners to serve ads based on your visits to this site and/or other "
         "sites on the internet.</p>"
         "<p>You can opt out of personalised advertising by visiting <a href='https://adssettings.google.com' "
         "rel='nofollow noopener' target='_blank'>Google Ads Settings</a> or "
         "<a href='https://www.aboutads.info' rel='nofollow noopener' target='_blank'>aboutads.info</a>. You can also "
         "block or delete cookies in your browser settings.</p>"),
        ("Affiliate Links",
         "<p>Some links to food delivery services are affiliate links. If you order through them we may earn a small "
         "commission at no extra cost to you. These services have their own privacy policies.</p>"),
        ("How We Use Information",
         "<ul><li>To reply to your messages.</li><li>To improve the site and its content.</li>"
         "<li>To show relevant advertising.</li><li>To meet legal obligations.</li></ul>"
         "<p>We do not sell your personal information.</p>"),
        ("Access, Correction and Complaints",
         "<p>You can ask to access or correct the personal information we hold about you by emailing "
         "<a href='mailto:hello@schnitzmenu.com'>hello@schnitzmenu.com</a>. If you are unhappy with how we handled your "
         "information you can contact the Office of the Australian Information Commissioner (OAIC).</p>"),
        ("Changes to This Policy",
         "<p>We may update this policy from time to time. The latest version is always on this page.</p>"),
    )


def disclaimer():
    return simple(
        "Disclaimer",
        "Important information about the content on SchnitzMenu.com.",
        ("Unofficial Website",
         "<p>SchnitzMenu.com is an independent, unofficial fan guide. We are <strong>not affiliated with, endorsed by, "
         "or sponsored by Schnitz International Pty Ltd</strong> or any of its franchisees. Schnitz and related names "
         "and marks belong to their respective owners and are used here only to identify the restaurant being described.</p>"),
        ("Prices",
         "<p>All prices on this site are approximate and are provided for general information only. Prices vary by "
         "location, state, ordering method and date, and may change without notice. Always confirm the current price "
         "with your local restaurant.</p>"),
        ("Nutrition and Allergen Information",
         "<p>Calorie and allergen information is collected from public and third-party sources and may be incomplete "
         "or out of date. It is not medical or dietary advice. If you have a food allergy, intolerance or coeliac "
         "disease, always check with the restaurant before ordering.</p>"),
        ("Affiliate and Advertising Disclosure",
         "<p>This site may earn income from advertising and affiliate links. This does not affect the information we "
         "publish.</p>"),
        ("Limitation of Liability",
         "<p>We make every effort to keep information accurate but cannot guarantee it. We are not responsible for any "
         "loss or harm arising from the use of information on this website.</p>"),
    )


def dmca():
    return simple(
        "DMCA &amp; Copyright Policy",
        "How to report content you believe infringes your copyright.",
        ("Our Content",
         "<p>All text, tables and graphics on SchnitzMenu.com are original works created for this site unless stated "
         "otherwise. Please do not copy our content without permission.</p>"),
        ("Reporting Infringement",
         "<p>If you believe content on this site infringes your copyright, email "
         "<a href='mailto:hello@schnitzmenu.com'>hello@schnitzmenu.com</a> with:</p>"
         "<ul><li>Your name and contact details.</li><li>A description of the copyrighted work.</li>"
         "<li>The URL of the content on our site.</li>"
         "<li>A statement that you have a good-faith belief the use is not authorised.</li>"
         "<li>A statement that the information in your notice is accurate and that you are the owner or authorised "
         "to act for the owner.</li></ul>"
         "<p>We will review every valid notice and remove infringing content promptly.</p>"),
    )


# ---------------------------------------------------------------------------
# Page registry: slug, title, SEO title, meta description, builder, template, sidebar
# ---------------------------------------------------------------------------

PAGES = [
    ("home", "Home", "Schnitz Menu Australia 2026 - Prices, Calories & Full Menu",
     "Unofficial Schnitz menu guide for Australia with 2026 prices, calories, allergens and deals. Updated monthly.",
     home, "elementor_header_footer", "no-sidebar"),
    ("schnitz-menu", "Schnitz Menu", "Schnitz Menu 2026 - Full Menu with Prices & Calories (Australia)",
     "The full Schnitz menu in Australia: wraps, burgers, plates, salads, tenders, kids meals and sides with prices and calories.",
     schnitz_menu, "default", "right-sidebar"),
    ("schnitz-menu-prices", "Schnitz Menu Prices", "Schnitz Menu Prices 2026 - Full Price List Australia",
     "How much is Schnitz? Approximate 2026 prices for every Schnitz wrap, burger, plate, kids meal and side in Australia.",
     prices, "default", "right-sidebar"),
    ("schnitz-calories", "Schnitz Calories", "Schnitz Calories & Nutrition 2026 - Calorie Chart",
     "Schnitz calories and kilojoules for popular items, a top-10 calorie chart and tips for a lighter order.",
     calories, "default", "right-sidebar"),
    ("schnitz-allergen-menu", "Schnitz Allergen Menu", "Schnitz Allergen Menu 2026 - Gluten, Egg, Milk, Soy & Sesame",
     "Schnitz allergen guide by crumb: gluten, wheat, egg, milk, soy and sesame. Is Schnitz gluten free? Find out here.",
     allergens, "default", "right-sidebar"),
    ("schnitz-kids-menu", "Schnitz Kids Menu", "Schnitz Kids Menu 2026 - Little Rascals Meals & Prices",
     "Schnitz kids menu prices and what comes in the Kiddy Schnugget Pack and Teeny Weeny.",
     kids, "default", "right-sidebar"),
    ("schnitz-coupons", "Schnitz Deals & Coupons", "Schnitz Deals & Coupons 2026 - Bundles and Specials",
     "Latest Schnitz meal deals, family bundles and specials in Australia, plus tips to save money.",
     deals, "default", "right-sidebar"),
    ("about", "About", "About SchnitzMenu.com", "Who runs SchnitzMenu.com and how we keep prices accurate.",
     about, "default", "no-sidebar"),
    ("contact", "Contact", "Contact SchnitzMenu.com", "Contact SchnitzMenu.com with questions or price corrections.",
     contact, "default", "no-sidebar"),
    ("privacy-policy", "Privacy Policy", "Privacy Policy - SchnitzMenu.com", "SchnitzMenu.com privacy policy.",
     privacy, "default", "no-sidebar"),
    ("disclaimer", "Disclaimer", "Disclaimer - SchnitzMenu.com", "SchnitzMenu.com is an unofficial guide. Read our disclaimer.",
     disclaimer, "default", "no-sidebar"),
    ("dmca", "DMCA", "DMCA Policy - SchnitzMenu.com", "SchnitzMenu.com copyright and DMCA policy.",
     dmca, "default", "no-sidebar"),
]
