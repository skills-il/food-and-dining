# Delivery Platform Integration Guides

> **How to read this file.** All three merchant portals sit behind a login, and none of
> the platforms publishes its merchant terms, commission rates, settlement dates or portal
> specifications. Everything below is a practitioner-level orientation to what these portals
> generally look like, gathered from restaurateurs, **not** documentation and not verified
> against any published source. Treat every number here as something to CONFIRM in the
> restaurant's own contract and portal before acting on it, and say so when you repeat it
> to an owner. Where this file and the restaurant's contract disagree, the contract wins.

## Wolt Israel - Restaurant Portal

- **Merchant portal:** reached from the Wolt for Restaurants page (https://explore.wolt.com/en/isr/merchant/business/restaurants). Wolt does not publish a stable standalone merchant-portal hostname, so use the link in your onboarding email rather than guessing a subdomain
- **Login:** as provisioned during onboarding.
- **Menu Management:**
  - Structured into categories (starters, mains, desserts, drinks)
  - Supports modifier groups (size, extras, toppings) per item
  - Photos per item; the portal states the current minimum resolution at upload
  - Price in NIS, including VAT
  - Preparation time set per item or per category
- **Order Dashboard:**
  - Real-time order feed with accept/reject workflow
  - Estimated pickup time shown to couriers
  - Order history with full details and delivery status
- **Analytics:**
  - Revenue reports (daily, weekly, monthly)
  - Order volume trends and peak hours
  - Customer review summary with response option
- **Commission:** indicatively around 25-35% of order value, negotiated per restaurant. Confirm against the signed contract
- **Payment Cycle:** typically weekly bank transfer. Confirm the day and the cut-off in the contract
- **Review Responses:** available directly from the portal, with a character limit and a moderation delay. Check both in the portal rather than assuming a figure.

## 10bis (תן ביס) - Restaurant Dashboard

- **Merchant portal:** reached from https://www.10bis.co.il/ under the restaurant/business section, or from the link in your onboarding email. There is no separate published merchant hostname
- **Login:** as provisioned during onboarding.
- **Menu Management:**
  - Simpler flat structure - categories and items
  - More limited modifier support than Wolt; check the current per-item limit in the portal
  - Photos optional but recommended
  - Price in NIS, including VAT
  - No per-item preparation time (set globally for restaurant)
- **Order Flow:**
  - Orders appear in the dashboard for accept/reject. Confirm whether unactioned orders auto-accept, and after how long, since this determines whether an unattended tablet costs you an order or commits you to one
  - Print integration available for kitchen ticket printers
  - Order status updates: accepted, ready for pickup
- **Analytics:**
  - Monthly revenue summary
  - Order count by day
  - Basic customer satisfaction score
- **Commission:** indicatively around 10-15% of order value, varying by plan; older public reporting cites 7-12%. Confirm against the signed contract
- **Payment Cycle:** typically monthly bank transfer. Confirm the date in the contract
- **Review Responses:** available via the dashboard. Check the character limit and whether responses publish immediately.

## Mishlocha (משלוחה) - Partner Portal

- **Merchant portal:** reached from the official site https://www.mishloha.co.il/ (the name is sometimes transliterated "Mishlocha"). There is no separate published partner hostname; use the link your account manager supplies
- **Login:** as provisioned by your account manager.
- **Menu Management:**
  - Category-based menu structure
  - Supports combo/meal deals as special items
  - Photo upload per item
  - Price in NIS, including VAT
  - Preparation time set per restaurant
- **Order Management:**
  - Real-time order notifications via portal and optional SMS
  - Manual accept/reject per order
  - Delivery tracking integration
- **Analytics:**
  - Revenue reports by period
  - Order trends and popular items
  - Delivery performance metrics
- **Commission:** indicatively around 15-25% of order value, contract-dependent. Confirm against the signed contract
- **Payment Cycle:** typically bi-weekly bank transfer. Confirm the dates in the contract
- **Review Responses:** Available via portal. Character limit: 400. Moderation delay: up to 48 hours.

## Common Integration Patterns

### Browser Automation (CDP) Tips
- Use headless Chromium with CDP for portal access
- Store session cookies to avoid re-authentication on every run
- Handle rate limiting: wait 2-3 seconds between page navigations
- Monitor for portal UI changes - selectors may break after platform updates
- Set viewport to desktop size (1280x800 minimum) to avoid mobile layouts

### Hebrew Encoding
- All portals expect UTF-8 for Hebrew text
- When syncing menus, normalize Unicode (NFC form) before comparing
- Some portals strip RTL markers - avoid relying on directional characters

### Error Recovery
- On login failure: clear cookies, retry with fresh session
- On menu sync timeout: retry individual failed items (not the full batch)
- On order polling failure: log the error, continue polling next cycle
- Keep a local cache of last known state to detect drift

## Review Response Guidelines

### General Principles
- Respond in Hebrew (the language customers expect)
- Keep responses concise: 2-4 sentences
- Always acknowledge the specific issue raised
- Offer a concrete resolution (not just an apology)
- Include a phone number or direct contact method
- Never argue or be defensive

### Platform-Specific Notes
- **Wolt:** Responses visible to all users. Keep professional tone. 500 char limit.
- **10bis:** Responses visible to reviewer only. Can be more personal. No limit.
- **Mishlocha:** Responses visible to all users. 400 char limit. Moderation may take 48h.

---

## Licensing notes (fuller detail)

SKILL.md carries the summary. The companion skill `israeli-food-business-compliance` is the
authority on licensing routes, fees and validity periods; this section exists only so the
delivery-specific hooks are written down somewhere.

**חוק רישוי עסקים, התשכ"ח-1968 + צו רישוי עסקים (עסקים טעוני רישוי)**

| Item | Covers |
|------|--------|
| 4.2א | מסעדה, expressly "לרבות משלוח מזון", including alcohol served on the premises |
| 4.2ב | בית קפה, מזנון or another בית אוכל, also "לרבות משלוח מזון" |
| 4.2ג | Preparing food for sale and consumption off the premises, "לרבות משלוח מזון". This is the delivery-only / cloud-kitchen row |

- **§14(ד)** makes an offence under §14 one of strict liability: there is no "we did not realise" defence.
- **§14א2** applies the same 18-month exposure to false particulars in a licence declaration, which
  matters precisely because the declaration route (מסלול תצהיר) is the fast one.
- **§16 and §17** let a court order the business's operation stopped or the premises closed.
- **§20** allows an administrative stop order, issuable by the head of the local authority or by the
  National Food Service director together with the district physician.
- **§8ב(ב)** bars the licensing authority from granting a licence to a public-facing business
  without accessibility compliance and the accessibility experts' opinions.

**Manufacturing licence, חוק הגנה על בריאות הציבור (מזון), התשע"ו-2015 §25**

§25(א) exempts food prepared in a בית אוכל from a רישיון ייצור only while no more than 30% of it,
on a weekly average, is intended for supply to bodies other than that establishment's diners.
Deliveries to end customers are supply to diners and are outside the count. §25(ב) frames a
בית אוכל as a business whose food is generally intended to be eaten on the premises, which is why a
delivery-only kitchen should put its own position to the licensing authority rather than assume it.
