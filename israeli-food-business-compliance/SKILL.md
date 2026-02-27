---
name: israeli-food-business-compliance
description: >-
  Guide Israeli food business regulatory compliance — business licensing,
  kashrut certification, health ministry requirements, and food labeling. Use
  when user asks about "food business license Israel", "Misrad HaBriut
  requirements", "kashrut certification process", "food labeling Hebrew",
  "restaurant permit Israel", "food import regulations", or "רישיון עסק מזון".
  Covers Ministry of Health licensing by business type, Rabbanut kashrut
  application process, certification renewal tracking, Hebrew food label
  generation, and health inspection preparation. Do NOT use for restaurant
  daily operations (use israeli-restaurant-ops) or general business compliance.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: >-
  Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for
  certification renewal tracking and scheduled compliance alerts.
metadata:
  author: skills-il
  version: 1.0.0
  category: food-and-dining
  tags:
    he:
      - בטיחות-מזון
      - כשרות
      - משרד-הבריאות
      - רישוי
      - תיוג
      - ישראל
    en:
      - food-safety
      - kashrut
      - health-ministry
      - licensing
      - labeling
      - israel
  display_name:
    he: תאימות רגולטורית לעסקי מזון ישראליים
    en: Israeli Food Business Compliance
  display_description:
    he: ליווי עסקי מזון ישראליים ברגולציה — רישוי עסקים, כשרות, משרד הבריאות ותיוג מזון
    en: >-
      Guide Israeli food business regulatory compliance — business licensing,
      kashrut certification, health ministry requirements, and food labeling.
  openclaw:
    requires:
      bins: []
      env: []
    emoji: "🏥"
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
3. Mashgiach (kosher supervisor) visit — inspects ingredients, equipment, procedures
4. Ongoing: mashgiach visits (frequency depends on kashrut level)

Kashrut levels:
- Standard kosher (כשר) — basic supervision
- Mehadrin (מהדרין) — stricter standards, more frequent supervision
- Badatz (בד"ץ) — ultra-strict, private certification bodies

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

## Examples

### Example 1: New Restaurant Seeking Business License and Kashrut
User says: "I'm opening a restaurant in Jerusalem and need all the permits"
Actions:
1. Determine business type: restaurant (מסעדה) — identify MOH requirements
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
- `references/health-ministry-requirements.md` — Ministry of Health licensing requirements by food business type: required documents, facility standards, inspection criteria, and renewal schedules. Consult when determining licensing needs in Step 1 or preparing for inspections in Step 6.
- `references/labeling-requirements.md` — Israeli food labeling regulations: mandatory fields, allergen declaration requirements, nutritional information format, Hebrew label template, and import labeling rules. Consult when generating food labels in Step 4 or guiding import regulations in Step 5.

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

