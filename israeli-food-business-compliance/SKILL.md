---
name: israeli-food-business-compliance
description: Guide Israeli food business regulatory compliance, including business licensing, kashrut certification, health ministry requirements, food labeling (with red/green front-of-package labels), and 18% VAT rules. Use when user asks about "food business license Israel", "Misrad HaBriut requirements", "kashrut certification process", "food labeling Hebrew", "restaurant permit Israel", "food import regulations", "red label sugar salt fat", or "רישיון עסק מזון". Covers Ministry of Health licensing by business type, Rabbanut and Tzohar kashrut application process, certification renewal tracking, Hebrew food label generation, front-of-package red/green warning labels, and health inspection preparation. Do NOT use for restaurant daily operations (use israeli-restaurant-ops) or general business compliance.
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

### Step 2: Guide Kashrut Certification (Rabbanut Application)
Most Israeli restaurants and food businesses seek kosher certification from the local Rabbanut (rabbinical authority).

Process:
1. Contact local Rabbanut office (varies by municipality)
2. Submit application with: business license, menu, list of suppliers, kitchen layout
3. Mashgiach (kosher supervisor) visit, which inspects ingredients, equipment, procedures
4. Ongoing: mashgiach visits (frequency depends on kashrut level)

Kashrut levels:
- Standard kosher (כשר), basic supervision
- Mehadrin (מהדרין), stricter standards and more frequent supervision
- Badatz (בד"ץ), ultra-strict, private certification bodies
- Tzohar Food Inspection (צהר), an alternative nationwide kashrut supervision body operating alongside the Chief Rabbinate's system, whose supervisors are employed directly by Tzohar rather than by the businesses they inspect. Also recognized under the Kahana 2022 reform that allows certified private corporations to provide kashrut supervision under Chief Rabbinate oversight (rolling implementation from 2023).

Note: Since the 2022 kashrut reform, businesses can choose between Rabbanut, Tzohar, or any approved private supervision corporation; supervision certificates must follow the standardized format set by the Chief Rabbinate.

Prepare for mashgiach inspection:
- All ingredient labels visible with kosher certification marks
- Separate meat and dairy areas clearly marked
- Shabbat/holiday operation plan (if applicable)
- No banned ingredients (not listed on approved kosher lists)

### Step 3: Set Up Certification/License Renewal Tracking
Configure scheduled alerts for renewal dates:
- Business license: typically annual renewal
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
  - Format: bold or highlighted in ingredients list + separate allergen warning
- Nutritional information per 100g and per serving
- Net weight/volume
- Country of origin
- Manufacturer/importer details
- Production date and expiration date
- Storage instructions
- Kashrut mark (if certified)
- Barcode (Israeli standard)

See `references/labeling-requirements.md` for detailed format specifications and example label template.

### Step 4.5: Apply Front-of-Package Red/Green Warning Labels (סימון אדום/ירוק)
Since January 1, 2020, packaged food products sold in Israel must carry red warning labels on the front of the package when they exceed nutrient thresholds for sodium, sugar, or saturated fat. A voluntary green positive label is also available for products meeting national dietary guidelines. The Scientific Committee at the Ministry of Health updates these criteria periodically (three formal updates between 2020 and 2024).

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
Importing food to Israel requires:
- Import license from Ministry of Health
- Food item registration (for first-time imports)
- Hebrew label approval before import
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
- [ ] Staff health certificates (teudat briut) up to date
- [ ] Handwashing stations functional with soap and towels
- [ ] Temperature logs maintained (refrigerators, freezers, hot holding)
- [ ] Pest control documentation current
- [ ] Food stored off the floor, properly labeled with dates
- [ ] Cleaning schedule documented and followed
- [ ] No expired products on premises
- [ ] First-in-first-out (FIFO) rotation practiced

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
Result: Complete Hebrew food label ready for printing. Includes: bilingual product name, full ingredients in Hebrew (descending by weight), allergen warning box, nutrition per 100g and per serving, manufacturer details, expiry format, and storage instructions.

### Example 3: Preparing for Health Inspection
User says: "We have a health inspection next week, help me prepare"
Actions:
1. Determine business type and last inspection results (if available)
2. Generate comprehensive inspection checklist
3. Identify high-priority items: temperature logs, staff health certificates, pest control docs
4. Walk through common failure points: expired products, improper storage, missing documentation
5. Create day-of-inspection quick checklist
6. Suggest last-minute fixes for common issues
Result: 32-item inspection checklist organized by priority. Top 5 critical items highlighted (temperature logs, health certificates, handwashing stations, food labeling, pest control). Day-of checklist for the morning before inspection.

## Bundled Resources

### References
- `references/health-ministry-requirements.md`: Ministry of Health licensing requirements by food business type, including required documents, facility standards, inspection criteria, and renewal schedules. Consult when determining licensing needs in Step 1 or preparing for inspections in Step 6.
- `references/labeling-requirements.md`: Israeli food labeling regulations, including mandatory fields, allergen declaration requirements, nutritional information format, red/green front-of-package thresholds, Hebrew label template, and import labeling rules. Consult when generating food labels in Step 4 or guiding import regulations in Step 5.

### Reference Links
- Ministry of Health, Food Service: https://www.gov.il/he/pages/food-labeling
- Front-of-package labeling regulations (Efsharibari): https://efsharibari.health.gov.il/en/governance/legislation/unhealthy-food-labeling-law/
- Chief Rabbinate of Israel (kashrut): https://www.gov.il/he/departments/the_chief_rabbinate_of_israel
- Tzohar Food Inspection: https://www.tzohar.org.il/?page_id=16250
- Business Licensing Authority (rishyon esek): https://www.gov.il/he/departments/topics/business_licensing
- Israel Tax Authority (VAT / maam): https://www.gov.il/he/departments/israel_tax_authority
- Israel Standards Institute (תקני מזון): https://www.sii.org.il/

## Gotchas

- Kashrut certification levels (Rabbanut, Mehadrin, Badatz) are not interchangeable. Agents may treat them as equivalent, but each has different supervision requirements, costs, and market implications.
- Israeli food labeling regulations require allergen declarations in a specific bold/highlighted format that differs from EU and US standards. Agents trained on international labeling norms will produce non-compliant labels.
- The Ministry of Health business licensing categories changed in recent years, and the classification of food trucks (rechev mazon) now requires a different permit path than a fixed restaurant. Agents may use outdated classification rules.
- Israeli food import regulations require Hebrew label approval before the goods enter the country, not after. Agents familiar with US/EU import flows may sequence this step incorrectly.
- Pest control documentation in Israel must come from a licensed company registered with the Ministry of Environmental Protection. Agents may suggest generic pest control solutions that do not meet Israeli regulatory requirements.
- Kashrut reform 2022 (the "Kahana law") is in rolling implementation through 2026, with the Chief Rabbinate retaining ultimate oversight. Some municipalities (notably Bnei Brak and several Charedi neighborhoods) have been slower to recognize Tzohar and other private corporations' supervision. When advising a business owner, ask which neighborhood the establishment serves before recommending a non-Rabbanut path; consumer recognition still skews to Rabbanut in religious neighborhoods.
- Israeli "Cooked Food Delivery Regulations" introduced in 2024 require Hebrew allergen labels on prepared foods sold via delivery aggregators (Wolt, 10bis, Cibus). Restaurants that previously skipped paper labels because items were eaten in-house must now print allergen info on each delivery packaging. Aggregator platforms also display allergen warnings in-app and pull data from the merchant's profile.
- Front-of-package red label thresholds were last revised in 2024. The Scientific Committee at the Ministry of Health publishes any updates and a transition period. Verify your nutrition panel against the latest thresholds at efsharibari.health.gov.il before printing labels at scale.

## Troubleshooting

### Error: "Business license application rejected"
Cause: Missing documents, facility doesn't meet requirements, or zoning issue.
Solution: Check rejection reason from the municipal licensing authority. Common issues: kitchen layout not approved, ventilation insufficient, or business location not zoned for food service. Address specific deficiency and resubmit. Consider hiring a licensed consultant (yo'etz rishuy) for complex cases.

### Error: "Kashrut inspection failed"
Cause: Non-kosher ingredients found, or separation requirements not met.
Solution: Review mashgiach's report for specific findings. Common issues: supplier without proper kosher certification, cross-contamination between meat and dairy areas, ingredients not on approved list. Replace non-compliant ingredients and request re-inspection.

### Error: "Food label rejected by MOH"
Cause: Missing required fields or incorrect format.
Solution: Verify all 12 mandatory fields are present (see Step 4). Common issues: allergen declaration not in correct format (must be bold/highlighted), nutritional info missing per-serving data, Hebrew translation inaccurate. Use references/labeling-requirements.md as checklist.

### Error: "Health inspection violation notice"
Cause: Critical violation found during inspection (temperature abuse, pest evidence, expired products).
Solution: Address critical violations immediately. Temperature abuse: discard affected food, recalibrate thermometers, document corrective action. Pest evidence: call licensed pest control immediately, document treatment. Expired products: remove and document disposal. Inspector typically allows 7-30 days for correction depending on severity.
