---
name: israeli-food-business-compliance
description: Guide Israeli food business regulatory compliance, including business licensing, kashrut certification, health ministry requirements, food labeling (with red/green front-of-package labels), and 18% VAT rules. Use when user asks about "food business license Israel", "Misrad HaBriut requirements", "kashrut certification process", "food labeling Hebrew", "restaurant permit Israel", "food import regulations", "red label sugar salt fat", or "רישיון עסק מזון". Covers Ministry of Health licensing by business type, Rabbanut kashrut application process, certification renewal tracking, Hebrew food label generation, front-of-package red/green warning labels, and health inspection preparation. Do NOT use for restaurant daily operations (use israeli-restaurant-ops) or general business compliance.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for certification renewal tracking and scheduled compliance alerts.
---


# Israeli Food Business Compliance

## Instructions

### Step 1: Determine Ministry of Health Licensing Requirements
Israeli food businesses require a business license (rishyon esek) under the Business Licensing Law. Requirements vary by business type:

| Business Type | Hebrew | Key Requirements |
|---------------|--------|-----------------|
| Restaurant / Cafe | מסעדה / בית קפה | Kitchen layout approval, ventilation, handwashing stations, pest control |
| Food production / Factory | מפעל מזון | GMP compliance, lab testing, production facility approval |
| Food truck / Stand | דוכן / רכב מזון | Mobile food permit, water supply certification, waste disposal plan |
| Bakery | מאפייה | Oven safety certification, flour storage compliance |
| Catering | קייטרינג | Transport temperature compliance, event-specific permits |
| Market stall | דוכן שוק | Municipal market permit, cold storage for perishables |

For each type: identify required documents, inspection criteria, and renewal schedule. See `references/health-ministry-requirements.md` for detailed requirements per business type.

