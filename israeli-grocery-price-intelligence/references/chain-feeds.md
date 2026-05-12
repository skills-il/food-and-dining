# Israeli Supermarket Chain Price Feeds

## Overview

Under the Promotion of Competition in the Food and Pharma Sector Law (חוק קידום התחרות בענפי המזון והפארם, 2014, in force since 2015), supermarket AND pharmacy chains with 3 or more stores must publish product prices as machine-readable XML files. The Ministry of Economy's Competition Authority publishes the file spec ("פרסום מחירים, מפרט קבצים"). Files must be UTF-8 encoded.

## Feed Types

Per the government spec, every regulated chain publishes six file types: full snapshots and delta updates for prices, promotions, and stores.

| File Type | Prefix | Content | Update Frequency |
|-----------|--------|---------|-----------------|
| Full price snapshot | `PriceFull` | Complete product catalog with current prices | Daily (overnight, 01:00-05:00 IL time) |
| Price delta | `Price` | Changes between full snapshots | Multiple times per day, on price change |
| Full promo snapshot | `PromoFull` | Active sales, discounts, multi-buy deals | Daily (may lag `PriceFull`) |
| Promo delta | `Promo` | Promotion changes between full snapshots | On promo change |
| Full store list | `StoresFull` | All stores with addresses and operating hours | Weekly or on change |
| Store delta | `Stores` | Store changes (openings, closures, hour updates) | On change |

**File naming format** (per the spec): `<Prefix><ChainId>-<StoreId>-<yyyyMMddHHmm>.xml.gz` where:
- `Prefix` is one of the six above (`PriceFull`, `Price`, `PromoFull`, `Promo`, `StoresFull`, `Stores`)
- `ChainId` is the 13-digit Israeli EAN-style chain identifier (starts with `729...` for Israeli chains)
- `StoreId` is the chain-internal store number (3-4 digits typically)
- `yyyyMMddHHmm` is the file generation timestamp in Israel time (no seconds)

Example: `PriceFull7290027600007-001-202605120300.xml.gz` is Shufersal store 001, generated at 03:00 on 12 May 2026.

## Feed Platforms

Not every chain runs its own server. Most chains publish through one of three centralized platforms:

| Platform | URL | Chains Using It |
|----------|-----|-----------------|
| Shufersal Direct | https://prices.shufersal.co.il | Shufersal only |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (Carrefour + Mega + Yeinot Bitan branded stores under one Electra franchise) |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy, Yochananof, Victory, Osher Ad, Tiv Taam, Hazi Hinam, Mega (legacy feed), Dor Alon, Bareket, Keshet Taamim, Fresh Market / Super Dosh, Mahsani A'Shuk, Cofix, Super-Pharm, Good Pharm, and ~15 more smaller chains. Around 30 chains total |

Shufersal and Carrefour Israel have dedicated portals with per-store file downloads, no authentication required.

The previously separate "Nibit (Matrix Catalog)" platform at `matrixcatalog.co.il/NBCompetitionRegulations.aspx` is no longer reachable as of May 2026 (the host times out after 10s). Victory and other formerly-Nibit chains have migrated to Cerberus.

## Cerberus Authentication Flow

Cerberus is NOT a static file server. It is a stateful web app (CerberusFTPServer) that enforces CSRF protection and session cookies. A naive `curl https://url.publishedprices.co.il/file/d/<filename>.gz` returns the login HTML, not the file. The flow:

**Step 1 — fetch the login page and capture both the CSRF token and the session cookie:**
```bash
curl -sS -c cerberus_cookies.txt -A "Mozilla/5.0" \
  "https://url.publishedprices.co.il/login" -o login.html
csrftoken=$(grep -oE 'name="csrftoken" content="[^"]+"' login.html | sed 's/.*content="\([^"]*\)".*/\1/')
```

The csrftoken appears in a `<meta name="csrftoken" content="...">` tag in the response HTML, NOT as a hidden form input.

**Step 2 — POST credentials with the csrftoken and the saved cookie jar:**
```bash
curl -sS -b cerberus_cookies.txt -c cerberus_cookies.txt -A "Mozilla/5.0" \
  -X POST "https://url.publishedprices.co.il/login/user" \
  -d "username=<chain-code>&password=<password-or-empty>&csrftoken=$csrftoken" \
  -o /dev/null
```

For public chains (`RamiLevi`, `yohananof`, `Carrefour`, `osherad`, `TivTaam`, etc.) the password is empty.

