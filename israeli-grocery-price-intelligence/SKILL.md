---
name: israeli-grocery-price-intelligence
description: Access and compare Israeli supermarket prices using mandatory Price Transparency Law data feeds. Use when user asks about "supermarket prices Israel", "price comparison Shufersal", "Rami Levy prices", "grocery prices", "Price Transparency Law", "shopping list optimizer", "food costs Israel", or "השוואת מחירי סופר". Covers chain-specific XML feed parsing, cross-chain price comparison, shopping list optimization, price trend tracking, and restaurant ingredient cost analysis. Do NOT use for restaurant operations (use israeli-restaurant-ops) or non-food retail prices.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled price monitoring and automated shopping list optimization.
---


# Israeli Grocery Price Intelligence

## Instructions

### Preferred: Use the Supermarket Prices MCP Server

If the user has the **supermarket-prices** MCP server installed, use it instead of manually fetching XML feeds. The MCP handles authentication, CSRF tokens, SSL issues, and platform quirks automatically.

Install instructions: https://agentskills.co.il/he/mcp/supermarket-prices

Available MCP tools:
- `list_chains` -- list all ~35 chains with data source info (web / publishprice / FTP)
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
- File naming format: `Price{Full}<ChainId>-<StoreId>-<yyyyMMddHHmm>.xml.gz` where ChainId is the 13-digit Israeli EAN prefix and the timestamp is the file generation moment in Israel time
- Full snapshots typically refreshed daily (overnight, 01:00-05:00 IL time); delta files may be pushed several times per day
- See `references/chain-feeds.md` for per-chain endpoints, access methods, and Cerberus authentication

Chains publish through three platforms (not individual domains):

| Platform | URL | Chains |
|----------|-----|--------|
| Shufersal Direct | https://prices.shufersal.co.il | Shufersal |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (operates Carrefour, Mega, and Yeinot Bitan branded stores under one Electra franchise) |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy, Yochananof, Victory, Osher Ad, Tiv Taam, Hazi Hinam, Mega (legacy feed), Dor Alon, Super-Pharm, Good Pharm, and ~20 more smaller chains. Total ~30 chains across this platform |

The previously separate "Nibit (Matrix)" platform at `matrixcatalog.co.il` is no longer reachable (the host times out as of May 2026). Victory and other chains formerly published there now publish through the Cerberus platform.

**Cerberus requires real authentication, not just a URL fetch.** A GET on the file directory without an active session returns the login HTML, not data. The flow is: GET `/login` → parse the `<meta name="csrftoken">` value AND keep the response cookie → POST `/login` with `username=<chain-code>`, `password=<password-or-empty>`, `csrftoken=<value>` → reuse the cookie for `/file/json/dir` to list files and `/file/d/<filename>` to download. See `references/chain-feeds.md` for the full flow and per-chain credentials.

### Step 2: Parse Chain-Specific Data Formats
Each chain publishes in a slightly different XML schema. Major chains:

| Chain | Hebrew Name | Platform | Notes |
|-------|-------------|----------|-------|
| Shufersal | שופרסל | Direct (prices.shufersal.co.il) | Largest chain (~400 stores across Shufersal Deal, Sheli, Yesh, and Express banners), most structured data |
| Rami Levy | רמי לוי | Cerberus | Known for low prices, 50+ stores |
| Yochananof | יוחננוף | Cerberus | Central Israel focus |
| Victory | ויקטורי | Cerberus | Independently owned (Ravid family, publicly traded VCTR.TA), 60+ stores; completely separate from Carrefour Israel |
| Carrefour Israel | קרפור ישראל | Direct (prices.carrefour.co.il) | Electra Consumer Products franchise; operates Carrefour, Mega, and Yeinot Bitan branded stores in parallel (not all stores converted to Carrefour) |
| Osher Ad | אושר עד | Cerberus (username: `osherad`, no password) | Discount chain, 20+ large-format stores |
| Tiv Taam | טיב טעם | Cerberus | Non-kosher items available; merged with East & West Import & Marketing Dec 2024 |

Use `scripts/parse_price_xml.py` to parse feeds into normalized JSON format.
Key fields: item_code, item_name, manufacturer, price, unit_price, quantity, unit_of_measure, is_weighted, update_date

**Weighted-item math:** when `bIsWeighted=1`, `ItemPrice` is the price per kilogram, NOT the price of the package on the shelf. `Quantity` may be empty or fractional. Cross-chain comparisons must compare per-kg unit prices for these items, otherwise a 250g pack at 12 NIS/kg (= 3 NIS at the till) looks more expensive than a 1kg pack at 11 NIS/kg.

