---
name: israeli-restaurant-ops
description: Help Israeli restaurant owners optimize menus, pricing, and daily operations for delivery platforms. Use when user asks about "restaurant management Israel", "Wolt commission", "10bis pricing", "Mishlocha", "menu optimization", "food cost analysis", "delivery commission", "review response", or "ניהול מסעדה". Covers menu copy optimization, pricing strategy with commission awareness, review response drafting, platform comparison, food cost analysis, and daily operations. Do NOT use for cooking recipes, personal meal planning, or non-Israeli delivery platforms.
license: MIT
---


# Israeli Restaurant Operations

## Instructions

### Step 1: Optimize Menu Copy for Delivery Platforms
Help write compelling Hebrew menu descriptions that perform well on delivery platform search and attract orders:

**Menu Item Template:**
```
שם המנה: [שם קצר וברור, 3-5 מילים]
תיאור: [1-2 משפטים שמתארים טעם, מרקם, ואופן הכנה]
תגיות: [כשר/טבעוני/ללא גלוטן/חריף/פופולרי]
```

Guidelines for Hebrew menu descriptions:
- Write naturally in Hebrew, not translated from English
- Lead with the protein or main ingredient
- Mention cooking method (על האש, בתנור, מוקפץ)
- Include sensory words (פריך, עסיסי, קרמי, מעושן)
- Add dietary labels in Hebrew: טבעוני, צמחוני, ללא גלוטן, ללא לקטוז
- **Kashrut labels are different from dietary labels and are gated by law. Never add כשר or כשר למהדרין to a menu on your own initiative.** See "Kashrut claims" below before writing any kashrut wording
- Keep names short for mobile screens (most delivery orders come from phones)
- **Allergens are a regulatory duty, not a nice-to-have.** Israel's allergen list runs to fifteen items (the fourteen international ones plus פול). Do not invent or guess a dish's allergen profile from its description: get it from the kitchen, item by item. For the full list and the current marking obligations for prepared and packaged food, see the companion skill **israeli-food-business-compliance**
- Use category names that match how Israelis search: עיקריות, מנות ראשונות, תוספות, משקאות, קינוחים

**Platform-specific tips:**
- **Wolt**: Supports rich category structures and modifier groups. Use detailed descriptions. Photos are critical for conversion.
- **10bis**: Simpler menu structure. Keep descriptions concise. Corporate lunch customers want clear portions and pricing.
- **Mishlocha**: Category-based with combo support. Consider building combo deals (מנה + שתייה + תוספת).

**Kashrut claims (a criminal-liability gate, not a copy decision):**

Under **חוק איסור הונאה בכשרות, התשמ"ג-1983 §3(א)**, "בעל בית אוכל לא יציג בכתב את בית האוכל ככשר, אלא אם כן ניתנה לו תעודת הכשר". Writing כשר on a menu without a valid certificate is an offence, and **§14 sets the penalty at up to one year's imprisonment**. §3(ב) adds that a certified restaurant presented in writing as kosher may not serve or sell items that are not themselves covered by the certificate. §10 requires the certificate to be displayed in a visible place, and only while it is in force.

So, before writing any kashrut wording:

1. **Ask whether the restaurant holds a current תעודת הכשר**, and for which items. If the answer is no or unclear, write no kashrut claim at all, in any language, on any platform.
2. **Copy the wording from the certificate.** Do not upgrade כשר to כשר למהדרין, and do not infer a level from ingredients or from a supplier's certification. The levels are not interchangeable. Wording naming a private certifying body (בד"ץ and the like) must be re-checked against the post-amendment regime before it goes on a menu.
3. **Never rule on whether a food, ingredient or process is kosher.** That is the certifying authority's call, not the agent's and not the owner's.

