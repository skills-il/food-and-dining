# Changelog

## 1.6.0 - 2026-08-27

Full live re-probe of every documented feed endpoint. Corrections throughout after downloading and
parsing real files from every platform.

Platform routing
- The "three platforms" model was wrong. Super-Pharm publishes on its own portal, Good Pharm via
  Bina Projects, Hazi Hinam on its own site, and Victory / Mahsani A'Shuk on the Nibit successor
  `laibcatalog.co.il` (which we could not reach to confirm). Cerberus logins for Victory,
  Super-Pharm, Good Pharm, Bareket and Mega all fail.
- `matrixcatalog.co.il` no longer resolves at all (NXDOMAIN), rather than timing out.
- Added the Cerberus chain codes confirmed by successful login, including Cofix as `SuperCofixApp`.

Cerberus access
- The directory listing is POST-only. A GET returns HTTP 200 with an empty list and an `error` key,
  which reads as "this chain publishes nothing". Documented the working flow, including the fresh
  csrftoken that must be read from `/file` after login.
- An unauthenticated file request answers 302, not a 200 login page.
- Removed unverified User-Agent guidance: the stock `curl` UA was not blocked.

Schema
- Documented the two XML dialects. Shufersal and Carrefour use `ChainID` / `ManufactureName` /
  `PriceUpdateTime`; Cerberus chains use `ChainId` / `ManufacturerName` / `PriceUpdateDate`.
- `ItemNm` does not exist; Rami Levy uses `ItemName` for all items.
- Club id is a nested integer on Cerberus but a flat string like `0 - כלל הלקוחות` on Shufersal, so
  the old integer test silently discarded every Shufersal promotion.
- `RewardType` and its siblings sit on `Promotion` in one dialect and on `PromotionItem` inside
  `Groups/Group` in the other.
- Filename shape is not a platform property: one chain's listing carries both the 3-segment and
  5-segment forms, so segment-count regexes break.

Script (`scripts/parse_price_xml.py`)
- Field mappings are now auto-detected from the document instead of trusted from `--chain`. Every
  chain profile was previously broken: `rami-levy` blanked all 2,225 product names, and the
  Shufersal and default profiles blanked manufacturer and update date on all rows.
- Added PromoFull parsing for both dialects, including club-id parsing and the nested reward fields.
- Emits chain, sub-chain and store identity, without which per-store comparison and dedup are
  impossible.
- Detects gzip by magic bytes and handles UTF-16 with a BOM, so a redirect stub or an expired signed
  URL reports the real cause instead of crashing.
- `price_per_kg` is only asserted when the unit is recognisably kilograms.

Content
- Added delta-versus-snapshot reconciliation and `ItemStatus` handling.
- Added the per-store fan-out, promotion validity filtering, and a note that price-controlled
  staples show little cross-chain spread.
- Widened `allowed-tools`, which previously granted only python and WebFetch and so could not
  execute the documented Cerberus flow.

## 1.5.1 - 2026-08-11

Replaced Wikipedia citations behind a statutory and a tax-rate claim with primary sources: the statute text on Wikisource and ITA Interpretation Directive 01/2025.

