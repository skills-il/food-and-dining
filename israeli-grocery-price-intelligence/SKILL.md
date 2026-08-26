---
name: israeli-grocery-price-intelligence
description: Access and compare Israeli supermarket prices using mandatory Price Transparency Law data feeds. Use when user asks about "supermarket prices Israel", "price comparison Shufersal", "Rami Levy prices", "grocery prices", "Price Transparency Law", "shopping list optimizer", "food costs Israel", or "השוואת מחירי סופר". Covers chain-specific XML feed parsing, cross-chain price comparison, shopping list optimization, price trend tracking, and restaurant ingredient cost analysis. Do NOT use for restaurant operations (use israeli-restaurant-ops) or non-food retail prices.
license: MIT
allowed-tools: Bash(python:*) Bash(python3:*) Bash(curl:*) Bash(grep:*) Bash(sed:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled price monitoring and automated shopping list optimization.
---


# Israeli Grocery Price Intelligence

## Instructions

### Fastest path for a non-developer: ready-made comparison apps

If the user just wants to know where a product or basket is cheapest (and is not building an automated pipeline), point them at the consumer price-comparison services that already parse these feeds, no code required:

- **CHP** (https://chp.co.il), the most widely used Israeli grocery price-comparison site, compares a full basket across nearby branches.
- **Pricez** (https://www.pricez.co.il) and **Savy** (https://www.savy.co.il), additional consumer comparison apps.
- The **official Ministry of Economy list of approved price-comparison apps** (https://www.gov.il/he/pages/cpfta_apps), the authoritative directory of services vetted under the price-transparency law.

Use the raw-feed / MCP path below when the user needs automation, a custom shopping-list optimizer, trend tracking, or restaurant cost analysis that the consumer apps don't offer.

### Preferred (for automation): Use the Supermarket Prices MCP Server

If the user has the **supermarket-prices** MCP server installed, use it instead of manually fetching XML feeds. The MCP handles authentication, CSRF tokens, SSL issues, and platform quirks automatically.

Install instructions: https://agentskills.co.il/he/mcp/supermarket-prices

Available MCP tools:
- `list_chains` -- list the covered chains with data source info (web / publishprice / FTP)
- `search_products` -- search by product name or barcode
- `compare_prices` -- cross-chain price comparison, sorted cheapest first
- `get_promotions` -- current sales and promotions per chain
- `get_store_data` -- store locations, filterable by city
- `get_chain_files` -- browse raw XML price files
- `get_xml_schema_info` -- reference docs for the XML schema and fields

If the MCP is available, skip Steps 1-2 and use MCP tools directly for Steps 3-6. If the MCP is not installed, fall back to the manual XML feed approach below.

### Step 1: Access Supermarket XML Feeds (Manual Fallback)
Under the Promotion of Competition in the Food and Pharma Sector Law (חוק קידום התחרות בענפי המזון והפארם, 2014, in force since 2015), Israeli supermarket and pharmacy chains with 3+ stores must publish product prices as XML files. The "Pharma" in the law name is why Super-Pharm and Good Pharm publish too, but pharmacy feeds cover drugstore SKUs (toiletries, OTC, baby food) only, not fresh produce or dairy.

- Available data files per chain (filename prefixes per the government spec):
  - **PriceFull** -- full snapshot of the product catalog with prices
  - **Price** -- delta updates between full snapshots
  - **PromoFull** + **Promo** -- full snapshot and deltas of current sales and promotions
  - **StoresFull** + **Stores** -- store locations and details
- **Do not regex on filename shape.** Two shapes are in use, they are NOT split cleanly by platform, and a single chain's listing carries both:
  - 3-segment: `PriceFull<ChainId>-<StoreId>-<yyyyMMddHHmm>.gz`
  - 5-segment: `PriceFull<ChainId>-<SubChainId>-<StoreId>-<yyyyMMdd>-<HHmmss>.gz`

  A live Rami Levy listing (Cerberus) held 44 `PriceFull` files in the 3-segment shape and 93 in the 5-segment shape, with the newer files using the 5-segment form. Shufersal and Carrefour also use the 5-segment form. `Stores` files use their own 4-segment shape and are often plain `.xml`. Prefix case is inconsistent even within one listing (`price`, `Price`, `pricefull`, `PriceFull`), so match case-insensitively and parse positionally from the right rather than assuming a segment count. Neither shape ends in `.xml.gz`.

  **Match the LONGER prefix first.** A case-insensitive `startswith("price")` also matches every `PriceFull`, and `startswith("promo")` matches every `PromoFull`, so a filter written for deltas silently ingests full snapshots. Test for `pricefull` / `promofull` before falling through to `price` / `promo`
- **Feeds are published one file per STORE, not one per chain.** A chain-level file does not exist: a chain with several hundred branches publishes a `PriceFull` per branch per day. Fetching one arbitrary file and calling it "Shufersal's price" is wrong, and every merged dataset needs `(ChainId, SubChainId, StoreId, ItemCode)` as its key, read from the file's own root element. That tuple is also the join back to the `Stores` feed for the branch address, which is what makes any "near me" answer possible.
- Full snapshots typically refreshed daily (overnight, 01:00-05:00 IL time); delta files may be pushed several times per day
- **Shufersal downloads are time-limited signed URLs.** The portal root is only a browser UI. List files with `GET https://prices.shufersal.co.il/FileObject/UpdateCategory?catID=<N>&storeId=0` (`catID=1` Price, `2` PriceFull, `3` Promo, `4` PromoFull, `5` Stores), then read the `pricesprodpublic.blob.core.windows.net` links out of the HTML. Those links carry an `se=` expiry roughly half an hour out, pinned to a clock boundary rather than measured from your request, so the window you actually get can be much shorter. Fetch promptly and never cache or bookmark one.
- **Carrefour** inlines its file list in the portal HTML as a JavaScript `files` array alongside a `path` of `yyyyMMdd`; download at `https://prices.carrefour.co.il/<path>/<filename>`. A wrong filename returns a real 404.
- See `references/chain-feeds.md` for per-chain endpoints, access methods, and Cerberus authentication

Chains publish through **several** platforms, not one and not three. Each platform has its own
access mechanics. Routing a chain to the wrong platform is the single most common cause of an
agent reporting "this chain publishes nothing". The table below was verified by live probe on
2026-08-27; treat it as a starting point and re-probe rather than assume:

| Platform | URL | Chains verified on it | Access |
|----------|-----|----------------------|--------|
| Shufersal Direct | https://prices.shufersal.co.il | Shufersal | Public listing page; downloads are **expiring signed URLs** (see below) |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (Carrefour / Mega / Yeinot Bitan branded stores) | Public; file list is inlined in the page, downloads at `/<yyyyMMdd>/<filename>` |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy, Yochananof, Tiv Taam, Osher Ad, Dor Alon, Keshet Taamim, Fresh Market / Super Dosh, Cofix (`SuperCofixApp`) | Session login + CSRF (see below) |
| Super-Pharm own portal | http://prices.super-pharm.co.il | Super-Pharm | Public listing page |
| Bina Projects | https://goodpharm.binaprojects.com/Main.aspx | Good Pharm, and several small chains (King Store, Shuk Ahir, Zol VeBegadol, Bareket) | Public listing page per chain subdomain |
| Chain's own site | https://shop.hazi-hinam.co.il/Prices | Hazi Hinam | Public file table |

**Chains that are NOT on Cerberus, despite often being listed there.** A Cerberus login for
`Victory`, `SuperPharm`, `GoodPharm`, `Bareket` or `Mega` fails (the POST returns 200 and
re-renders the login form rather than the 302 a valid chain code gets). `HaziHinam` logs in but
its directory listing is empty, while its own site serves a full file table. Do not conclude from
a Cerberus failure that a chain stopped publishing, look for its own portal first.

Victory and Mahsani A'Shuk moved off the defunct Nibit platform to a successor endpoint
(`laibcatalog.co.il`). That host resolves but did not accept connections from our probe on
2026-08-27, so we cannot confirm its current state either way, verify it yourself before relying
on it. The old `matrixcatalog.co.il` host no longer resolves at all (NXDOMAIN, not a timeout).

**Cerberus requires real authentication, not just a URL fetch, and the directory listing is a
POST.** The flow is: GET `/login` → parse the `<meta name="csrftoken">` value AND keep the
response cookie → POST `/login/user` with `username=<chain-code>`, `password=<password-or-empty>`,
`csrftoken=<value>` (a valid chain code answers **302**; an invalid one answers 200 and re-renders
the form) → GET `/file` and read the **fresh** csrftoken from that page → **POST** `/file/json/dir`
with that token plus DataTables paging params to list files → GET `/file/d/<filename>` to download.

A **GET** on `/file/json/dir` returns HTTP 200 with
`{"aaData":[],"error":"Invalid request method used for this operation."}`. That is an empty list,
not an error status, so an agent that issues a GET will silently conclude the chain publishes
nothing. See `references/chain-feeds.md` for the working commands and per-chain codes.

### Step 2: Parse Chain-Specific Data Formats
Each chain publishes in a slightly different XML schema. Major chains:

| Chain | Hebrew Name | Platform | Notes |
|-------|-------------|----------|-------|
| Shufersal | שופרסל | Direct (prices.shufersal.co.il) | Largest chain, operating the Shufersal Deal, Sheli, Yesh and Express banners; most structured data. Read the `Stores` feed for a current branch count |
| Rami Levy | רמי לוי | Cerberus (`RamiLevi`) | Known for low prices |
| Yochananof | יוחננוף | Cerberus | Central Israel focus |
| Victory | ויקטורי | Not on Cerberus (see platform notes) | A separate company from Carrefour Israel, not a Carrefour banner. It runs several banners (Victory, Victory Local, Victory City, Victory Plus, Victory Online) that can price the same SKU differently, so key comparisons on the specific banner and store rather than on "Victory" as one entity |
| Carrefour Israel | קרפור ישראל | Direct (prices.carrefour.co.il) | One publisher covering several banners in parallel. Its own `Stores` feed lists `בעיר` and `יינות ביתן` branded stores alongside Carrefour ones, so not every store is Carrefour-branded |
| Osher Ad | אושר עד | Cerberus (username: `osherad`, no password) | Discount chain, large-format stores |
| Tiv Taam | טיב טעם | Cerberus (`TivTaam`) | Carries non-kosher items, so its product mix differs from kosher-only chains |

Use `scripts/parse_price_xml.py` to parse feeds into normalized JSON format.
Key fields: item_code, item_name, manufacturer, price, unit_price, quantity, unit_of_measure, is_weighted, update_date

**Weighted-item math:** when `bIsWeighted=1`, `ItemPrice` is a price per unit of measure rather than the price of the package on the shelf, **and that unit is NOT always a kilogram**. Read `UnitOfMeasure` and normalise by it. On a live Carrefour `PriceFull`, 174 of 560 weighted items declared `100 גרם` rather than a kilogram unit, so treating `ItemPrice` as NIS/kg overstates those by an order of magnitude. Values seen in the wild include `קילוגרם`, `ק"ג`, `1קילוגרם`, `100 גרם` and even `100 ק"ג`, with inconsistent spacing. `Quantity` may be empty or fractional. Normalise every weighted item to a common unit before comparing, otherwise cross-chain rankings are silently wrong.

### Step 2.5: Reconcile Delta Files Against Snapshots
A `Price` or `Promo` file is a **delta**, containing only rows that changed. Parsing one as if it
were a catalogue yields a 200-item "chain catalogue" that is really one morning's edits.

- Start from the most recent `PriceFull` for that store, then apply `Price` deltas in filename-timestamp order. Out-of-order application produces fabricated price movements, which is fatal to Step 5 trend tracking.
- A row absent from a delta is **unchanged**, not deleted.
- Check `ItemStatus` before treating a row as a live price; do not present a delisted or inactive SKU as purchasable.
- Reconcile per store. Deltas are keyed by store, so mixing branches silently overwrites prices.

### Step 3: Cross-Chain Price Comparison
Match products across chains by:
- **Barcode** (most reliable, Israeli standard barcode prefix 729)
- **Item name + manufacturer** (fuzzy matching for naming differences)
- **Item code** (chain-specific, less reliable for cross-chain)

**Some staples are under statutory price control** (פיקוח מחירים), including controlled dairy
products, so their shelf price is capped and near-identical across chains. Presenting a
"switch chains and save" result on a controlled item overstates the achievable saving. We could
not retrieve a current authoritative list of controlled products (the Ministry of Economy page is
not machine-fetchable), so check the controlling order before you present savings on a staple
rather than assuming the spread is real.

Generate comparison table for specific products:
- Calculate: cheapest chain, average price, price spread (max-min)
- Handle store-specific pricing (same chain may have different prices by location)

### Step 4: Optimize Shopping Lists
Given a shopping list, find the cheapest option:
- **Single-store:** cheapest store for entire basket
- **Multi-store:** optimal split across 2-3 nearby stores (minimize cost + travel)

Factor in current promotions from the `PromoFull` feed. **Where the promotion fields live depends
on the dialect**, and this is where naive parsers silently return nothing:

- **Cerberus dialect** (Rami Levy et al.): `RewardType`, `MinQty`, `DiscountedPrice` and
  `DiscountRate` sit directly on each `<Promotion>`, and the club id is nested at
  `Clubs/ClubId` as a bare integer.
- **Shufersal / Carrefour dialect**: `<Promotion>` carries `PromotionID`, `PromotionDescription`,
  `MinNoOfItemOffered`, `RedemptionLimit`, `PromotionDays` and a flat `ClubID`, while
  `RewardType`, `MinQty`, `MaxQty`, `DiscountRate` and `MinPurchaseAmount` live one level deeper,
  inside `Groups/Group/PromotionItems/PromotionItem`.

`RewardType` values 1, 2, 3, 7 and 9 all occur on live feeds. The commonly-used readings are
1 = flat discounted price, 2 = fixed price for N units, 3 = Nth-item discount, but we could not
find an authoritative published mapping for any code, so treat these as conventions to confirm
against `PromotionDescription` rather than as specified semantics, and never auto-apply a code
you have not confirmed.

**Club-only handling is dialect-specific.** In the Cerberus dialect `Clubs/ClubId` is an integer
and `!= 0` means club-only. In the Shufersal dialect `ClubID` is a **string that begins with the
code**, e.g. `0 - כלל הלקוחות` for an open promotion. Comparing that string to `0` is always
unequal, so a parser applying the integer rule to Shufersal drops every promotion as club-only.
Parse the leading integer before the ` - ` separator, then test it. Club-restricted promotions
should NOT be applied to a guest basket.

**Filter promotions for validity before applying them.** A promotion is live only inside its
`PromotionStartDate`/`EndDate` window AND its `PromotionStartHour`/`EndHour`, and
`PromotionDays` can restrict it to particular days of the week. Applying an expired or
out-of-window promotion produces a basket total the user cannot reproduce at the till, which is
the most visible wrong answer this skill can give.

Handle substitutions: suggest cheaper alternatives for similar products.

Calculate total basket cost per scenario. Consider user preferences: kosher requirements, organic options, brand preferences.

### Step 5: Track Price Trends
Monitor prices over time for tracked products:
- Alert on significant changes (>10% increase or decrease)
- Weekly price trend report for tracked categories
- Track inflation patterns by food category
- Compare against CPI food component data

### Step 6: Restaurant/Catering Ingredient Cost Analysis
For restaurant owners: calculate ingredient costs from supermarket data.
- Input: recipe with ingredients and quantities
- Output: cost per serving based on cheapest available prices
- Track ingredient cost trends over time
- Alert when key ingredient prices spike
- Generate monthly cost report for menu pricing decisions

## Examples

### Example 1: Compare Milk Prices Across Chains
User says: "What's the cheapest place to buy Tnuva 3% milk 1 liter?"
Actions:
1. Query `PriceFull` feeds from the relevant chains and stores for the item (barcode matching)
2. Compile prices per chain and per store, keyed on `(ChainId, SubChainId, StoreId, ItemCode)`
3. Apply active promotions from `PromoFull`, filtered for validity window and club restriction
4. Generate a comparison table sorted by price

**Answer the price-control question first.** 3% milk is a controlled staple, so its shelf price is
capped and cross-chain spread is near zero. The honest answer here is "this item is price-capped,
you will not save meaningfully by switching chains for it", and then to point the user at
uncontrolled items in the same basket where the spread is real. Do not present a "switch and save"
recommendation on a controlled product, and do not quote prices from memory: read them from the
live feed, because they change daily.

### Example 2: Optimize Weekly Shopping List
User says: "Here's my shopping list for the week, find me the cheapest option near Ramat Gan"
Actions:
1. Parse shopping list (15 items)
2. Find prices at chains with stores near Ramat Gan
3. Calculate: single-store (Rami Levy: 285 NIS, Shufersal: 310 NIS, Yochananof: 295 NIS)
4. Calculate: optimal 2-store split (Rami Levy + Shufersal with promos: 262 NIS)
5. Suggest 3 substitutions saving additional 18 NIS
Result: Best single-store: Rami Levy at 285 NIS. Optimal split: Rami Levy (10 items, 195 NIS) + Shufersal (5 items with promos, 67 NIS) = 262 NIS. Total savings vs single-store: 23 NIS.

### Example 3: Track Ingredient Costs for Restaurant Menu
User says: "Track the cost of ingredients for my shakshuka dish, tomatoes, eggs, onions, peppers, spices"
Actions:
1. Identify matching products in price feeds (fresh tomatoes, eggs size L, yellow onions, bell peppers, cumin, paprika)
2. Find cheapest per ingredient across chains
3. Calculate cost per serving (2 eggs, 3 tomatoes, 1 onion, 1 pepper, spices)
4. Set up weekly price monitoring for these ingredients
5. Generate baseline cost report
Result: Current cost per serving: 8.40 NIS (cheapest chain combination). Eggs are 32% of cost. Price alert configured, you'll be notified if any ingredient price changes >10%.

## Bundled Resources

### References
- `references/chain-feeds.md` -- Per-chain feed endpoints organized by platform (Shufersal Direct, Carrefour Direct, Cerberus / PublishedPrices). Includes XML schema documentation, update schedules, and known format variations. Consult when accessing chain data in Steps 1-2.

### Scripts
- `scripts/parse_price_xml.py` -- Parses `PriceFull` and `PromoFull` feeds into normalized JSON. Auto-detects the XML dialect from the document, so it works for any chain (`--chain` is only a provenance label). Emits chain / sub-chain / store identity, parses promotions in both dialects including the club-id string form, detects gzip by magic bytes and handles UTF-16 with a BOM. Run: `python3 scripts/parse_price_xml.py --help`

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Israeli Supermarket Prices](https://agentskills.co.il/he/mcp/supermarket-prices) | Wraps the Price Transparency Law feeds across the chains it covers. Handles Shufersal direct, Carrefour publishprice, and Cerberus FTP transports automatically. Use it instead of the manual XML steps when available. |
| [Shufersal MCP](https://agentskills.co.il/he/mcp/shufersal) | Adds cart automation on shufersal.co.il (search, add to cart, recipe-to-cart). Complements price intelligence with the actual checkout flow. |

## Gotchas

- Do not assume a chain is on Cerberus. Rami Levy, Yochananof, Osher Ad, Tiv Taam and Dor Alon are; **Victory, Super-Pharm, Good Pharm, Bareket and Mega are not**, and Hazi Hinam logs in to Cerberus with an empty listing while publishing a full file table on its own site. Equally, do not fabricate a `prices.<chain>.co.il` host, most chains have none. Consult `references/chain-feeds.md` and re-probe before concluding a chain stopped publishing.
- Cerberus is NOT a static file server, and its directory listing is a **POST, not a GET**. A GET on `/file/json/dir` returns HTTP 200 carrying `{"aaData":[],"error":"Invalid request method used for this operation."}`, which reads as "this chain has no files" unless you inspect the `error` key. The listing POST also needs a csrftoken read from `/file` **after** login, not the one from the pre-login page. A `/file/d/<filename>` request with no session answers **HTTP 302** with a short redirect stub rather than the file, so require both a 2xx status and a gzip payload before treating a response as data.
- The legacy "Nibit (Matrix)" host `matrixcatalog.co.il` no longer resolves at all (NXDOMAIN as of 2026-08-27), so a request fails at DNS rather than timing out. Its successor for Victory and Mahsani A'Shuk is `laibcatalog.co.il`, which resolves but refused connections from our probe; confirm its state before building on it.
- Prices in Israel include VAT (18%) by default, unlike US prices which are pre-tax. The 18% rate has been in effect since 1 Jan 2025 (raised from 17%); a proposed Jan 2026 increase to 19% was rejected in the Knesset budget vote. Agents trained before 2025 may "correct" 18% back to 17%, they should not. Agents may also perform cost comparisons that double-count or ignore VAT depending on their training data assumptions.
- Israeli product barcodes use the 729 country prefix, but some imported products retain their original country barcode. Agents may fail cross-chain matching when the same product has different barcode formats across chains. Store-brand items often use internal codes starting with `2` and cannot be cross-matched at all.
- The club-id field is named and typed differently per dialect: nested integer `Clubs/ClubId` on Cerberus feeds, flat string `ClubID` like `0 - כלל הלקוחות` on Shufersal/Carrefour. Applying the Cerberus integer test to a Shufersal string marks every promotion club-only and silently discards all of them; ignoring the field entirely reports inflated savings. Parse the leading code, then test it.
- "Mega" and "Yeinot Bitan" did not fully rebrand to Carrefour. One publisher covers all three banners: Carrefour Israel's own `Stores` feed lists `בעיר` and `יינות ביתן` branded stores alongside Carrefour ones. There is no separate working Mega feed to fall back on, the standalone `prices.mega.co.il` host answers 403 and a Cerberus login as `Mega` fails. "Victory" is a different company entirely, not a Carrefour banner, and agents routinely confuse the two. Victory also runs several banners that can price the same SKU differently, so key the comparison on the specific banner and store, not on "Victory" as one entity.
- Pharmacy chains (Super-Pharm, Good Pharm) ARE covered by the law and do publish, but **not through Cerberus**: Super-Pharm runs its own portal at `prices.super-pharm.co.il` and Good Pharm publishes via Bina Projects. Their SKU range is drugstore items (toiletries, OTC, baby food) without fresh produce, dairy, or meat, so don't try to price-compare milk at Super-Pharm.
- `RewardType` and its `MinQty` / `MaxQty` / `DiscountRate` siblings sit on the `<Promotion>` element in the Cerberus dialect but one level deeper, on each `PromotionItem` inside `Groups/Group`, in the Shufersal/Carrefour dialect. A parser written to one shape finds nothing in the other and reports zero promotions. Note also `MinPurchaseAmount` (Shufersal) vs `MinPurchaseAmnt`, and `MinNoOfItemOffered` vs `MinNoOfItemOfered`, the spellings genuinely differ between feeds.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Wikisource, Promotion of Competition in the Food Sector Law (statute text) | https://he.wikisource.org/wiki/חוק_קידום_התחרות_בענף_המזון | Plain-language summary, legislative history, recent amendments |
| Ministry of Economy, price-publication regulations | https://www.gov.il/he/pages/cpfta_prices_regulations | The file specification behind the six file types, naming and encoding rules. Cloudflare-protected, so open it in a browser |
| Shufersal Direct Portal | https://prices.shufersal.co.il | Live PriceFull/PricesPromotions/Stores feeds for Shufersal |
| Cerberus PublishedPrices Portal | https://url.publishedprices.co.il/login | Live feeds for Rami Levy, Yochananof, Tiv Taam, Osher Ad, Dor Alon and other Cerberus chains. Victory, Super-Pharm, Good Pharm, Bareket and Mega are NOT here, see the platform table |
| Carrefour Israel Direct Portal | https://prices.carrefour.co.il | Live feeds for Carrefour / Mega / Yeinot Bitan stores |
| OpenIsraeliSupermarkets, community parsers | https://github.com/OpenIsraeliSupermarkets | Reference Python scrapers and parsers used by the community. The active library is `il-supermarket-scraper` (PyPI), which handles Cerberus CSRF login, chain-code lookup, file listing, and decompression. Its scraper classes are also the best available cross-check of which platform each chain currently publishes on |
| Super-Pharm price portal | http://prices.super-pharm.co.il | Super-Pharm's own feed listing (it is not on Cerberus) |
| Bina Projects portal (Good Pharm) | https://goodpharm.binaprojects.com/Main.aspx | Good Pharm and several small chains publish here |
| Hazi Hinam price files | https://shop.hazi-hinam.co.il/Prices | Hazi Hinam's own file table |
| Israel Tax Authority, Interpretation Directive 01/2025 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-051224-2/he/vat_represent-info-051224-2.pdf | Current Israeli VAT rate (18% since 1 Jan 2025), includes historical rate changes |

## Troubleshooting

### Error: "XML feed download failed"
Cause: for Shufersal specifically, the most likely cause is an **expired signed URL**. Download links from the Shufersal portal are Azure Blob URLs carrying an `se=` expiry about half an hour out and pinned to a clock boundary, so a link captured earlier, cached, or copied from documentation will fail. Otherwise the chain moved platform (see the platform table) or the file genuinely is not published yet.
Solution: re-list the files immediately before each download rather than reusing a stored URL. For other platforms, re-probe the listing endpoint and check the chain has not migrated. Feeds are refreshed overnight, so a missing PriceFull early in the day is expected rather than an error.

### Error: "Product not found in cross-chain comparison"
Cause: Product naming or barcode differs across chains.
Solution: Try matching by barcode first (most reliable). If barcode match fails, use fuzzy name matching with manufacturer. Some chains use different product names for the same item (e.g., "חלב תנובה 3%" vs "חלב 3% תנובה").

### Error: "Price data outdated"
Cause: Using cached data from a previous day or the chain hasn't updated yet.
Solution: Check the UpdateDate field in the XML feed. Most chains update overnight. If data is >24 hours old, force a fresh download. Promotions feed updates may lag behind PricesFull updates.

### Error: "Shopping list optimization slow"
Cause: Comparing all items across all chains and all stores is computationally expensive.
Solution: Limit comparison to chains with stores within a configurable radius (default: 5 km). Pre-filter by chains the user actually shops at. Use cached price data instead of fetching fresh for every optimization.

### Error: "Cerberus returns an empty file list"
Cause (verified 2026-08-27): the listing was requested with GET. `/file/json/dir` accepts POST only and answers a GET with HTTP 200 plus `{"aaData":[],"error":"Invalid request method used for this operation."}`. The second verified cause is a stale csrftoken, the listing needs the token rendered on `/file` after login, not the pre-login one.
Verified NOT to be the cause: an unusual User-Agent. Every probe behind this section ran with the stock `curl` User-Agent and completed login, listing and download without being blocked.
Solution: follow the flow in `references/chain-feeds.md` and always read the `error` key before treating an empty `aaData` as "no files".

### Error: "Chain logs in to Cerberus but has no files"
Cause (verified 2026-08-27): the chain does not publish through Cerberus. `Victory`, `SuperPharm`, `GoodPharm`, `Bareket` and `Mega` fail login outright (200 + re-rendered form instead of 302); `HaziHinam` authenticates but lists zero files while serving a full table at `shop.hazi-hinam.co.il/Prices`.
Solution: look up the chain's real platform in `references/chain-feeds.md` before concluding it stopped publishing. A confident "chain X does not publish" needs a positive search for chain X's own portal.
