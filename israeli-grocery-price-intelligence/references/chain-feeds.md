# Israeli Supermarket Chain Price Feeds

## Overview

Under the Promotion of Competition in the Food and Pharma Sector Law (חוק קידום התחרות בענפי המזון והפארם, 2014, in force since 2015), supermarket AND pharmacy chains with 3 or more stores must publish product prices as machine-readable XML files. The Ministry of Economy's Competition Authority publishes the file spec ("פרסום מחירים, מפרט קבצים") at https://www.gov.il/he/pages/cpfta_prices_regulations. **Encoding is not reliably UTF-8 in practice**: price files generally are, but a live Carrefour `Stores` file was UTF-16 little-endian with a BOM and no XML declaration. Sniff the BOM and fall back across encodings rather than assuming.

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

**File naming.** Two shapes are in use and they are **not** cleanly split by platform. A single
Cerberus chain's listing carries both. Verified on a live Rami Levy listing, 2026-08-27:

| Shape | Pattern | Real example | Where seen |
|-------|---------|--------------|------------|
| 3-segment | `<Prefix><ChainId>-<StoreId>-<yyyyMMddHHmm>.gz` | `PriceFull7290058140886-039-202607150513.gz` | 44 of Rami Levy's `PriceFull` files, the older ones |
| 5-segment | `<Prefix><ChainId>-<SubChainId>-<StoreId>-<yyyyMMdd>-<HHmmss>.gz` | `PriceFull7290058140886-001-001-20260827-001001.gz` | 93 of Rami Levy's `PriceFull` files (the newer ones), and all Shufersal / Carrefour files |
| 4-segment | `Stores<ChainId>-<StoreId>-<yyyyMMdd>-<HHmmss>.xml` | `Stores7290058140886-000-20260826-050500.xml` | `Stores` files, frequently plain `.xml` |

Practical consequence: **do not write a filename regex that assumes a segment count.** Match the
prefix case-insensitively (`price`, `Price`, `pricefull` and `PriceFull` all appear in one
listing), then parse the timestamp from the right-hand end. Neither price shape ends in `.xml.gz`;
the payload is gzipped XML but the filename ends `.gz`.

- `ChainId` is the 13-digit Israeli EAN-style chain identifier (starts with `729...`). Shufersal is `7290027600007`, Rami Levy `7290058140886`, Carrefour Israel `7290055700007`.

## Feed Platforms

Not every chain runs its own server; most publish through a shared platform. There are more than three platforms. The rows below were confirmed by live probe on 2026-08-27.

| Platform | URL | Chains confirmed | Access |
|----------|-----|------------------|--------|
| Shufersal Direct | https://prices.shufersal.co.il | Shufersal | Listing page; downloads are expiring signed Azure Blob URLs |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (Carrefour + Mega + Yeinot Bitan banners) | File list inlined in page HTML; download at `/<yyyyMMdd>/<filename>` |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy (`RamiLevi`), Yochananof (`yohananof`), Tiv Taam (`TivTaam`), Osher Ad (`osherad`), Dor Alon (`doralon`), Keshet Taamim (`Keshet`), Fresh Market / Super Dosh (`freshmarket`), Cofix (`SuperCofixApp`), plus Polizer, Salach Dabach, Stop Market, Super Yuda, Yellow | Session login + CSRF, listing is a POST |
| Super-Pharm own portal | http://prices.super-pharm.co.il | Super-Pharm | Public listing page |
| Bina Projects | `https://<chain>.binaprojects.com/Main.aspx` (the bare host 403s; use the Main.aspx page, not the bare host) | Good Pharm, King Store, Bareket, Shuk Ahir, Zol VeBegadol, Super Sapir, City Market branches | Public listing page per chain subdomain |
| Chain's own site | https://shop.hazi-hinam.co.il/Prices | Hazi Hinam | Public file table |
| Laibcatalog (Nibit successor) | `laibcatalog.co.il` | Victory, Mahsani A'Shuk, Het Cohen | Unconfirmed, see note below |

**Cerberus login failures that are NOT outages.** `Victory`, `SuperPharm`, `GoodPharm`, `Bareket`
and `Mega` all fail Cerberus login (200 + re-rendered form rather than 302) because they do not
publish there. `HaziHinam` authenticates but returns zero files, while its own site serves a full
table. Route by the table above, not by assumption.

`matrixcatalog.co.il` no longer resolves (NXDOMAIN as of 2026-08-27), so requests fail at DNS
rather than timing out. Its successor `laibcatalog.co.il` resolves to an IP but refused TCP
connections from our probe on 2026-08-27; we could not establish whether it is down, geo-fenced,
or simply unreachable from our network. Verify it directly before depending on it, and do not
record Victory as "not publishing" on the strength of that failure alone.