**Who may certify changed in July 2026.** תיקון מס' 5 (ס"ח תשפ"ו, 778, 19 July 2026) repealed the private licensed-certifier track introduced by the earlier reform. For a בית אוכל the certificate now comes from **the local rabbi serving where the restaurant is located, or from מועצת הרבנות הראשית** (and, where no local rabbi is serving, a rabbi authorised by the Council), issued through the local kashrut authority, the authorised religious council or the Chief Rabbinate. If the restaurant's certificate came from a private body under the previous regime, flag that it needs re-checking rather than assuming it still stands.

For the full regulatory picture (licensing, allergens, labelling, food-safety inspections) see the companion skill **israeli-food-business-compliance**, which is the authority in this directory on food-business regulation. This skill covers menus, pricing and platform operations.

### Step 2: Calculate Pricing with Commission Awareness
Help set menu prices that maintain target margins after platform commissions:

**Commission Rates by Platform:**

**Read this before quoting a number.** None of the three platforms publishes its merchant commission. The ranges below are the industry ballpark reported by Israeli restaurateurs, not published rates, and actual terms are negotiated per restaurant and vary with volume, category, exclusivity and whether the restaurant or the platform supplies delivery. **Always ask the owner for the rate in their own contract and compute with that.** Use these only to sanity-check an order of magnitude, and say so when you do.

| Platform | Commission (indicative, verify in contract) | Payment Cycle (verify) | Notes |
|----------|--------------------------------------------|------------------------|-------|
| Wolt | roughly 25-35% | Typically weekly | Higher commission, but the largest customer base |
| 10bis (תן ביס) | roughly 10-15% | Typically monthly | Lower commission, strong in corporate/office areas. Older public reporting cites 7-12%, so treat the lower end as plausible |
| Mishloha (משלוחה) | roughly 15-25% | Typically bi-weekly | Mid-range, strong in specific cities |

Because every worked example below depends on the commission, run them with the owner's real rate. The arithmetic is the deliverable; the sample percentages are not.

**Pricing Formula:**

**The price on a delivery platform is the final consumer price, so it already includes VAT.** Getting this direction wrong is the most common and most expensive mistake in delivery pricing: treat the commission-grossed number as if VAT still had to be added, publish it anyway, and the restaurant silently absorbs the VAT. Work in one direction only:

```
Target Net Revenue = what the restaurant must keep, net of VAT and net of commission
Displayed Price (VAT-inclusive) = Target Net Revenue x 1.18 / (1 - Commission Rate)
```

Check any price with the reverse calculation, which is what actually lands in the bank:

```
Revenue net of VAT   = Displayed Price / 1.18
Commission           = Commission Rate x Displayed Price   (confirm in the contract whether
                       the platform charges on the VAT-inclusive or VAT-exclusive amount;
                       this changes the answer, and the two are not interchangeable)
Realised net revenue = Displayed Price / 1.18  -  Commission / 1.18
```

**Example Calculation:**
A schnitzel plate with food cost of 18 NIS, targeting a 60% gross margin on food:
- Target net revenue: 18 / (1 - 0.60) = 45 NIS
- Wolt (30% commission): 45 x 1.18 / 0.70 = 75.9, publish **76 NIS** (realised: 76/1.18 - 22.80/1.18 = 45.1)
- 10bis (12% commission): 45 x 1.18 / 0.88 = 60.3, publish **60 NIS** (realised 44.8)
- Mishloha (20% commission): 45 x 1.18 / 0.80 = 66.4, publish **66 NIS** (realised 44.8)

Note how far these sit above the naive "45 / (1 - commission)" answer. Publishing 65 NIS on Wolt for this dish returns only 38.6 NIS net, a 14% shortfall against the 45 target, and the gap is invisible until the monthly statement.

Many restaurants set a single price across platforms and absorb the margin difference, or set slightly higher prices on higher-commission platforms. Help the owner decide which strategy fits their business, and show them what the parity choice costs per order rather than just asserting one.

**Delivery Fee Considerations:**
- Some platforms charge the restaurant for delivery, others charge the customer
- Factor delivery-related packaging costs (containers, bags, utensils): typically 3-8 NIS per order
- Minimum order amounts vary by platform and affect average order value

