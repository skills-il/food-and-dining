# Delivery Platform Integration Guides

## Wolt Israel — Restaurant Portal

- **Portal URL:** https://restaurant-portal.wolt.com
- **Login:** Email + password. Some accounts require SMS-based 2FA.
- **Menu Management:**
  - Structured into categories (starters, mains, desserts, drinks)
  - Supports modifier groups (size, extras, toppings) per item
  - Photos required per item (minimum 800x600 resolution)
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
- **Commission:** 25-35% of order value (negotiable based on volume)
- **Payment Cycle:** Weekly bank transfer (Thursday for previous week)
- **Review Responses:** Available directly from portal. Character limit: 500. Moderation delay: up to 24 hours.

## 10bis (תן ביס) — Restaurant Dashboard

- **Portal URL:** https://restaurant.10bis.co.il
- **Login:** Business phone number + SMS OTP (no password-based login).
- **Menu Management:**
  - Simpler flat structure — categories and items
  - Limited modifier support (up to 3 modifier groups per item)
  - Photos optional but recommended
  - Price in NIS, including VAT
  - No per-item preparation time (set globally for restaurant)
- **Order Flow:**
  - Orders appear in dashboard; auto-accepted after 5 minutes if not rejected
  - Print integration available for kitchen ticket printers
  - Order status updates: accepted, ready for pickup
- **Analytics:**
  - Monthly revenue summary
  - Order count by day
  - Basic customer satisfaction score
- **Commission:** 10-15% of order value (varies by subscription plan)
- **Payment Cycle:** Monthly bank transfer (15th of following month)
- **Review Responses:** Available via dashboard. No character limit. Published immediately.

## Mishlocha (משלוחה) — Partner Portal

- **Portal URL:** https://partner.mishlocha.co.il
- **Login:** Email + password. Optional 2FA via authenticator app.
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
- **Commission:** 15-25% of order value (contract-dependent)
- **Payment Cycle:** Bi-weekly bank transfer (1st and 15th of month)
- **Review Responses:** Available via portal. Character limit: 400. Moderation delay: up to 48 hours.

## Common Integration Patterns

### Browser Automation (CDP) Tips
- Use headless Chromium with CDP for portal access
- Store session cookies to avoid re-authentication on every run
- Handle rate limiting: wait 2-3 seconds between page navigations
- Monitor for portal UI changes — selectors may break after platform updates
- Set viewport to desktop size (1280x800 minimum) to avoid mobile layouts

### Hebrew Encoding
- All portals expect UTF-8 for Hebrew text
- When syncing menus, normalize Unicode (NFC form) before comparing
- Some portals strip RTL markers — avoid relying on directional characters

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