## Cerberus Authentication Flow

Cerberus is NOT a static file server. It is a stateful web app (CerberusFTPServer) that enforces CSRF protection and session cookies. A naive `curl https://url.publishedprices.co.il/file/d/<filename>.gz` returns the login HTML, not the file. The flow:

**Step 1, fetch the login page and capture both the CSRF token and the session cookie:**
```bash
curl -sS -c cerberus_cookies.txt -A "Mozilla/5.0" \
  "https://url.publishedprices.co.il/login" -o login.html
csrftoken=$(grep -oE 'name="csrftoken" content="[^"]+"' login.html | sed 's/.*content="\([^"]*\)".*/\1/')
```

The csrftoken appears in a `<meta name="csrftoken" content="...">` tag in the response HTML, NOT as a hidden form input.

**Step 2, POST credentials with the csrftoken and the saved cookie jar:**
```bash
curl -sS -b cerberus_cookies.txt -c cerberus_cookies.txt -A "Mozilla/5.0" \
  -X POST "https://url.publishedprices.co.il/login/user" \
  -d "username=<chain-code>&password=<password-or-empty>&csrftoken=$csrftoken" \
  -o /dev/null
```

For public chains (`RamiLevi`, `yohananof`, `Carrefour`, `osherad`, `TivTaam`, etc.) the password is empty.

**Step 3, refresh the csrftoken from the post-login page.** The token minted on `/login` is not
accepted by the listing endpoint:
```bash
curl -sS -b cerberus_cookies.txt -c cerberus_cookies.txt \
  "https://url.publishedprices.co.il/file" -o file.html
csrftoken=$(grep -oE 'name="csrftoken" content="[^"]+"' file.html | sed 's/.*content="\([^"]*\)".*/\1/')
```

**Step 4, POST the directory listing.** This endpoint is **POST-only**:
```bash
curl -sS -b cerberus_cookies.txt -X POST \
  "https://url.publishedprices.co.il/file/json/dir" \
  -d "sEcho=1&iDisplayStart=0&iDisplayLength=1000&cd=/&csrftoken=$csrftoken"
```

A **GET** on the same path returns HTTP 200 with
`{"aaData":[],"error":"Invalid request method used for this operation."}`, and a POST carrying a
stale token returns `{"aaData":[],"error":"CSRF security check failed"}`. Both look like an empty
file list unless you read the `error` key. Always check it before concluding a chain publishes
nothing.

**Step 5, download a file (a plain GET, with the session cookie):**
```bash
curl -sS -b cerberus_cookies.txt \
  "https://url.publishedprices.co.il/file/d/PriceFull7290058140886-708-202608270010.gz" -o PriceFull.gz
```

**Verifying a chain code.** A valid code answers the Step 2 POST with **302**; an invalid one
answers **200** and re-renders the login form. Use that to tell "wrong chain code" from
"platform down".

**Access notes:**
- The stock `curl` User-Agent was NOT blocked in our 2026-08-27 probe: login, directory listing and file download all succeeded with default headers. Earlier guidance in this file to send a "realistic" User-Agent was unverified and has been removed.
- An unauthenticated GET of `/file/d/<filename>` answers **HTTP 302** with a short redirect stub, not the file and not a 200 login page. Require a 2xx status AND a gzip payload before treating a response as data.
- Sessions are cookie-based and expire after a period of inactivity; re-run the login flow when a request starts returning the login page again.
- This is a public portal serving data that the law requires chains to publish, and the login for these chain codes takes an empty password. We have not located published terms of use governing automated access to it, so we make no claim that any particular request volume is authorised. Keep request rates modest, and if the platform signals that it is refusing automated access, stop rather than working around it.
- The `il-supermarket-scraper` PyPI package implements this flow and is the practical route for bulk collection.

## Per-Chain Feed Access

