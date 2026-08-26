# Domain coverage checklist: Israeli grocery price intelligence

Scope: accessing, parsing and comparing the price files Israeli food and pharma chains are
required to publish under the Promotion of Competition in the Food and Pharma Sector Law.

Last re-verified by live probe: 2026-08-27.

## Must cover (core)

| Item | Why it is core | Status |
|---|---|---|
| The statutory basis and who it binds (chains with 3+ stores, food AND pharma) | Determines which chains have a feed at all | Covered, Step 1 |
| The six file types (Price, PriceFull, Promo, PromoFull, Stores, StoresFull) | The whole data model | Covered, Step 1 + reference |
| Per-platform routing for every named chain | Routing a chain to the wrong platform is the top cause of a false "this chain publishes nothing" | Covered, platform table (verified by probe) |
| Cerberus authentication flow including the POST-only directory listing and the post-login csrftoken | A GET returns HTTP 200 with an empty list, which reads as "no data" | Covered, Step 1 + reference |
| Shufersal expiring signed-URL download mechanics | Links expire in minutes; a cached URL always fails | Covered, Step 1 + reference |
| Carrefour inline file list and date-path download | Otherwise unreachable | Covered, Step 1 + reference |
| The two XML dialects and their field-name differences | A parser written to one silently returns blank fields on the other | Covered, reference schema section + script auto-detection |
| Promotion structure per dialect, including where RewardType lives | Shufersal nests it under Groups/Group/PromotionItems | Covered, Step 4 + reference |
| Club-only promotion handling per dialect, including the Shufersal string form | Applying the integer test to the string drops every promotion | Covered, Step 4 + Gotchas |
| Weighted-item per-kg math (bIsWeighted) | Cross-chain comparisons silently misrank without it | Covered, Step 2 |
| Barcode matching and its limits (729 prefix, store-brand internal codes) | Cross-chain matching is the core operation | Covered, Step 3 |
| VAT is included in published prices | Agents routinely add or strip it | Covered, Gotchas |
| Consumer comparison apps for non-technical users | Most users do not need a pipeline | Covered, Instructions opening |

## Should cover (advanced)

| Item | Status |
|---|---|
| Multi-store basket optimisation | Covered, Step 4 |
| Price-trend tracking and CPI comparison | Covered, Step 5 |
| Restaurant ingredient costing | Covered, Step 6 |
| Stale-file detection (filename timestamp vs inner update stamp) | Covered, reference |
| Chain-banner granularity (Victory banners, Shufersal banners) pricing differently | Covered, Step 2 |

## Out of scope (explicit)

| Item | Rationale | Re-litigated 2026-08-27 |
|---|---|---|
| Non-food retail price comparison | The statute covers food and pharma chains only; no feed exists for general retail | Still out of scope. A user could ask, and the honest answer is "no published feed exists", which the description already states |
| Restaurant operations (licensing, staffing, kashrut) | Handled by `israeli-restaurant-ops`; this skill only supplies ingredient costs | Still out of scope, and the two skills make no contradicting claims (checked) |
| Building or hosting a live price-comparison service | Product work, not a skill workflow | Still out of scope |
| Circumventing any platform's access controls | We document the published access flow only. Where a platform signals it is refusing automated access, the skill says stop rather than describing a workaround | Still out of scope, deliberately |
| Exact per-store prices as static facts | Prices change daily; the skill teaches retrieval, it must never hard-code a price | Still out of scope. The Examples section is explicitly labelled illustrative |

## Authoritative sources

- Statute text: https://he.wikisource.org/wiki/חוק_קידום_התחרות_בענף_המזון
- Ministry of Economy approved comparison apps: https://www.gov.il/he/pages/cpfta_apps
- Community reference implementation (also the best cross-check of which platform each chain currently uses): https://github.com/OpenIsraeliSupermarkets
- Live platform endpoints: see `chain-feeds.md`