### Step 3: Draft Review Responses in Hebrew
Help draft professional, warm Hebrew responses to customer reviews on delivery platforms:

**For positive reviews (4-5 stars):**
```
שלום [שם], תודה רבה על המילים החמות! שמחים שנהנית מ[המנה/החוויה]. מחכים לך בהזמנה הבאה 🙏
```

**For negative reviews (1-3 stars) about food quality:**
```
שלום [שם], תודה שהקדשת זמן לשתף אותנו. מצטערים לשמוע שהחוויה לא עמדה בציפיות. בדקנו את הנושא עם הצוות שלנו ו[פעולה שננקטה]. נשמח להזמין אותך שוב ולהוכיח שאנחנו יכולים טוב יותר. אפשר ליצור קשר ב-[טלפון] ונשמח לתקן את הרושם.
```

**For negative reviews about delivery time (not the restaurant's fault):**
```
שלום [שם], מצטערים על העיכוב. המנה יצאה מהמטבח שלנו בזמן, אבל לצערנו אין לנו שליטה על זמני השליח. העברנו את המשוב לפלטפורמה. נשמח לראות אותך שוב.
```

**For negative reviews about wrong/missing items:**
```
שלום [שם], מצטערים מאוד על הטעות. לקחנו את זה לטיפול ושיפרנו את תהליך הבדיקה שלנו לפני שליחה. נשמח לפצות אותך בהזמנה הבאה. צרו קשר ב-[טלפון].
```

**Response guidelines:**
- Always respond within 24-48 hours
- Never argue with the customer, even if the complaint seems unfair
- Keep responses under 500 characters (platform limits)
- Offer a concrete resolution, not just "we're sorry"
- Include a phone number for direct contact on serious complaints
- Match the customer's language (if they wrote in Hebrew, respond in Hebrew; same for English or Arabic)

### Step 4: Compare Delivery Platforms
Help restaurant owners decide which platforms to join based on their restaurant type and location:

**Platform Comparison:**

| Factor | Wolt | 10bis (תן ביס) | Mishloha (משלוחה) |
|--------|------|-----------------|-------------------|
| Commission (indicative, verify in contract) | roughly 25-35% | roughly 10-15% | roughly 15-25% |
| Customer Base | Largest, young urban crowd | Strong in corporate/office zones | City-specific strengths |
| Delivery | Wolt couriers | Mixed (own + external) | Partner couriers |
| Payment to Restaurant | Weekly | Monthly | Bi-weekly |
| Best For | High-volume, urban restaurants | Restaurants near office buildings | Mid-size cities, local favorites |
| Onboarding | Structured process, photos required | Simpler setup | Varies by region |
| Analytics Dashboard | Detailed (orders, ratings, trends) | Basic | Basic to moderate |
| Corporate Orders | Limited | Strong (meal benefit cards) | Limited |

**Decision framework by restaurant type:**
- **New restaurant, urban area**: Start with Wolt for visibility, add 10bis if near offices
- **Established restaurant, loyal base**: Mishlocha (lower commission) + Wolt for new customers
- **Near office buildings/industrial zones**: 10bis is a must (corporate meal benefits)
- **Small town/periphery**: Mishlocha often has better coverage outside Tel Aviv/center
- **High-end restaurant**: Consider Wolt only, where presentation and branding tools are best

**Important note about 10bis dual model:**
10bis operates as both a consumer delivery service and a corporate meal benefit platform (ארוחת עובדים). The corporate side has lower commissions but different order patterns (weekday lunches, set budget per employee). Make sure the owner understands which 10bis program they are joining.

**Cibus / Pluxee (corporate meal-benefit alternative):**
Cibus (rebranded Cibus Pluxee in June 2023 as part of the Sodexo spin-off) is the main corporate meal-benefit competitor to 10bis in Israel. If the restaurant is targeting office workers, evaluate both - restaurants frequently join both platforms because employee benefit cards are not interchangeable. Commission and onboarding terms differ from 10bis; consult cibus.co.il directly for current rates.

### Step 5: Analyze Food Costs and Menu Engineering
Help with recipe costing, margin analysis, and menu optimization using the menu engineering matrix:

**Recipe Costing Template:**
```
מנה: [שם]
מרכיבים:
  - [מרכיב 1]: [כמות] x [מחיר ליחידה] = [עלות]
  - [מרכיב 2]: [כמות] x [מחיר ליחידה] = [עלות]
  ...
סה"כ עלות מרכיבים: [סכום]
עלות אריזה למשלוח: [3-8 ש"ח]
עלות כוללת למנה: [סכום]
מחיר מכירה: [מחיר]
אחוז עלות מזון: [עלות / מחיר * 100]%
רווח גולמי למנה: [מחיר - עלות]
```

**Target food cost percentages by restaurant type:**
- Fast food / street food: 25-30%
- Casual dining: 28-35%
- Fine dining: 30-40%
- Delivery-only (cloud kitchen): 25-32%

**Menu Engineering Matrix (Stars/Puzzles/Dogs/Plowhorses):**

| Category | Popularity | Profitability | Action |
|----------|-----------|---------------|--------|
| Stars (כוכבים) | High | High | Promote heavily, keep as-is |
| Puzzles (חידות) | Low | High | Better descriptions, better placement, consider renaming |
| Plowhorses (סוסי עבודה) | High | Low | Raise price gradually, reduce portion cost, re-engineer recipe |
| Dogs (כלבים) | Low | Low | Remove from menu or completely reinvent |

To classify menu items, you need two data points per item:
1. **Popularity**: Number of orders per week (or % of total orders)
2. **Profitability**: Gross margin per plate (selling price minus food cost)

Items above average on both metrics are Stars. Below average on both are Dogs.

### Step 6: Plan Daily Operations and Scheduling
Help with operational checklists, food safety, and scheduling around Israeli calendar considerations:

**Before any of this: the business must be licensed.** A בית אוכל is a licensable business under **חוק רישוי עסקים, התשכ"ח-1968** and the licensing order, פריט 4.2 of the schedule. The sub-items matter for delivery specifically:

| Item | Covers |
|------|--------|
| 4.2א | מסעדה, expressly "לרבות משלוח מזון", and alcohol served on the premises |
| 4.2ב | בית קפה, מזנון or other בית אוכל, also "לרבות משלוח מזון" |
| 4.2ג | Preparing food for sale and consumption off the premises, "לרבות משלוח מזון". This is the delivery-only / cloud-kitchen row |

Two consequences an owner should hear before they onboard to a platform:

- **Operating without a licence is a strict-liability offence** (§14(ד)): up to 18 months' imprisonment or a fine, doubled for a company, plus a continuing daily fine, and a court or an administrative order can close the business (§16, §17, §20).
- **Supplying OTHER BUSINESSES can trigger a manufacturing licence, but consumer deliveries do not.** Under **חוק הגנה על בריאות הציבור (מזון), התשע"ו-2015 §25(א)** the exemption from a רישיון ייצור holds only while no more than **30%** of the food prepared there, on a weekly average, goes to bodies other than the establishment's own diners. Meals sent to end customers through Wolt, 10bis or Mishloha are supply to diners and do NOT count, so growing delivery volume does not by itself endanger the licence. Wholesale-style supply to other outlets or caterers does. Separately, a delivery-only kitchen with no on-premises diners should not assume the exemption reaches it at all.

Accessibility is a precondition of the licence (§8ב(ב)), and תקנה 84 of the accessibility-to-service regulations requires accessible seating and, for chains of ten or more branches, photographs of common dishes on request, which lands in this skill's menu scope.

Do not advise on licence applications from this skill: route the owner to **israeli-food-business-compliance** and the local licensing authority. `references/platform-guides.md` carries the fuller licensing notes.

**Opening Checklist (רשימת פתיחה):**
- [ ] Check ingredient freshness and expiry dates
- [ ] Verify delivery platform availability status is "open"
- [ ] Confirm staff assignments for the shift
- [ ] Check packaging supplies (containers, bags, utensils, napkins)
- [ ] Review previous day's reviews and respond to any unanswered ones
- [ ] Update any sold-out items on all platforms

**Closing Checklist (רשימת סגירה):**
- [ ] Mark restaurant as "closed" on all delivery platforms
- [ ] Record daily sales summary (total orders, revenue per platform)
- [ ] Log food waste
- [ ] Clean and sanitize kitchen per health regulations
- [ ] Update ingredient inventory
- [ ] Prep list for tomorrow

**Food Safety Temperature Log:**

These are the Israeli statutory figures, from תקנות רישוי עסקים (תנאי תברואה נאותים לבתי אוכל), התשמ"ג-1983. Do NOT use the US/HACCP numbers an agent is likely to reach for by default: the common "hot holding above 60°C" figure is **5°C below** the Israeli floor, so a log built on it certifies a breach as a pass.

| Item | Required Temp | Source | Actual Temp | Time | Initials |
|------|--------------|--------|-------------|------|----------|
| Chilled food (bacteria-friendly, unfrozen) | Not above 5°C | תקנה 50(א) | ___ | ___ | ___ |
| Frozen food and raw ground meat | Not above minus 18°C | תקנה 50(ב) | ___ | ___ | ___ |
| Hot holding, until served | At least 65°C | תקנה 51(א) | ___ | ___ | ___ |
| Thawing area | Not above 10°C | תקנה 47 | ___ | ___ | ___ |
| Received goods (chilled) | Not above 5°C | תקנה 50(א) | ___ | ___ | ___ |

**Cooling curve after cooking (תקנה 51(ב)):** sauces, salads and other dishes cooled after cooking must be cooled immediately and as fast as possible, so that the temperature at the centre of the food is not above **20°C one hour** after cooking ends and not above **5°C two hours** after. This is a separate obligation from cold storage and is the one most often missed.

**Cold-room thermometer (תקנה 21):** a recording thermometer with its display outside the cold room at 1.60-1.70m, visible, accurate to **±0.5°C**.

**Grease separator (מפריד שומן):** required by the same regulations, installed per the director's instructions. Worth a line on the opening checklist since a blocked one is both a health-inspection finding and a shutdown risk.

**Israeli Calendar Scheduling Considerations:**
- **Shabbat**: Most restaurants close Friday afternoon through Saturday evening. Update platform hours weekly (sunset times change seasonally).
- **Jewish holidays**: Rosh Hashana, Yom Kippur, Sukkot, Pesach, Shavuot all require schedule changes. Some restaurants stay open on holidays, others close.
- **Pesach**: Major menu changes required (no chametz). Plan a separate Pesach menu at least 2 weeks ahead.
- **Ramadan**: Restaurants in mixed cities may see different order patterns. Late-night orders increase significantly.
- **Memorial Day / Independence Day**: Yom HaZikaron (low orders, somber mood) immediately followed by Yom HaAtzmaut (high demand, BBQ orders spike).
- **Summer hours**: Extended evening hours, more delivery orders after 9pm.

**Staff cost is the other half of the margin, and it has a sector-specific floor.**

Restaurants are covered by a sector extension order (צו הרחבה בענף ההסעדה), which sets a **higher minimum wage than the rest of the economy**, and an employer may not pay below it:

| | Restaurant sector (הסעדה) | General economy |
|---|---|---|
| From 01.04.2026 | **₪7,281.55 / month, ₪40.00 / hour** | ₪6,443.85 / month, ₪35.40 / hour |
| Relationship | 113% of the general minimum wage | - |
| From 01.04.2027 | rises to 116% of the general minimum | - |

Do not compute the hourly rate as monthly divided by 182. Use the published hourly figure.

**Overtime and rest-day premiums (חוק שעות עבודה ומנוחה, התשי"א-1951):**

| When | Rate |
|------|------|
| First 2 overtime hours in a day (§16(א)) | 125% |
| Each overtime hour after that (§16(א)) | 150% |
| Weekly rest (Shabbat) (§17(א)) | 150%, **plus** compensating rest hours, which cannot be paid out instead |

Employing staff during the weekly rest requires a permit (היתר עבודה בשבת); it is not simply a pay question.

**Tips are wages, not a gratuity the employer can ignore.** Following the National Labour Court's consolidated ruling in עב"ל 44405-10-15 / ע"ע 28480-02-16 (26.03.2018), from 2019 a tip in the restaurant sector belongs to the restaurant and, once paid to the employee, forms part of their wage. Practically: the waiter passes the tip to the employer, the employer records it in the till, pays it through the **payslip**, and income tax, Bituach Leumi and pension are computed on the tip-inclusive wage. Whatever the arrangement, the employee's total must reach at least the applicable minimum wage, which in a restaurant is the sector floor above. Tips at event halls and gardens (אולמות וגני אירועים) are treated differently and are outside this rule.

Whether VAT applies to a tip is a separate question that turns on how it was taken and recorded: route it to israeli-food-business-compliance and the restaurant's accountant rather than answering it here. This skill does not compute payroll and is not employment-law advice. Confirm any specific case with an accountant or an employment lawyer.

**Staff scheduling tip**: factor the Shabbat, holiday and overtime premiums above into staffing decisions for high-demand delivery periods, since they can invert the margin on a shift that looks profitable on revenue alone.

## Examples

### Example 1: Setting Prices for a New Hummus Restaurant
User says: "I'm opening a hummus place in Ramat Gan, my food cost per plate is about 12 NIS. How should I price for delivery?"

Analysis:
1. Target food cost: ~30% (casual dining)
2. That means menu price should be around 40 NIS (12 / 0.30)
3. But delivery requires packaging (add 5 NIS cost, so total cost = 17 NIS)
4. With 30% food cost target: 17 / 0.30 = ~57 NIS (too high for hummus)
5. Adjust to 35% food cost: 17 / 0.35 = ~49 NIS

Platform pricing (displayed prices include VAT, per the formula in Step 2):
- 10bis (12% commission): 49 x 1.18 / 0.88 = 65.1, publish 65 NIS
- Mishloha (20% commission): 49 x 1.18 / 0.80 = 72.3, publish 72 NIS
- Wolt (30% commission): 49 x 1.18 / 0.70 = 82.6, publish 83 NIS

Recommendation: Ramat Gan has heavy office presence, so prioritize 10bis, where the low commission lets the dish sit at 65 NIS. If the owner wants one price everywhere for simplicity, it has to be the Wolt-safe 83 NIS, which is likely unsellable for hummus, so this is a case for per-platform pricing rather than parity. Consider hummus + drink + side combos to raise average order value, and price the combo through the same formula rather than by eye.

### Example 2: Rewriting a Menu Description
User says: "My shakshuka listing on Wolt isn't getting orders. The description just says 'shakshuka with bread'"

Before:
```
שקשוקה עם לחם
```

After:
```
שקשוקה ביתית על האש
עגבניות טריות מבושלות לאט עם פלפלים קלויים, תבלינים מהמטבח ושתי ביצים עלומות. מוגשת עם לחם טרי מהטאבון. מנה ל-1.
תגיות: צמחוני
```

Why this works better: Sensory words (מבושלות לאט, קלויים, טריות), cooking method (על האש, מהטאבון), clear portion size, dietary labels for search filters.

**Note what this rewrite did NOT do:** it did not add a kashrut tag. The original listing carried none, and the agent has no certificate in front of it. Adding כשר here would be exactly the §3(א) offence described in Step 1. If the restaurant does hold a תעודת הכשר, ask for it and copy its wording, as a separate step.

### Example 3: Handling a Negative Review About Cold Food
User says: "I got a 2-star review on Wolt saying the food arrived cold"

Draft response:
```
שלום, מצטערים מאוד שהאוכל הגיע קר. אנחנו שמים דגש על אריזה חמה ושליחה מהירה, אבל לפעמים עיכובים בדרך משפיעים על הטמפרטורה. נשמח לפצות אותך בהזמנה הבאה. צרו קשר ב-[טלפון] ונסדר את זה.
```

Additional advice to the owner:
- Invest in insulated packaging (costs 2-3 NIS more per order but reduces cold-food complaints significantly)
- Ask Wolt about their "preparation time" setting. If you mark dishes as ready too early, they sit waiting for a courier.
- Consider which dishes travel well and which don't. Fried items lose crispiness, soups travel great, salads should be packaged separately.
- **Treat repeated cold-arrival complaints as a food-safety finding, not only a review problem.** Hot food must be held at at least 65°C until it is handed over (תקנה 51(א)). A pattern of cold arrivals means the hot-holding or the transport step is failing, which is a compliance exposure as well as a rating one. Investigate the holding line before reaching for an apology template.

## Gotchas

- Israeli delivery platform commissions sit in a different band from US platforms like DoorDash or UberEats, so agents trained on US data will assume the wrong rate. None of the Israeli platforms publishes its merchant rate: the working figures (roughly 25-35% Wolt, 10-15% 10bis, 15-25% Mishloha) are an industry ballpark to sanity-check against, and every real calculation must use the rate in the restaurant's own contract.
- The price shown on a delivery platform is the final, VAT-inclusive consumer price. An agent that computes a price and then adds 18% on top, or that grosses up for commission and forgets VAT entirely, will be wrong by roughly 15% in the direction that costs the restaurant money.
- VAT in Israel is 18%, not 20% (UK) or 0% (some US states). Agents must use the correct rate when calculating net revenue from gross order values.
- Israeli restaurants commonly close Friday afternoon through Saturday evening for Shabbat. Agents scheduling operations, promotions, or report generation must account for this weekly downtime pattern.
- 10bis (Tenbis) operates as both a corporate meal benefit platform and a consumer delivery service. The commission structure and order flow differ between the two modes. Agents may conflate them.
- Hebrew menu item text requires RTL handling. When generating or editing menu descriptions, agents must produce valid Hebrew text without mixing LTR characters in ways that break display on delivery platforms.
- Menu prices in Israel are always in NIS (New Israeli Shekel). Agents should never convert to or assume USD/EUR pricing. Rounding should be to the nearest whole shekel (no agorot on delivery platforms).
- Kosher certification levels matter and are NOT interchangeable: "כשר" (regular), "כשר למהדרין" (mehadrin), "כשר לפסח" (for Passover). Presenting a restaurant in writing as kosher without a valid תעודת הכשר is an offence under §3(א) of חוק איסור הונאה בכשרות carrying up to a year's imprisonment (§14). An agent generating menu copy must never add or upgrade a kashrut label on its own initiative, and must never decide whether something is kosher.
- Israeli food-safety temperatures are set by תקנות רישוי עסקים (תנאי תברואה נאותים לבתי אוכל), התשמ"ג-1983, and differ from the US/HACCP numbers most models default to. Hot holding is **at least 65°C** (not 60) and chilled storage is **not above 5°C**. An agent that reaches for the familiar American figures will certify a statutory breach as compliant.
- Restaurant staff have a **sector-specific minimum wage** above the national one (₪40.00/hour from 01.04.2026, versus ₪35.40 general). Any margin or labour-cost calculation built on the national minimum understates cost for this industry.
- Tips are wages in the restaurant sector, must run through the payslip, and carry income tax, Bituach Leumi and pension. Agents trained on US tipping practice will treat them as off-book income to the server.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| 10bis (Tenbis) | https://www.10bis.co.il/ | Current commission rates, corporate meal-benefit onboarding, payment cycle |
| Mishloha (משלוחה, sometimes transliterated Mishlocha) | https://www.mishloha.co.il/ | City-specific coverage, partner courier terms, regional commission |
| Wolt for Restaurants | https://explore.wolt.com/en/isr/merchant/business/restaurants | Commission tiers, onboarding requirements, analytics dashboard |
| Cibus / Pluxee Israel | https://www.cibus.co.il/ | Corporate meal-benefit competitor to 10bis (now branded Cibus Pluxee); verify current rates |
| National Food Service (Ministry of Health) | https://www.gov.il/he/departments/national_food_service | Current Israeli food-safety regulations and business-licensing requirements |
| תקנות רישוי עסקים (תנאי תברואה נאותים לבתי אוכל), התשמ"ג-1983 | https://he.wikisource.org/wiki/תקנות_רישוי_עסקים_(תנאי_תברואה_נאותים_לבתי_אוכל) | Statutory food temperatures (תקנות 47, 50, 51), cooling curve, thermometer spec, grease separator |
| חוק איסור הונאה בכשרות, התשמ"ג-1983 | https://he.wikisource.org/wiki/חוק_איסור_הונאה_בכשרות | §3 written kashrut claims, §10 display duty, §14 penalty, and who may certify after תיקון מס' 5 (2026) |
| חוק רישוי עסקים, התשכ"ח-1968 | https://he.wikisource.org/wiki/חוק_רישוי_עסקים | Licence requirement, declaration route, §14 strict liability, §20 administrative closure |
| Kol Zchut: minimum wage in the restaurant sector | https://www.kolzchut.org.il/he/שכר_מינימום_לעובדים_בתחום_ההסעדה | The הסעדה sector wage floor and its scheduled increases |
| Kol Zchut: tips for restaurant staff | https://www.kolzchut.org.il/he/תשר_(%22טיפ%22)_למלצרים_במסעדות,_בתי_קפה_וברים | Tips as wages, payslip duty, tax/BL/pension treatment |

## Troubleshooting

### Problem: Menu description not generating orders
Cause: Generic descriptions, missing dietary tags, no photos, or poor category placement.
Solution: Rewrite descriptions with sensory words and cooking methods (see Step 1). Add dietary labels. Ensure the item is in the right category. On Wolt in particular, item photos are widely reported by restaurateurs to be one of the largest single levers on conversion, though the platform publishes no figure, so treat any specific percentage you have seen as anecdotal.

### Problem: Margins too thin after platform commissions
Cause: Pricing set without accounting for commission percentages and packaging costs.
Solution: Recalculate using the formula in Step 2. Consider raising delivery prices 10-15% above dine-in prices (this is standard practice). Review food costs and look for ingredient substitutions that maintain quality.

### Problem: Too many negative reviews about delivery
Cause: Issues with courier timing, packaging, or food that doesn't travel well.
Solution: These are largely outside the restaurant's control. Use response templates from Step 3 that acknowledge the issue without accepting blame for courier delays. Invest in better packaging. Adjust "preparation time" settings so food doesn't sit waiting.

### Problem: Unsure which platform to prioritize
Cause: Each platform has different strengths, and spreading too thin can hurt service quality.
Solution: Use the comparison framework in Step 4. Start with 1-2 platforms, get operations smooth, then expand. Track orders and margins per platform monthly to see which actually works for your restaurant.

### Problem: Food costs creeping up without price adjustments
Cause: Ingredient prices in Israel fluctuate frequently, especially produce, dairy, and meat.
Solution: Re-cost your top 10 selling items monthly using the template in Step 5. Set calendar reminders to review prices quarterly. If a key ingredient rises more than 10%, adjust menu prices within a week.