### Shufersal (שופרסל)
- **Platform:** Direct
- **Feed Portal:** https://prices.shufersal.co.il
- **Access:** Listing page is public; the download links it emits are signed and expire after about half an hour (see below)
- **Format:** Gzipped XML, filename ends `.gz`
- **File naming:** Shufersal dialect, `<Prefix>7290027600007-<SubChainId>-<StoreId>-<yyyyMMdd>-<HHmmss>.gz`
- **Schema:** Shufersal dialect (`ChainID`, `ManufactureName`, `PriceUpdateTime`). Verified 2026-08-27 against a live `PriceFull`
- **Update time:** Typically 02:00-05:00 Israel time
- **Listing:** `GET https://prices.shufersal.co.il/FileObject/UpdateCategory?catID=<N>&storeId=0` where `catID` is 1 Price, 2 PriceFull, 3 Promo, 4 PromoFull, 5 Stores. The response HTML contains `pricesprodpublic.blob.core.windows.net` links.
- **Downloads expire.** Those links carry an Azure SAS `se=` expiry about half an hour out, pinned to a clock boundary rather than measured from your request, so the usable window can be much shorter. Validate the `se=` value before use, re-list on a 403, and never cache, bookmark or hard-code one.
- **Notes:** The largest chain, operating several banners (Shufersal Deal, Sheli, Yesh, Express) with a store file per branch. Uses the Shufersal dialect (`ManufactureName`, `PriceUpdateTime`). For a current branch count, read the `Stores` feed rather than trusting a number written here.

### Rami Levy (רמי לוי)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (username `RamiLevi`, empty password)
- **Access:** Public via Cerberus auth flow (see top of file); no password
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** Cerberus dialect (`ItemName`, `ManufacturerName`, `PriceUpdateDate`). Verified 2026-08-27 against a live `PriceFull`; it does NOT use `ItemNm`.
- **Update time:** Typically 01:00-04:00 Israel time
- **Notes:** Known for competitive pricing. For a current branch count, read its `Stores` feed.

### Yochananof (יוחננוף)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Yochananof")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** detect it from the file (see the XML Schema Reference); do not assume from the chain name
- **Update time:** Typically 03:00-06:00 Israel time
- **Notes:** Central Israel focus. Fewer stores means faster full downloads.

### Victory (ויקטורי)
- **Platform:** Laibcatalog (Nibit successor). **NOT Cerberus** -- a Cerberus login as `Victory` fails.
- **Feed Portal:** `laibcatalog.co.il` (unreachable from our 2026-08-27 probe; verify before use)
- **Chain IDs:** `7290696200003`, `7290058103393`
- **Access:** Unconfirmed; the community `il-supermarket-scraper` package targets this host
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** detect it from the file (see the XML Schema Reference); do not assume from the chain name
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** A separate company from Carrefour Israel, not a Carrefour banner. Migrated off the defunct Nibit / matrixcatalog.co.il platform; the community scraper targets `laibcatalog.co.il` as its successor, which we could not reach to confirm. It is **not** on Cerberus.

### Carrefour Israel (קרפור ישראל, formerly Mega/Yeinot Bitan)
- **Platform:** Direct
- **Feed Portal:** https://prices.carrefour.co.il
- **Access:** Public, no authentication required
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** detect it from the file (see the XML Schema Reference); do not assume from the chain name
- **Update time:** Typically 02:00-05:00 Israel time
- **Listing:** the portal HTML inlines a JavaScript `files` array (name, size, modified) plus a `path` of `yyyyMMdd`. Download at `https://prices.carrefour.co.il/<path>/<filename>`; a wrong filename returns a real 404.
- **Chain ID:** `7290055700007`. Uses the Shufersal dialect (verified 2026-08-27 against a live `PriceFull` and `Stores` file).
- **Notes:** One publisher covering the Carrefour, Mega and Yeinot Bitan banners. Its own live `Stores` file lists Carrefour-branded stores alongside `בעיר` and `יינות ביתן` branded ones, so read that file rather than assuming every store is Carrefour-branded. The legacy host `publishprice.mega.co.il` now 301-redirects to the consumer shop `online2.carrefour.co.il`, NOT to this price portal, so do not rely on it for feed access; use `https://prices.carrefour.co.il` directly.

### Osher Ad (אושר עד)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login
- **Access:** Username: `osherad`, no password required
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** detect it from the file (see the XML Schema Reference); do not assume from the chain name
- **Update time:** Typically 01:00-03:00 Israel time
- **Notes:** Discount chain, large-format stores. Some products may have limited metadata.

### Tiv Taam (טיב טעם)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Tiv Taam")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML, filename ends `.gz`
- **Schema:** detect it from the file (see the XML Schema Reference); do not assume from the chain name
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Carries non-kosher products, so its product categories differ from kosher-only chains.

### Additional Chains on Cerberus
Confirmed by successful login on 2026-08-27 (a valid chain code answers 302):
- **Keshet Taamim (קשת טעמים)** -- `Keshet`
- **Fresh Market / Super Dosh (פרש מרקט / סופר דוש)** -- `freshmarket`
- **Dor Alon (דור אלון)** -- `doralon`
- **Cofix (קופיקס)** -- `SuperCofixApp`, convenience-store SKU range only
- **Hazi Hinam (חצי חינם)** -- `HaziHinam` authenticates but its listing is EMPTY; use its own site instead (see the table below)
- **Polizer (פוליצר)**, **Salach Dabach (סאלח דבאח)**, **Stop Market (סטופ מרקט)**, **Super Yuda (שופ יודה)**, **Yellow (יילו)** -- confirmed Cerberus chain codes in the community scraper

