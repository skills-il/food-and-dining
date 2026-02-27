---
name: israeli-grocery-price-intelligence
description: >-
  Access and compare Israeli supermarket prices using mandatory Price
  Transparency Law data feeds. Use when user asks about "supermarket prices
  Israel", "price comparison Shufersal", "Rami Levy prices", "grocery prices",
  "Price Transparency Law", "shopping list optimizer", "food costs Israel",
  or "השוואת מחירי סופר". Covers chain-specific XML feed parsing, cross-chain
  price comparison, shopping list optimization, price trend tracking, and
  restaurant ingredient cost analysis. Do NOT use for restaurant operations
  (use israeli-restaurant-ops) or non-food retail prices.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: >-
  Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled
  price monitoring and automated shopping list optimization.
metadata:
  author: skills-il
  version: 1.0.0
  category: food-and-dining
  tags:
    - grocery
    - supermarket
    - prices
    - price-comparison
    - shufersal
    - rami-levy
    - israel
  display_name:
    he: מודיעין מחירי מכולת ישראלי
    en: Israeli Grocery Price Intelligence
  display_description:
    he: השוואת מחירי סופרמרקטים ישראליים באמצעות נתוני חוק שקיפות מחירים — שופרסל, רמי לוי, יוחננוף ועוד
    en: >-
      Access and compare Israeli supermarket prices using mandatory Price
      Transparency Law data feeds.
  openclaw:
    requires:
      bins: []
      env: []
    emoji: "🏷️"
---

# Israeli Grocery Price Intelligence

## Instructions

### Step 1: Access Supermarket XML Feeds
Under the 2015 Price Transparency Law (חוק שקיפות מחירים), Israeli supermarket chains with 3+ stores must publish product prices as XML files.
- Data published at: prices.shufersal.co.il, and similar portals per chain
- Available data files:
  - **PricesFull** — complete product catalog with prices
  - **PricesPromotions** — current sales and promotions
  - **Stores** — store locations and details
- Files updated daily (typically overnight)
- See `references/chain-feeds.md` for per-chain URLs and access methods

### Step 2: Parse Chain-Specific Data Formats
Each chain publishes in a slightly different XML schema. Supported chains and their format:

| Chain | Hebrew Name | Feed URL Pattern | Notes |
|-------|-------------|------------------|-------|
| Shufersal | שופרסל | prices.shufersal.co.il | Largest chain, most structured data |
| Rami Levy | רמי לוי | prices.rframi.co.il | Known for low prices |
| Yochananof | יוחננוף | prices.ybitan.co.il | Central Israel focus |
| Victory / Mega | ויקטורי / מגה | prices.mega.co.il | Merged under Alon group |
| Osher Ad | אושר עד | prices.osherad.co.il | Discount chain |
| Tiv Taam | טיב טעם | prices.tivtaam.co.il | Non-kosher items available |

Use `scripts/parse_price_xml.py` to parse feeds into normalized JSON format.
Key fields: item_code, item_name, manufacturer, price, unit_price, quantity, unit_of_measure, update_date

### Step 3: Cross-Chain Price Comparison
Match products across chains by:
- **Barcode** (most reliable — Israeli standard barcode)
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
User says: "Track the cost of ingredients for my shakshuka dish — tomatoes, eggs, onions, peppers, spices"
Actions:
1. Identify matching products in price feeds (fresh tomatoes, eggs size L, yellow onions, bell peppers, cumin, paprika)
2. Find cheapest per ingredient across chains
3. Calculate cost per serving (2 eggs, 3 tomatoes, 1 onion, 1 pepper, spices)
4. Set up weekly price monitoring for these ingredients
5. Generate baseline cost report
Result: Current cost per serving: 8.40 NIS (cheapest chain combination). Eggs are 32% of cost. Price alert configured — you'll be notified if any ingredient price changes >10%.

## Bundled Resources

### References
- `references/chain-feeds.md` — URLs and access methods for each Israeli supermarket chain's price transparency feeds. Includes XML schema documentation, update schedules, and known format variations. Consult when accessing chain data in Steps 1-2.

### Scripts
- `scripts/parse_price_xml.py` — Parses Israeli supermarket XML price feeds into normalized JSON. Supports Shufersal, Rami Levy, and other chain formats. Handles gzipped XML files and character encoding. Run: `python scripts/parse_price_xml.py --help`

## Troubleshooting

### Error: "XML feed download failed"
Cause: Chain's price transparency server is temporarily down or URL has changed.
Solution: Check if the chain updated their feed URL (this happens occasionally). Try accessing the feed manually in a browser. Feeds are typically most reliable in the morning hours (updated overnight). See `references/chain-feeds.md` for current URLs.

### Error: "Product not found in cross-chain comparison"
Cause: Product naming or barcode differs across chains.
Solution: Try matching by barcode first (most reliable). If barcode match fails, use fuzzy name matching with manufacturer. Some chains use different product names for the same item (e.g., "חלב תנובה 3%" vs "חלב 3% תנובה").

### Error: "Price data outdated"
Cause: Using cached data from a previous day or the chain hasn't updated yet.
Solution: Check the UpdateDate field in the XML feed. Most chains update overnight. If data is >24 hours old, force a fresh download. Promotions feed updates may lag behind PricesFull updates.

### Error: "Shopping list optimization slow"
Cause: Comparing all items across all chains and all stores is computationally expensive.
Solution: Limit comparison to chains with stores within a configurable radius (default: 5 km). Pre-filter by chains the user actually shops at. Use cached price data instead of fetching fresh for every optimization.