**Step 3 — reuse the cookie jar for file listing and downloads:**
```bash
# List available files (returns JSON)
curl -sS -b cerberus_cookies.txt "https://url.publishedprices.co.il/file/json/dir"

# Download a specific file
curl -sS -b cerberus_cookies.txt "https://url.publishedprices.co.il/file/d/PriceFull7290058140886-001-202605120300.gz" -o PriceFull.gz
```

**Anti-bot considerations:**
- Use a realistic User-Agent header. The default `curl` UA will get blocked.
- Add a >=1 second delay between requests; Cerberus throttles aggressive listing.
- Sessions expire after ~30 minutes of inactivity. Re-login on 401 responses.
- The `il-supermarket-scraper` PyPI package handles all of the above automatically.

## Per-Chain Feed Access

### Shufersal (שופרסל)
- **Platform:** Direct
- **Feed Portal:** https://prices.shufersal.co.il
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **File naming:** `<Prefix><ChainId>-<StoreId>-<yyyyMMddHHmm>.xml.gz` (ChainId for Shufersal is `7290027600007`)
- **Schema:** Standard government format with extensions
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Largest chain in Israel by revenue; ~400 stores operated under four banners (Shufersal Deal, Sheli, Yesh, Express). Most reliable and structured feed. Good baseline for testing parsers.

### Rami Levy (רמי לוי)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (username `RamiLevi`, empty password)
- **Access:** Public via Cerberus auth flow (see top of file); no password
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format. Uses `ItemNm` instead of `ItemName` in some feeds.
- **Update time:** Typically 01:00-04:00 Israel time
- **Notes:** Known for competitive pricing. 50+ stores nationwide.

### Yochananof (יוחננוף)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Yochananof")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 03:00-06:00 Israel time
- **Notes:** Central Israel focus. Fewer stores means faster full downloads.

### Victory (ויקטורי)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (username `Victory`, empty password)
- **Access:** Public via Cerberus auth flow (see top of file); no password
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Independently owned (Ravid family, publicly traded VCTR.TA). 60+ stores nationwide. Completely separate from Carrefour Israel. Migrated from the (now-defunct) Nibit / matrixcatalog.co.il platform to Cerberus.

### Carrefour Israel (קרפור ישראל, formerly Mega/Yeinot Bitan)
- **Platform:** Direct
- **Feed Portal:** https://prices.carrefour.co.il
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Operates under Carrefour, Mega, and Yeinot Bitan brands (same company, Electra Consumer Products franchise). 100+ stores. Legacy URL `publishprice.mega.co.il` redirects here.

### Osher Ad (אושר עד)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login
- **Access:** Username: `osherad`, no password required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format, minimal extensions
- **Update time:** Typically 01:00-03:00 Israel time
- **Notes:** Discount chain with 20+ large-format stores. Some products may have limited metadata.

### Tiv Taam (טיב טעם)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Tiv Taam")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Includes non-kosher products. Product categories may differ from kosher-only chains.

### Additional Chains on Cerberus
The following smaller chains also publish via `https://url.publishedprices.co.il/login`:
- **Hazi Hinam (חצי חינם)**
- **Keshet Taamim (קשת טעמים)**
- **Fresh Market / Super Dosh (פרש מרקט / סופר דוש)**
- **Dor Alon (דור אלון)**
- **Bareket (ברקת)** -- mainly northern Israel; feed can be flaky
- **Mahsani A'Shuk (מחסני השוק)**
- **Cofix (קופיקס)** -- convenience-store SKU range only
- **Super-Pharm (סופר-פארם)** -- pharmacy chain, drugstore SKUs (toiletries, OTC, baby food), no fresh produce / dairy / meat
- **Good Pharm (גוד פארם)** -- pharmacy chain, same scope as Super-Pharm
- **Mega (מגה)** -- legacy feed; current Mega/Yeinot Bitan stores publish via Carrefour Israel Direct
- Plus ~15 additional smaller chains and convenience stores

The previously-listed "Mahsanei Lahav" / "Mahsanei Hashuk" Nibit endpoints are no longer active. These chains either consolidated under other brands or moved to Cerberus.

## XML Schema Reference

### PricesFull Schema (common fields)

