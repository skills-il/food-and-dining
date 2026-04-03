---
name: israeli-grocery-price-intelligence
description: Access and compare Israeli supermarket prices using mandatory Price Transparency Law data feeds. Use when user asks about "supermarket prices Israel", "price comparison Shufersal", "Rami Levy prices", "grocery prices", "Price Transparency Law", "shopping list optimizer", "food costs Israel", or "השוואת מחירי סופר". Covers chain-specific XML feed parsing, cross-chain price comparison, shopping list optimization, price trend tracking, and restaurant ingredient cost analysis. Do NOT use for restaurant operations (use israeli-restaurant-ops) or non-food retail prices.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled price monitoring and automated shopping list optimization.
---


# Israeli Grocery Price Intelligence

## Instructions

### Step 1: Access Supermarket XML Feeds
Under the 2015 Price Transparency Law (חוק שקיפות מחירים), Israeli supermarket chains with 3+ stores must publish product prices as XML files.
- Available data files per chain:
  - **PricesFull** -- complete product catalog with prices
  - **PricesPromotions** -- current sales and promotions
  - **Stores** -- store locations and details
- Files updated daily (typically overnight)
- See `references/chain-feeds.md` for per-chain URLs and access methods

Chains publish through three platforms (not individual domains):

| Platform | URL | Chains |
|----------|-----|--------|
| Shufersal Direct | http://prices.shufersal.co.il | Shufersal |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy, Yochananof, Osher Ad, Tiv Taam, and smaller chains |
| Nibit (Matrix) | http://matrixcatalog.co.il/NBCompetitionRegulations.aspx | Victory |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (formerly Mega/Yeinot Bitan) |

### Step 2: Parse Chain-Specific Data Formats
Each chain publishes in a slightly different XML schema. Major chains:

| Chain | Hebrew Name | Platform | Notes |
|-------|-------------|----------|-------|
| Shufersal | שופרסל | Direct (prices.shufersal.co.il) | Largest chain (850+ stores), most structured data |
| Rami Levy | רמי לוי | Cerberus | Known for low prices, 30+ stores |
| Yochananof | יוחננוף | Cerberus | Central Israel focus |
| Victory | ויקטורי | Nibit (Matrix) | Independently owned (Ravid family, publicly traded VCTR.TA) |
| Carrefour Israel | קרפור ישראל | Direct (prices.carrefour.co.il) | Operates under Carrefour, Mega, and Yeinot Bitan brands |
| Osher Ad | אושר עד | Cerberus (username: `osherad`, no password) | Discount chain, 20+ large-format stores |
| Tiv Taam | טיב טעם | Cerberus | Non-kosher items available |

Use `scripts/parse_price_xml.py` to parse feeds into normalized JSON format.
Key fields: item_code, item_name, manufacturer, price, unit_price, quantity, unit_of_measure, update_date

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

Factor in current promotions (PricesPromotions feed). Handle substitutions: suggest cheaper alternatives for similar products.

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
- `references/chain-feeds.md` -- Per-chain feed URLs organized by platform (Shufersal Direct, Cerberus, Nibit, Carrefour Direct). Includes XML schema documentation, update schedules, and known format variations. Consult when accessing chain data in Steps 1-2.

### Scripts
- `scripts/parse_price_xml.py` -- Parses Israeli supermarket XML price feeds into normalized JSON. Supports Shufersal, Rami Levy, and other chain formats. Handles gzipped XML files and character encoding. Run: `python scripts/parse_price_xml.py --help`

## Gotchas

- Most chains do NOT have their own `prices.X.co.il` domain. Rami Levy, Yochananof, Osher Ad, and Tiv Taam all publish through the Cerberus platform at `publishedprices.co.il`. Victory publishes through Nibit at `matrixcatalog.co.il`. Agents that fabricate per-chain URLs will get connection errors. Always consult `references/chain-feeds.md` for verified endpoints.
- Prices in Israel include VAT (18% as of 2025) by default, unlike US prices which are pre-tax. Agents may perform cost comparisons that double-count or ignore VAT depending on their training data assumptions.
- Israeli product barcodes use the 729 country prefix, but some imported products retain their original country barcode. Agents may fail cross-chain matching when the same product has different barcode formats across chains.
- "Mega" and "Yeinot Bitan" rebranded to Carrefour Israel (Electra Consumer Products franchise). The old feed domain `publishprice.mega.co.il` redirects to `prices.carrefour.co.il`. "Victory" is a completely separate, independently owned company (Ravid family). Agents may still confuse these as related entities.
- Promotions in Israeli supermarkets often have conditions agents miss: "buy 2 get discount" (2 b-X shekel), club-member-only pricing, or regional promotions that apply only to specific store locations.

## Troubleshooting

### Error: "XML feed download failed"
Cause: Chain's price transparency server is temporarily down or URL has changed.
Solution: Check if the chain updated their feed URL (this happens occasionally). Cerberus and Nibit platforms may have SSL certificate issues; try HTTP if HTTPS fails. Feeds are typically most reliable in the morning hours (updated overnight). See `references/chain-feeds.md` for current URLs.

### Error: "Product not found in cross-chain comparison"
Cause: Product naming or barcode differs across chains.
Solution: Try matching by barcode first (most reliable). If barcode match fails, use fuzzy name matching with manufacturer. Some chains use different product names for the same item (e.g., "חלב תנובה 3%" vs "חלב 3% תנובה").

### Error: "Price data outdated"
Cause: Using cached data from a previous day or the chain hasn't updated yet.
Solution: Check the UpdateDate field in the XML feed. Most chains update overnight. If data is >24 hours old, force a fresh download. Promotions feed updates may lag behind PricesFull updates.

### Error: "Shopping list optimization slow"
Cause: Comparing all items across all chains and all stores is computationally expensive.
Solution: Limit comparison to chains with stores within a configurable radius (default: 5 km). Pre-filter by chains the user actually shops at. Use cached price data instead of fetching fresh for every optimization.

### Error: "Cerberus/Nibit platform returns empty page or login prompt"
Cause: Platform may require chain selection before listing files, or may block automated requests.
Solution: When accessing Cerberus, pass the chain identifier in the request (each chain has a code). For Nibit, select the chain from the dropdown. If blocked, add a delay between requests and use standard browser headers. Check `references/chain-feeds.md` for platform-specific access notes.
