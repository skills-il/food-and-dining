# Domain coverage checklist: Israeli food business compliance

Scope: business licensing, kashrut certification, Ministry of Health requirements,
Hebrew food labelling including front-of-package warning labels, food import,
health-inspection preparation, and VAT for food businesses.
Audience: Israeli food business owners, mostly non-technical.

Figures are deliberately kept out of this file. The authoritative values live in
`evidence.json` and in SKILL.md; duplicating them here creates a third place to
drift.

## Must cover (core)

- Resolving the licensing item (פריט) in the Schedule to Tzav Rishuy Asakim before anything
  else, since the item drives approving authorities, route, validity and fee count.
- Group 4 (מזון) is where food businesses sit, and the Tzav HaChacham search engine is the
  way a user finds their own item rather than guessing it.
- The licensing routes: ordinary route, licence on the basis of a declaration, heter mezoraz A,
  heter mezoraz B, and the fact that the permitted route is set per item.
- The uniform specification (מפרט אחיד): what it is, that it binds the local authority for the
  matters it covers, and that many food items still have none.
- The licensing fee: that it is a national tariff, charged per licensing item, and re-indexed
  twice a year, so it must be re-checked rather than quoted from memory.
- Licence validity: that it is set per item and varies widely, and that no blanket period may
  be stated.
- Ministry of Health sanitary conditions for the business type (bt'ei ochel versus food
  production have separate regulation sets).
- Health-inspection preparation, the defect notice as a formal instrument, and the existence of suspension and closure powers.
- Kashrut is voluntary; licensing is not, and a kashrut certificate never substitutes for a
  health or licensing approval.
- The current kashrut regime after the July 2026 amendment: only the Rabbanut may grant
  kashrut, a city rabbi may not certify outside his city without Chief Rabbinate Council
  approval, and the private-corporation route is closed.
- That the 2021 reform was largely never implemented before it was repealed, so a user who
  believed they were waiting for it never had that option.
- The mashgiach employment rule, since it changes the supervision arrangement and its cost
  for every certified business.
- Mandatory labelling fields for pre-packed food, in Hebrew.
- The allergen list, including the Israel-specific broad bean entry and the fact that it is
  marked differently from the adopted European list.
- The front-of-package red label: which nutrients, that solids and liquids have different
  thresholds, that each exceeded nutrient gets its own label, and the main exclusions.
- The voluntary green label and that it cannot coexist with a red label.
- Which regime a given labelling instruction belongs to: the rules in force today, or the
  adopted European rules whose transition period is still running. Stating a future rule as
  current, or the reverse, is the characteristic failure in this domain.
- Food import: registration, the route split, and that Hebrew labelling compliance is the
  importer's duty.
- VAT: the standard rate, the zero-rated fresh-produce case and its limits, and that
  restaurant service is fully taxed.

## Known gaps, scheduled (NOT yet covered)

These are genuine Must/Should items that this cycle did not deliver. They are listed here
so no later cycle mistakes the checklist for a statement of coverage. Each is also carried
in `optimization-log.json` lessons[].

- Accessibility approval for a public-facing food business, which is a live condition on
  the licence.
- Recall and suspected-food-poisoning reporting duties and their route. Highest priority
  for the next cycle: it is the only scenario here with same-day public-health stakes.
- The approving authorities per food item, the sequence between them, the preliminary
  advisory step available before a full application, and a realistic timeline.
- Alcohol licensing conditions and the smoking-restriction duties on the occupier.
- The osek patur turnover ceiling, so the smallest operators are not told to charge VAT
  they may not owe.
- The proposed move to self-supervision with a hygiene trustee, to be stated expressly as
  a proposal and not as law.

## Should cover (advanced)

- Ordering: planning and permitted-use conformity precede licensing.
- Change of ownership does not transfer a licence.
- Operating without a licence: closure order and personal exposure.
- Pest control from a company registered with the Ministry of Environmental Protection.
- Fire-safety approvals and the accessibility layer.
- Recall and food-poisoning reporting duties.
- The proposed move toward self-supervision with a hygiene trustee, flagged as a proposal
  and not as law.

## Out of scope (explicit)

- Halachic rulings on whether a food, ingredient or process is kosher. Reserved to a
  qualified rabbi; the skill explains the certification process only. Reviewed 2026-08-24,
  still out of scope.
- Acting as a licensing consultant or filing on the user's behalf. Reviewed 2026-08-24,
  still out of scope: an ordinary user does ask for this, and the skill answers by
  explaining the route and naming the consultant option rather than by filing.
- Per-municipality by-law text for every local authority. Reviewed 2026-08-24: a user does
  plausibly ask, and the skill answers by naming the layer and telling them to pull their
  own authority's requirement sheet, which is the only capturable answer.
- Customs brokerage and clearance mechanics. Reviewed 2026-08-24, still out of scope.
- Consumer nutrition and dietary advice. Reviewed 2026-08-24, still out of scope.
- Enumerating every group 4 item number. Reviewed 2026-08-24: deliberately out of scope
  because the Schedule's item titles could not be read from an authoritative full text this
  cycle, and inventing them would be worse than routing the user to the official search
  engine. Revisit when the Schedule text is reachable.
- Restaurant daily operations, handled by israeli-restaurant-ops.

## Authoritative sources

- Ministry of Health, food labelling and nutritional marking hub
- Ministry of Health, allergen marking guide for the adopted European regulation
- Ministry of Interior, uniform specifications site and the Tzav HaChacham item search
- Ministry of Interior, business licensing fee tariff circulars
- Chief Rabbinate of Israel department page
- Knesset legislation register for the Prohibition of Kashrut Fraud Law and its amendments
- Israel Tax Authority for VAT