```xml
<Items>
  <Item>
    <ItemCode>7290000000001</ItemCode>
    <ItemType>0</ItemType>
    <ItemName>חלב תנובה 3% שומן 1 ליטר</ItemName>
    <ManufacturerName>תנובה</ManufacturerName>
    <ManufactureCountry>IL</ManufactureCountry>
    <ManufacturerItemDescription>חלב מפוסטר 3%</ManufacturerItemDescription>
    <UnitQty>1</UnitQty>
    <Quantity>1</Quantity>
    <UnitOfMeasure>ליטר</UnitOfMeasure>
    <bIsWeighted>0</bIsWeighted>
    <QtyInPackage>1</QtyInPackage>
    <ItemPrice>6.50</ItemPrice>
    <UnitOfMeasurePrice>6.50</UnitOfMeasurePrice>
    <AllowDiscount>1</AllowDiscount>
    <ItemStatus>1</ItemStatus>
    <PriceUpdateDate>2026-02-26</PriceUpdateDate>
  </Item>
</Items>
```

### Key Fields

| Field | Description | Notes |
|-------|-------------|-------|
| ItemCode | Barcode / product code | Use for cross-chain matching |
| ItemName | Product name (Hebrew) | Naming varies across chains |
| ManufacturerName | Manufacturer | Useful for fuzzy matching |
| ItemPrice | Current price in NIS | VAT included |
| UnitOfMeasurePrice | Price per unit (kg/liter) | For weight/volume comparison |
| bIsWeighted | 0=fixed, 1=sold by weight | Affects price calculation |
| PriceUpdateDate | Last price update date | Check for staleness |

## PromoFull Schema

`PromoFull` files describe active promotions. The main element is `<Promotion>`. Key fields:

| Field | Description | Notes |
|-------|-------------|-------|
| PromotionId | Unique promotion ID within chain | |
| PromotionDescription | Hebrew description shown to shoppers | Free text, e.g., "2 ב-10 ש"ח" |
| RewardType | How the discount applies (see table below) | Integer code |
| MinQty | Minimum quantity to trigger the promo | Often 1 or 2 |
| MaxQty | Maximum quantity at promo price | |
| DiscountedPrice | Effective price when promo applies | Per unit, NIS |
| DiscountRate | Discount percentage | If applicable |
| MinPurchaseAmnt | Minimum basket total to trigger | NIS |
| ClubId | Chain club identifier; 0 = open to all | Non-zero = club-only |
| PromotionStartDate / EndDate | Validity window | yyyy-MM-dd |
| IsWeightedPromo | 1 if promo applies to weighted items | |
| `<PromotionItems>` | Nested list of `<Item>` elements with `ItemCode` and `IsGiftItem` | Which products are included |

### RewardType values

| Code | Meaning |
|------|---------|
| 1 | Flat discounted price (replace `ItemPrice` with `DiscountedPrice` for qualifying purchases) |
| 2 | Fixed price for N units (e.g., "2 ב-10 ש"ח") |
| 3 | Nth-item discount (e.g., "buy 3 pay for 2") |
| 5 | Discount on second purchase |
| 6 | Discount when buying from a category |

**Club-only handling:** when `ClubId != 0`, the promotion applies only to chain club members (Shufersal Sofash = 0001, Rami Levy club, etc.) and should NOT be applied to a generic basket-cost estimate.

## Known Format Variations

- **Field naming:** Some chains (notably Rami Levy on Cerberus) use `ItemNm` instead of `ItemName`, or `ManuName` instead of `ManufacturerName`
- **Encoding:** Government spec mandates UTF-8, and Shufersal/Rami Levy comply. Older Mega/Yeinot Bitan archives sometimes use Windows-1255; modern Carrefour Direct feeds are UTF-8
- **Weighted items:** When `bIsWeighted=1`, `ItemPrice` is the price per kg, NOT the price of the package; `Quantity` may be empty or fractional; `UnitOfMeasurePrice` equals `ItemPrice`. Parsers must apply per-kg math for weighted items, otherwise cross-chain comparisons silently misrank
- **Barcode formats:** Israeli barcodes typically start with 729. Store-brand items use internal codes starting with `2` and cannot be cross-matched between chains
- **Promotion overlap:** A product may appear in both `PriceFull` (regular price) and `PromoFull` (sale price). Always check the promotions feed for the effective price, and respect `ClubId`/`MinQty`/`MinPurchaseAmnt`
- **Platform differences:** Cerberus wraps file access in an authenticated session (see "Cerberus Authentication Flow" above). The underlying XML schema is the same government standard across Shufersal Direct, Carrefour Direct, and Cerberus, but the download method differs per platform
- **Stale-file detection:** CDNs occasionally serve yesterday's file. Robust pipelines check BOTH the filename timestamp AND the inner `<PriceUpdateDate>` against `now() - 36h`; if both are older, force a fresh download
- **File sizes:** A typical Shufersal `PriceFull` is ~1-3 MB gzipped, 30-100 MB uncompressed per large store. A full daily snapshot across all chains and stores totals ~5-10 GB uncompressed