Chains that are **not** on Cerberus, with their real homes:

| Chain | Real platform |
|-------|---------------|
| Super-Pharm (סופר-פארם) | Own portal, http://prices.super-pharm.co.il. Pharmacy SKUs only (toiletries, OTC, baby food), no fresh produce / dairy / meat |
| Good Pharm (גוד פארם) | Bina Projects, https://goodpharm.binaprojects.com/Main.aspx (the bare host 403s). Same drugstore scope |
| Bareket (ברקת) | Bina Projects |
| Hazi Hinam (חצי חינם) | Own site, https://shop.hazi-hinam.co.il/Prices (its Cerberus account lists zero files) |
| Mega (מגה) | Current Mega / Yeinot Bitan stores publish via Carrefour Israel Direct. The standalone `prices.mega.co.il` host answers 403 behind Cloudflare |
| Mahsani A'Shuk (מחסני השוק) | Laibcatalog, alongside Victory |

## XML Schema Reference

**There are two dialects.** Every field name below was read off a live file downloaded on
2026-08-27. The dialect is not predictable from the chain name (chains migrate platforms), so
detect it from the document: the presence of `ManufactureName`, `PriceUpdateTime` or
`LastSaleDateTime` identifies the Shufersal dialect.

### Root element

| | Cerberus dialect | Shufersal / Carrefour dialect |
|---|---|---|
| Root children | `XmlDocVersion`, `ChainId`, `SubChainId`, `StoreId`, `BikoretNo`, `DllVerNo`, `Items` | `ChainID`, `SubChainID`, `StoreID`, `BikoretNo`, `Items` |

Note the capitalisation difference (`ChainId` vs `ChainID`); it is not cosmetic, an XPath written
for one fails silently on the other.

### PriceFull item fields

| Purpose | Cerberus dialect | Shufersal / Carrefour dialect |
|---------|------------------|-------------------------------|
| Product name | `ItemName` | `ItemName` |
| Manufacturer | `ManufacturerName` | **`ManufactureName`** |
| Manufacturer description | `ManufacturerItemDescription` | **`ManufactureItemDescription`** |
| Price update stamp | `PriceUpdateDate` (e.g. `2026-01-05 15:49:18`) | **`PriceUpdateTime`** (e.g. `2026-05-14T08:59:51.000`) |
| Barcode | `ItemCode` | `ItemCode` |
| Price | `ItemPrice` | `ItemPrice` |
| Unit price | `UnitOfMeasurePrice` | `UnitOfMeasurePrice` |
| Weighted flag | `bIsWeighted` | `bIsWeighted` |
| Cerberus-only | `ItemId` | -- |
| Shufersal-only | -- | `LastSaleDateTime` |

**`ItemNm` does not exist.** Earlier revisions of this file claimed Rami Levy uses `ItemNm`
instead of `ItemName`. It does not: a live Rami Levy `PriceFull` uses `ItemName` for all 2,225
items. Mapping to `ItemNm` yields a blank name for every single product.

Common fields present in both: `ItemType`, `ManufactureCountry`, `UnitQty`, `Quantity`,
`UnitOfMeasure`, `QtyInPackage`, `AllowDiscount`, `ItemStatus`.

### PromoFull

The two dialects differ structurally, not just in spelling.

**Cerberus dialect** -- discount terms sit on the `<Promotion>` element:

| Field | Notes |
|-------|-------|
| `PromotionId`, `PromotionDescription` | |
| `RewardType` | Observed values 1, 2, 3, 7, 9 |
| `MinQty`, `DiscountedPrice`, `DiscountedPricePerMida`, `DiscountRate` | `MinQty` present on 229 of 232 sampled promotions |
| `MinNoOfItemOfered` | One `f` |
| `Clubs/ClubId` | **Nested**, bare integer. `0` = open to all |
| `PromotionItems/Item` | `ItemCode`, `ItemType`, `IsGiftItem` |
| `PromotionStartDate` / `EndDate` / `StartHour` / `EndHour`, `AllowMultipleDiscounts`, `IsWeightedPromo`, `AdditionalRestrictions`, `WeightUnit` | |

`MaxQty` and `MinPurchaseAmnt` did NOT appear on any of the 232 sampled Cerberus promotions.
Treat them as optional and absent rather than guaranteed.