### Step 3: Cross-Chain Price Comparison
Match products across chains by:
- **Barcode** (most reliable, Israeli standard barcode prefix 729)
- **Item name + manufacturer** (fuzzy matching for naming differences)
- **Item code** (chain-specific, less reliable for cross-chain)

Generate comparison table for specific products:
- Calculate: cheapest chain, average price, price spread (max-min)
- Handle store-specific pricing (same chain may have different prices by location)

### Step 4: Optimize Shopping Lists
Given a shopping list, find the cheapest option:
- **Single-store:** cheapest store for entire basket
- **Multi-store:** optimal split across 2-3 nearby stores (minimize cost + travel)

Factor in current promotions from the `PromoFull` feed. Each promotion has a `RewardType` that controls how the discount applies (1 = flat discounted price, 2 = fixed price for N units, 3 = Nth-item discount, etc.), plus `MinQty` / `MaxQty` thresholds, an optional `MinPurchaseAmnt`, and a `ClubId`. A non-zero `ClubId` means the discount applies only to chain club members (Shufersal Sofash, Rami Levy club, etc.) and should NOT be applied to a guest basket. Handle substitutions: suggest cheaper alternatives for similar products.

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
1. Query PricesFull feeds from all chains for item (barcode matching)
2. Compile prices per chain and store location
3. Apply any active promotions from PricesPromotions
4. Generate comparison table sorted by price
Result: Cheapest: Rami Levy at 5.90 NIS, Osher Ad at 6.10 NIS, Shufersal at 6.50 NIS (but 2-for-10 promo active). With Shufersal promo, buying 2 = 5.00 NIS each. Recommendation: Shufersal if buying 2+, Rami Levy for single.

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
- `scripts/parse_price_xml.py` -- Parses Israeli supermarket XML price feeds into normalized JSON. Supports Shufersal, Rami Levy, and other chain formats. Handles gzipped XML files and character encoding. Run: `python scripts/parse_price_xml.py --help`

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Israeli Supermarket Prices](https://agentskills.co.il/he/mcp/supermarket-prices) | Wraps the Price Transparency Law feeds across ~35 chains. Handles Shufersal direct, Carrefour publishprice, and Cerberus FTP transports automatically. Use it instead of the manual XML steps when available. |
| [Shufersal MCP](https://agentskills.co.il/he/mcp/shufersal) | Adds cart automation on shufersal.co.il (search, add to cart, recipe-to-cart). Complements price intelligence with the actual checkout flow. |

## Gotchas

- Most chains do NOT have their own `prices.X.co.il` domain. Rami Levy, Yochananof, Victory, Osher Ad, Tiv Taam, and ~20 other chains all publish through the Cerberus platform at `url.publishedprices.co.il`. Agents that fabricate per-chain URLs will get connection errors. Always consult `references/chain-feeds.md` for verified endpoints.
- Cerberus is NOT a static file server. A naive `curl https://url.publishedprices.co.il/file/d/PriceFull...xml.gz` returns the login page (HTTP 200 with HTML, not the file). You must first GET `/login`, parse the `csrftoken` from the `<meta name="csrftoken">` tag, keep the response cookie, then POST `/login` with the chain username, an empty password if the chain is public, and the csrftoken. Only then do file listing and download endpoints return data.
- The legacy "Nibit (Matrix)" platform at `matrixcatalog.co.il/NBCompetitionRegulations.aspx` is no longer reachable as of May 2026 (curl times out after 10s). Victory and other chains that previously published there now use Cerberus. Skills or agents still pointing at matrixcatalog.co.il will fail.
- Prices in Israel include VAT (18%) by default, unlike US prices which are pre-tax. The 18% rate has been in effect since 1 Jan 2025 (raised from 17%); a proposed Jan 2026 increase to 19% was rejected in the Knesset budget vote. Agents trained before 2025 may "correct" 18% back to 17% — they should not. Agents may also perform cost comparisons that double-count or ignore VAT depending on their training data assumptions.
- Israeli product barcodes use the 729 country prefix, but some imported products retain their original country barcode. Agents may fail cross-chain matching when the same product has different barcode formats across chains. Store-brand items often use internal codes starting with `2` and cannot be cross-matched at all.
- Promotions with `ClubId != 0` are restricted to chain club members (Shufersal Sofash, Rami Levy club, Yochananof Club, etc.) and should NOT be applied to a generic basket-cost estimate. Many naive agents ignore `ClubId` and report inflated savings.
- "Mega" and "Yeinot Bitan" did not fully rebrand to Carrefour. The Electra Consumer Products franchise (April 2022, 20-year term) operates all three banners in parallel; some stores were converted to Carrefour, others retained the Mega or Yeinot Bitan banner. A legacy "Mega" feed still exists on Cerberus alongside the Carrefour Direct portal. "Victory" is a completely separate, independently owned company (Ravid family, VCTR.TA). Agents may still confuse these as related entities.
- Pharmacy chains (Super-Pharm, Good Pharm) ARE covered by the law and publish through Cerberus, but their SKU range is drugstore items (toiletries, OTC, baby food) without fresh produce, dairy, or meat. Don't try to price-compare milk at Super-Pharm.
- Promotions in Israeli supermarkets often have conditions agents miss: "buy 2 get discount" (2 b-X shekel) is `RewardType=2` with `MinQty=2`; "buy 3 pay for 2" is `RewardType=3`; some have `MinPurchaseAmnt` thresholds; regional promotions apply only to specific store IDs.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Wikipedia, Promotion of Competition in Food and Pharma Law (Hebrew) | https://he.wikipedia.org/wiki/חוק_קידום_התחרות_בענפי_המזון_והפארם | Plain-language summary, legislative history, recent amendments |
| Wikipedia, List of supermarket chains in Israel | https://en.wikipedia.org/wiki/List_of_supermarket_chains_in_Israel | Current chain ownership, store counts, brand consolidations |
| Shufersal Direct Portal | https://prices.shufersal.co.il | Live PriceFull/PricesPromotions/Stores feeds for Shufersal |
| Cerberus PublishedPrices Portal | https://url.publishedprices.co.il/login | Live feeds for Rami Levy, Yochananof, Victory, Tiv Taam, Osher Ad, Mega, and ~25 other chains |
| Carrefour Israel Direct Portal | https://prices.carrefour.co.il | Live feeds for Carrefour / Mega / Yeinot Bitan stores |
| OpenIsraeliSupermarkets, community parsers | https://github.com/OpenIsraeliSupermarkets | Reference Python scrapers and parsers used by the community. The active library is `il-supermarket-scraper` (PyPI), which handles Cerberus CSRF login, chain-code lookup, file listing, and decompression |
| Wikipedia, Taxation in Israel | https://en.wikipedia.org/wiki/Taxation_in_Israel | Current Israeli VAT rate (18% since 1 Jan 2025), includes historical rate changes |

## Troubleshooting

### Error: "XML feed download failed"
Cause: Chain's price transparency server is temporarily down or URL has changed.
Solution: Check if the chain updated their feed URL (this happens occasionally). The Cerberus platform occasionally has SSL certificate issues; try HTTP if HTTPS fails. Feeds are typically most reliable in the morning hours (updated overnight). See `references/chain-feeds.md` for current URLs.

### Error: "Product not found in cross-chain comparison"
Cause: Product naming or barcode differs across chains.
Solution: Try matching by barcode first (most reliable). If barcode match fails, use fuzzy name matching with manufacturer. Some chains use different product names for the same item (e.g., "חלב תנובה 3%" vs "חלב 3% תנובה").

### Error: "Price data outdated"
Cause: Using cached data from a previous day or the chain hasn't updated yet.
Solution: Check the UpdateDate field in the XML feed. Most chains update overnight. If data is >24 hours old, force a fresh download. Promotions feed updates may lag behind PricesFull updates.

### Error: "Shopping list optimization slow"
Cause: Comparing all items across all chains and all stores is computationally expensive.
Solution: Limit comparison to chains with stores within a configurable radius (default: 5 km). Pre-filter by chains the user actually shops at. Use cached price data instead of fetching fresh for every optimization.

### Error: "Cerberus platform returns empty page or login prompt"
Cause: Cerberus requires an authenticated session, not a one-shot URL fetch. The most common failure mode is omitting the CSRF token or the session cookie.
Solution: Follow the full Cerberus auth flow documented in `references/chain-feeds.md`: GET `/login`, extract the `csrftoken` `<meta>` value AND save the cookie from the response, POST `/login` with `username=<chain-code>`, `password=` (empty for public chains), and `csrftoken=<value>`, reuse the cookie for `/file/json/dir` and `/file/d/<filename>`. Add a ≥1s delay between requests and use a realistic User-Agent header — Cerberus throttles aggressive listing.