**Resolve the licensing item (פריט) before anything else.** Israeli business licensing keys off a numbered item in the Schedule to Tzav Rishuy Asakim (Asakim Te'unei Rishuy), not off the informal business name. The item determines which authorities must approve, which licensing route applies, how long the licence lasts, and how many fees are due. Food businesses sit in Group 4 (מזון). Do not guess the item number: send the user to the "Tzav HaChacham" search engine on the Ministry of Interior's uniform-specification site (see Reference Links), which searches the Schedule directly.

**Licensing routes.** Beyond the ordinary route, the licensing reform introduced shortened differential routes: rishuy al yesod tatzhir (licence on the basis of a declaration), heter mezoraz A, and heter mezoraz B. Which route a business may use is set per item in the Schedule, so resolve the item first and read its route from there rather than assuming.

**Uniform specification (מפרט אחיד).** Where a uniform specification has been published for an item, it is the binding, nationally consistent list of requirements, and a local authority cannot impose divergent demands for the matters it covers. Published specifications are listed by group on the Ministry of Interior site. Many food items still have no published specification, in which case the municipality's own requirement sheet governs.

**Fees.** The business-licensing fee is a national tariff set by the Ministry of Interior and applied by every local authority, and it is charged **per licensing item**, so a business holding several items pays several fees. From 1 April 2026 the fee is 381 NIS for the main request types, among them a new licence, a licence renewal, a temporary permit, an accelerated permit and a change of ownership; a replacement for a lost or damaged licence or permit is 190.5 NIS. The tariff circular itself carries the full list of request types (see Reference Links). The tariff is re-indexed twice a year, on 1 April and 1 October, so check the current figure before quoting it to a user.

**Licence validity** is set per item in the Schedule and ranges from one year to fifteen. Never state a single blanket validity period; read it from the item.

**Which sanitary rulebook applies.** Eating places (restaurants, cafes, anything serving prepared food) are inspected against Takanot Rishuy Asakim (Tnaei Tavrua Naotim leVatei Ochel), 5743-1983. Food manufacturing sits under a separate sanitary regime and under the Public Health Protection (Food) Law, 5776-2015. Naming the right instrument matters: an owner cannot look up their binding requirement, and cannot hold a useful conversation with an inspector or consultant, without it.

**Two things to say before an owner spends money.** First, planning comes before licensing: a licence cannot be issued for a use the property is not permitted to have, so permitted-use conformity should be checked before signing a lease or fitting out a kitchen, not after a rejection. Second, a licence does not transfer with the business. Someone buying a going restaurant does not inherit the seller's licence and must apply in their own name, which is the single most expensive misunderstanding in this area.

### Step 2: Guide Kashrut Certification (Rabbanut Application)
Kashrut certification is voluntary; a business licence is not. A kashrut certificate never substitutes for a health or licensing approval.

**The legal regime changed in July 2026, and most material written between 2022 and 2025 is now wrong.** Amendment No. 5 to the Prohibition of Kashrut Fraud Law repealed the 2021 Kahana reform. Under the amendment only the Rabbanut may grant kashrut. A local kashrut authority supplies supervision within the municipality or local council where it was established; the Minister for Religious Services may authorise a religious council to supply kashrut services in an adjacent area, for a period he directs and only in defined circumstances, such as where no religious council operates there. Two consequences worth stating plainly to a user:

- The route in which a private kashrut corporation certified a business in its own name, as an alternative to the local rabbi, is closed. In practice the 2021 reform was largely never implemented before it was repealed, so businesses that believed they were waiting for it were never able to use it.
- Private badatzim have not disappeared. They operate as they did before the 2021 reform: as an additional layer on top of the local rabbinate's certificate, not instead of it.

**The mashgiach payment rule is coming, but it is NOT in force yet.** The amendment severs the payment link between the supervised business and its supervisor: a mashgiach's pay is to come from the local kashrut authority, and no other payment or benefit may reach the supervisor from anyone else. Those provisions commence two years after publication, so they bite from 19 July 2028, not today, and the Minister of Religious Services may defer them further. A body that already employed a given supervisor immediately before the amendment may carry on employing them even where the new conditions are not met. Tell an owner this is a 2028 change to plan for, and do NOT tell them to restructure or terminate a lawful supervision arrangement now.

Because the amendment is recent and contested, tell the user the certificate route below is the current one and to confirm the operational details with their local religious council rather than relying on any single published summary.

Process:
1. Contact the local religious council or rabbanut for the municipality where the business physically sits
2. Submit application with: business license, menu, list of suppliers, kitchen layout
3. Mashgiach (kosher supervisor) visit, which inspects ingredients, equipment, procedures
4. Ongoing: mashgiach visits (frequency depends on kashrut level)

Kashrut levels:
- Standard kosher (כשר), basic supervision
- Mehadrin (מהדרין), stricter standards and more frequent supervision
- Badatz (בד"ץ), ultra-strict private certification, layered on top of the rabbinate certificate

Prepare for mashgiach inspection:
- All ingredient labels visible with kosher certification marks
- Separate meat and dairy areas clearly marked
- Shabbat/holiday operation plan (if applicable)
- No banned ingredients (not listed on approved kosher lists)

Never rule on whether a food, ingredient, or process is kosher. That is a halachic determination reserved to a qualified rabbi. This skill explains how certification works and how to prepare for it.

### Step 3: Set Up Certification/License Renewal Tracking
Configure scheduled alerts for renewal dates:
- Business license: the validity period is set per licensing item in the Schedule and ranges from one year to fifteen, so read it off the licence itself rather than assuming an annual cycle
- Kashrut certificate: annual renewal, requires re-inspection
- Health inspection: periodic (frequency varies, typically every 6-12 months)
- Fire safety certificate: annual renewal
- Pest control documentation: quarterly

Send reminders 60 days, 30 days, and 7 days before expiration. Track required documents for each renewal. Store renewal history. If persistent memory is unavailable, export as `compliance-tracker.json`.

### Step 4: Generate Hebrew Food Labels
Israeli food labeling requirements (based on regulations from the Ministry of Health):
- Product name in Hebrew
- Ingredients list (in Hebrew, descending order by weight)
- Allergen declarations (חובת סימון אלרגנים):
  - Must declare: gluten, crustaceans, eggs, fish, peanuts, soybeans, milk, tree nuts, celery, mustard, sesame, sulfites, lupin, mollusks
  - Israel adds a fifteenth allergen that has no European equivalent: broad bean (פול), regulated in Appendix 3 of the adopted regulation because sensitivity to it is common in the Israeli population. It is NOT marked in the same way as the fourteen in Appendix 2, so do not simply append it to the list. Check the Ministry of Health allergen guide for its specific marking rule.
  - Format: bold or highlighted in ingredients list + separate allergen warning
- Nutritional information per 100g (per 100ml for liquids). A per-serving column may be added alongside it but is an optional extra, not a mandatory field, so do not fail a label for its absence
- Net weight/volume
- Country of origin
- Manufacturer/importer details
- Production date and expiration date
- Storage instructions
- Kashrut mark (if certified)
- Barcode, where the retailer requires one. This is a commercial requirement imposed by retail chains rather than a labelling duty, so a producer selling direct does not need one to be compliant

See `references/labeling-requirements.md` for detailed format specifications and example label template.

### Step 4.5: Apply Front-of-Package Red/Green Warning Labels (סימון אדום/ירוק)
Since January 1, 2020, packaged food products sold in Israel must carry red warning labels on the front of the package when they exceed nutrient thresholds for sodium, sugar, or saturated fat. A voluntary green positive label is also available for products meeting national dietary guidelines. The thresholds were set in two stages: the opening values applied from 1 January 2020, and the stricter second-stage values below replaced them from 1 January 2021. They have not moved since.

Red label thresholds (second stage, in force since January 2021):

| Nutrient | Solid foods (per 100g) | Liquids (per 100ml) |
|----------|------------------------|---------------------|
| Sodium (נתרן) | > 400 mg | > 300 mg |
| Total sugars (סוכרים) | > 10 g | > 5 g |
| Saturated fat (שומן רווי) | > 4 g | > 3 g |

Implementation notes:
- The label is a black-and-red stop-sign-style icon placed on the principal display panel (not on the back).
- Each exceeded nutrient requires its own separate red label.
- Some categories (infant food, fresh produce, water, alcohol) are excluded.
- Restaurants and ready-to-eat establishments are not required to apply red labels on prepared dishes, but packaged take-home items follow the regulation.
- Green positive label is voluntary and is granted only to products that carry no red label and meet additional sodium and processing limits.

When generating a label or evaluating a product, check thresholds against the table above and recommend reformulation if a borderline product can be moved below the threshold (e.g., reducing sodium from 410 to 390 mg/100g eliminates the red label).

### Step 5: Guide Food Import Regulations
Israel runs two import routes, and which one applies changes the paperwork and the timeline completely. Sensitive food (animal products, supplements, infant food and similar) stays on the stricter prior-approval route. Ordinary food can move on a declaration-based route, and the food reform added a European route for goods already approved in a regulated market, aimed at reducing the import burden. Establish which route the product falls into before quoting any process to the user; there is no single generic Ministry of Health import licence.

Importing food to Israel requires:
- Import license from Ministry of Health
- Food item registration (for first-time imports)
- Hebrew labelling compliant before the goods are released (confirm with the Food Service whether approval must precede arrival for the specific product; do not assume)
- Port inspection and sampling
- Kashrut certification (if kosher market)

Required documents:
- Certificate of origin
- Health certificate from country of origin
- Lab analysis results
- Hebrew label proof
- Customs declaration

### Step 6: Prepare for Health Inspections
Generate inspection preparation checklist by business type.

General checklist (all food businesses):
- [ ] Valid business license displayed
- [ ] Current kashrut certificate displayed (if applicable)
- [ ] Staff health and food-handler requirements met per the sanitary regulations applying to the business type (confirm the current form these take with the local health bureau rather than assuming a named certificate)
- [ ] Handwashing stations functional with soap and towels
- [ ] Temperature logs maintained (refrigerators, freezers, hot holding)
- [ ] Pest control documentation current
- [ ] Food stored off the floor, properly labeled with dates
- [ ] Cleaning schedule documented and followed
- [ ] No expired products on premises
- [ ] First-in-first-out (FIFO) rotation practiced

**What happens when an inspector finds something.** A defect-correction demand is a formal instrument, not an informal note: it names the defects and the period allowed to fix them, and the licensing fee tariff even carries a separate fee for cancelling one, which tells you it is a live administrative act with its own procedure. A business licence can also be suspended or the business closed, and operating without a valid licence is an offence in its own right rather than merely a paperwork lapse. Read the correction period off the notice the business actually received and never quote a generic number of days; if the owner disputes the demand, the objection route is through the licensing authority that issued it.

Additional for restaurants:
- [ ] Kitchen ventilation functioning
- [ ] Grease trap maintained
- [ ] Separate prep areas for raw and cooked food
- [ ] Allergen information available for customers

### Step 7: Apply VAT Rules (Maam) for Food Businesses
Israel's standard VAT (maam, מע"מ) rate rose to 18% on January 1, 2025 (from 17%). Food businesses must register with the Tax Authority as osek murshe and charge 18% on most sales.

Key rules:
- Standard rate: 18% on cooked food, packaged food, beverages, restaurant service, catering, delivery fees.
- Zero rate (0%): sale of fresh fruits and vegetables (whole, unprocessed). Once processed, packaged, or sold as a prepared dish, the standard 18% rate applies.
- Restaurant service is fully taxed at 18%, including the food component (no split between fresh-produce ingredient and prepared-dish output).
- Imported food: 18% VAT applies at customs clearance, on top of any customs duties.
- Tipping: not subject to VAT when paid voluntarily by the customer; service charges added to the bill are taxed at 18%.
- A VAT-registered food business issues a tax invoice (חשבונית מס) and files monthly or bi-monthly VAT reports (Doch Maam).

For invoice and reporting workflow, refer the user to the `israeli-vat-reporting` skill.

## Examples

### Example 1: New Restaurant Seeking Business License and Kashrut
User says: "I'm opening a restaurant in Jerusalem and need all the permits"
Actions:
1. Determine business type: restaurant (מסעדה), then identify MOH requirements
2. List required permits: business license, kashrut from Jerusalem Rabbanut, fire safety, health inspection
3. Generate document checklist: kitchen layout, ventilation plan, supplier list, menu
4. Guide kashrut application process for Jerusalem Rabbanut
5. Set up renewal tracking for all certifications
6. Prepare health inspection checklist
Result: Complete permit roadmap with timeline. Business license application prepared, Rabbanut application checklist ready. Renewal tracking configured with alerts starting 60 days before each expiration.

### Example 2: Creating Food Labels for a New Product
User says: "I'm launching a hummus product and need Hebrew labels"
Actions:
1. Determine product category: ready-to-eat chilled food
2. Collect: ingredients list, allergen info, nutritional data
3. Generate Hebrew label with all required fields (ingredients, allergens, nutrition table)
4. Highlight allergens: sesame (שומשום), chickpeas (note: not in mandatory list but common allergen)
5. Add storage instructions ("יש לאחסן בקירור עד 4°C")
6. Format per Israeli labeling regulations
Result: Complete Hebrew food label ready for printing. Includes: bilingual product name, full ingredients in Hebrew (descending by weight), allergen warning box, nutrition per 100g, manufacturer details, expiry format, and storage instructions.

### Example 3: Preparing for Health Inspection
User says: "We have a health inspection next week, help me prepare"
Actions:
1. Determine business type and last inspection results (if available)
2. Generate comprehensive inspection checklist
3. Identify high-priority items: temperature logs, staff fitness and exclusion records, pest control docs
4. Walk through common failure points: expired products, improper storage, missing documentation
5. Create day-of-inspection quick checklist
6. Suggest last-minute fixes for common issues
Result: 32-item inspection checklist organized by priority. Top 5 critical items highlighted (temperature logs, staff fitness and exclusion records, handwashing stations, food labeling, pest control). Day-of checklist for the morning before inspection.

## Bundled Resources

### References
- `references/health-ministry-requirements.md`: Ministry of Health licensing requirements by food business type, including required documents, facility standards, inspection criteria, and renewal schedules. Consult when determining licensing needs in Step 1 or preparing for inspections in Step 6.
- `references/labeling-requirements.md`: Israeli food labeling regulations, including mandatory fields, allergen declaration requirements, nutritional information format, red/green front-of-package thresholds, Hebrew label template, and import labeling rules. Consult when generating food labels in Step 4 or guiding import regulations in Step 5.

### Reference Links
- Ministry of Health, food labeling: https://www.gov.il/he/pages/food-labeling
- Ministry of Health, allergen marking guide (Regulation 1169/2011): https://www.gov.il/he/pages/allergens-guidance
- Front-of-package labeling regulations (Efsharibari): https://efsharibari.health.gov.il/en/governance/legislation/unhealthy-food-labeling-law/
- Chief Rabbinate of Israel (kashrut): https://www.gov.il/he/departments/chief_rabbinate_of_israel
- Uniform specifications + "Tzav HaChacham" item search (Ministry of Interior): https://www.gov.il/he/departments/units/reform1/govil-landing-page
- Business licensing fee tariff (Ministry of Interior): https://www.gov.il/he/pages/fee-height
- Israel Tax Authority (VAT / maam): https://www.gov.il/he/departments/israel_tax_authority
- Sanitary conditions for eating places (regulations, 1983): https://www.gov.il/he/pages/health-mazon37a
- Food regulation based on the European Union, incl. the importer routes: https://www.gov.il/he/pages/food-regulation-european-union
- Israel Standards Institute (תקני מזון): https://www.sii.org.il/

## Gotchas

- Kashrut certification levels (Rabbanut, Mehadrin, Badatz) are not interchangeable. Agents may treat them as equivalent, but each has different supervision requirements, costs, and market implications.
- Israeli food labeling regulations require allergen declarations in a specific bold/highlighted format that differs from EU and US standards. Agents trained on international labeling norms will produce non-compliant labels.
- The Ministry of Health business licensing categories changed in recent years, and the classification of food trucks (rechev mazon) now requires a different permit path than a fixed restaurant. Agents may use outdated classification rules.
- Import sequencing in Israel differs from US and EU flows, and the Hebrew label must be compliant and ready before the goods are released. Do not assert that a label approval is required before the shipment physically arrives without checking the specific route with the Food Service; agents state this confidently in both directions.
- Pest control documentation in Israel must come from a licensed company registered with the Ministry of Environmental Protection. Agents may suggest generic pest control solutions that do not meet Israeli regulatory requirements.
- The 2021 Kahana kashrut reform was repealed in July 2026, and agents trained on 2022-2025 material will confidently describe a competitive certification market that no longer exists (and that largely never operated). Do not tell a business owner they may choose a private kashrut corporation instead of the local rabbinate. Check the date of any kashrut source before relying on it.
- Allergen marking duties currently attach to pre-packed food. A restaurant meal sold through a delivery aggregator is not pre-packed food, and the duty to mark allergens on non-pre-packed food was deferred to 1 January 2032. Agents asked about delivery platforms tend to invent a delivery-specific labelling regulation; there is none. Say what the duty actually is and when it starts.
- The front-of-package thresholds have been stable since the second stage took effect in January 2021, but the wider labelling regime is mid-transition to the adopted European rules, with a transition period running to 1 January 2028 for pre-packed food. A rule that takes effect in the future must not be described as if it applies today, and the converse. State which regime a given instruction belongs to.

## Troubleshooting

### Error: "Business license application rejected"
Cause: Missing documents, facility doesn't meet requirements, or zoning issue.
Solution: Check rejection reason from the municipal licensing authority. Common issues: kitchen layout not approved, ventilation insufficient, or business location not zoned for food service. Address specific deficiency and resubmit. Consider hiring a licensed consultant (yo'etz rishuy) for complex cases.

### Error: "Kashrut inspection failed"
Cause: Non-kosher ingredients found, or separation requirements not met.
Solution: Review mashgiach's report for specific findings. Common issues: supplier without proper kosher certification, cross-contamination between meat and dairy areas, ingredients not on approved list. Replace non-compliant ingredients and request re-inspection.

### Error: "Food label rejected by MOH"
Cause: Missing required fields or incorrect format.
Solution: Verify every mandatory field is present (see Step 4). Note that the barcode is a retailer requirement rather than a mandatory legal field, so do not count it when checking compliance, and per-serving nutrition data is optional rather than a rejection cause. Common issues: allergen declaration not in correct format (must be bold/highlighted), Hebrew translation inaccurate. Use references/labeling-requirements.md as checklist.

### Error: "Health inspection violation notice"
Cause: Critical violation found during inspection (temperature abuse, pest evidence, expired products).
Solution: Address critical violations immediately. Temperature abuse: discard affected food, recalibrate thermometers, document corrective action. Pest evidence: call licensed pest control immediately, document treatment. Expired products: remove and document disposal. Correction windows vary by severity and are set by the inspector in the notice itself; do not quote a specific number of days to a user, read it off their notice.