**Shufersal / Carrefour dialect** -- the `<Promotion>` element carries only the envelope, and the
discount terms sit two levels down:

| Level | Fields |
|-------|--------|
| `<Promotion>` | `PromotionID`, `PromotionDescription`, `PromotionUpdateTime`, `PromotionStartDateTime`, `PromotionEndDateTime`, `PromotionStartHour`, `PromotionEndHour`, `PromotionDays`, `RedemptionLimit`, `MinNoOfItemOffered` (two `f`s), `ClubID`, `IsGiftItem`, `AdditionalIsCoupon`, `AdditionalRestrictions`, `Remarks`, `Groups` |
| `Groups/Group` | `GroupID`, `MinPurchaseAmount` (not `MinPurchaseAmnt`), `DiscountType`, `PromotionItems` |
| `Groups/Group/PromotionItems/PromotionItem` | `ItemCode`, `ItemType`, **`RewardType`**, **`MinQty`**, **`MaxQty`**, **`DiscountRate`** |

`RewardType` is absent from the `<Promotion>` element in this dialect: across 5,245 sampled
Shufersal promotions, zero carried it at that level. A parser looking for `Promotion/RewardType`
finds nothing and reports no usable promotions.

### RewardType values

Codes 1, 2, 3, 7 and 9 all occur on live Cerberus feeds. **We could not find an authoritative
published mapping for any of them.** The commonly-used readings below are conventions, not
specification, so confirm each against the promotion's own `PromotionDescription` before applying
it, and never auto-apply a code you have not confirmed.

| Code | Commonly read as | Status |
|------|------------------|--------|
| 1 | Flat discounted price | Unsourced convention |
| 2 | Fixed price for N units (e.g., "2 ב-10 ש"ח") | Unsourced convention |
| 3 | Nth-item discount (e.g., "buy 3 pay for 2") | Unsourced convention |
| 7, 9 | Unknown | Observed on live feeds, no reading we could verify |

Codes 5 and 6 were listed in earlier revisions of this file but did not appear on any sampled feed
and we could not source them.

### Club handling (dialect-specific)

| Dialect | Field | Value shape | Open-to-all test |
|---------|-------|-------------|------------------|
| Cerberus | `Clubs/ClubId` (nested) | Integer, e.g. `0`, `1` | `int(value) == 0` |
| Shufersal / Carrefour | `ClubID` (flat) | **String beginning with the code**, e.g. `0 - כלל הלקוחות` | parse the integer before ` - `, then compare |

Applying the integer test directly to the Shufersal string is never equal to `0`, so every
promotion is misclassified as club-only and silently dropped from a guest basket.

## Known Format Variations

- **Field naming:** the real split is the two dialects documented above (`ManufacturerName`/`PriceUpdateDate` on Cerberus vs `ManufactureName`/`PriceUpdateTime` on Shufersal/Carrefour). Detect it from the file, never from the chain name
- **Encoding:** price files are generally UTF-8, but do not rely on it. A live Carrefour `Stores` file (2026-08-27) was UTF-16LE with a BOM and no XML declaration, which breaks any parser that tries UTF-8 then a Hebrew 8-bit codepage. Older archives sometimes use Windows-1255. Detect by BOM first, then try UTF-8, UTF-16 and Windows-1255 in turn
- **Weighted items:** When `bIsWeighted=1`, `ItemPrice` is the price per kg, NOT the price of the package; `Quantity` may be empty or fractional; `UnitOfMeasurePrice` equals `ItemPrice`. Parsers must apply per-kg math for weighted items, otherwise cross-chain comparisons silently misrank
- **Barcode formats:** Israeli barcodes typically start with 729. Store-brand items use internal codes starting with `2` and cannot be cross-matched between chains
- **Promotion overlap:** A product may appear in both `PriceFull` (regular price) and `PromoFull` (sale price). Always check the promotions feed for the effective price, and respect the club id, `MinQty`, and any minimum-purchase field, reading them at the level their dialect puts them
- **Platform differences:** Cerberus wraps file access in an authenticated session (see "Cerberus Authentication Flow" above). The underlying XML schema is the same government standard across Shufersal Direct, Carrefour Direct, and Cerberus, but the download method differs per platform
- **Stale-file detection:** CDNs occasionally serve yesterday's file. Robust pipelines check BOTH the filename timestamp AND the inner `<PriceUpdateDate>` against `now() - 36h`; if both are older, force a fresh download
- **File sizes:** A typical Shufersal `PriceFull` is ~1-3 MB gzipped, 30-100 MB uncompressed per large store. A full daily snapshot across all chains and stores totals ~5-10 GB uncompressed
