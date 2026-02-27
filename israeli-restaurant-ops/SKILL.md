---
name: israeli-restaurant-ops
description: >-
  Manage Israeli restaurant operations across delivery platforms — Wolt, 10bis,
  and Mishlocha. Use when user asks about "restaurant management Israel",
  "Wolt integration", "10bis", "Mishlocha", "food delivery platform",
  "menu sync", "restaurant orders", "delivery commission", or "ניהול מסעדה".
  Covers menu synchronization, order monitoring, revenue tracking with
  commission breakdowns, review management, and delivery performance analytics.
  Do NOT use for cooking recipes, personal meal planning, or non-Israeli
  delivery platforms.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: >-
  Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for real-time
  order monitoring, scheduled revenue reports, and review alert notifications.
metadata:
  author: skills-il
  version: 1.0.0
  category: food-and-dining
  tags:
    he:
      - מסעדה
      - משלוח-מזון
      - Wolt
      - תן-ביס
      - משלוחה
      - ישראל
    en:
      - restaurant
      - food-delivery
      - wolt
      - 10bis
      - mishlocha
      - israel
  display_name:
    he: ניהול תפעול מסעדה ישראלית
    en: Israeli Restaurant Operations
  display_description:
    he: ניהול תפעול יומיומי למסעדות ישראליות מול פלטפורמות משלוח — וולט, תן ביס ומשלוחה
    en: >-
      Manage Israeli restaurant operations across delivery platforms — Wolt,
      10bis, and Mishlocha.
  openclaw:
    requires:
      bins: []
      env: []
    emoji: "🍽️"
---

# Israeli Restaurant Operations

## Instructions

### Step 1: Connect Delivery Platforms
Set up connections to Israeli delivery platforms via browser automation (CDP):
- **Wolt Israel** (wolt.com) — Restaurant Portal access for menu, orders, analytics
- **10bis (תן ביס)** (10bis.co.il) — Restaurant dashboard for orders and menu management
- **Mishlocha (משלוחה)** (mishlocha.co.il) — Partner portal for orders and menu updates

For each platform:
1. Navigate to restaurant portal/dashboard
2. Authenticate with stored credentials (handle 2FA if required)
3. Verify restaurant profile and operating hours are current
4. Test order notification flow

Store platform credentials securely. If persistent memory is unavailable, export config as `restaurant-config.json`.

### Step 2: Sync Menus Across Platforms
Maintain consistent menus across all delivery platforms:
- Create a master menu in Hebrew (main source of truth)
- Fields per item: name (Hebrew), description (Hebrew), price (NIS), category, photo, availability, preparation time
- Sync changes to all connected platforms:
  - Price update — push to Wolt, 10bis, Mishlocha simultaneously
  - Item unavailable — mark as sold out across all platforms
  - New item — add to all platforms with photo and description
- Handle platform-specific requirements:
  - Wolt: structured menu categories, modifier groups
  - 10bis: simpler menu structure, limited modifiers
  - Mishlocha: category-based menu with combo support

### Step 3: Set Up Order Monitoring
Configure real-time order tracking across platforms:
- Poll each platform for new orders every 1-2 minutes
- Send WhatsApp/Telegram alert to kitchen staff for each new order
- Alert format: `[Platform] הזמנה חדשה #[ID]: [items] - [time estimate]`
- Track order lifecycle: received — preparing — ready — picked up — delivered
- Alert on anomalies: order not picked up within 30 min, delivery taking too long
- End-of-day order summary via WhatsApp

### Step 4: Configure Revenue Tracking
Track revenue with per-platform commission breakdowns:

| Platform | Commission Range | Payment Cycle |
|----------|-----------------|---------------|
| Wolt | 25-35% of order value | Weekly bank transfer |
| 10bis | 10-15% (varies by plan) | Monthly |
| Mishlocha | 15-25% | Bi-weekly |

For each order track:
- Gross order value (what customer paid including VAT)
- Platform commission (%)
- Net revenue (what restaurant receives)
- Delivery fee (paid by customer or restaurant, varies)
- VAT component (17%)

Generate daily/weekly/monthly reports:
- Total orders by platform
- Gross vs net revenue comparison
- Commission costs by platform
- Average order value by platform
- Peak hours analysis

### Step 5: Set Up Review Monitoring
Monitor customer reviews across all platforms:
- Check for new reviews every 4 hours
- Alert immediately on negative reviews (3 stars or below)
- For negative reviews, draft a professional Hebrew response:
  - Acknowledge the issue
  - Apologize sincerely
  - Offer resolution (discount, free item on next order)
  - Invite the customer to contact directly
- Track review trends: average rating, common complaints, improvement over time
- Weekly review summary report

Response template for negative review:
`"שלום [שם], תודה שהקדשת זמן לשתף אותנו. אנחנו מצטערים לשמוע על [הבעיה]. אנחנו לוקחים את זה ברצינות ונשמח להזמין אותך שוב על חשבוננו. צרו קשר ב-[PHONE] ונשמח לתקן את הרושם."`

### Step 6: Generate Performance Reports
Create comprehensive performance reports delivered via WhatsApp:

Daily report (auto-sent at closing time):
- Total orders (by platform)
- Total revenue (gross/net)
- Average preparation time
- Any delivery issues or complaints

Weekly report:
- Week-over-week comparison
- Best/worst performing items
- Commission costs total
- Review summary

Monthly report:
- Revenue trends
- Platform performance comparison
- Top items by revenue
- Suggested menu optimizations based on data

## Examples

### Example 1: New Restaurant Onboarding Across 3 Platforms
User says: "I just opened a restaurant in Tel Aviv and I need to manage my Wolt, 10bis, and Mishlocha accounts"
Actions:
1. Connect to each platform's restaurant portal via browser automation
2. Import existing menu from the first platform as master
3. Sync master menu to the other two platforms
4. Configure order monitoring with WhatsApp alerts for kitchen staff
5. Set up revenue tracking with commission rates per platform
6. Enable review monitoring with negative review alerts
Result: Restaurant fully connected to all 3 platforms. Master menu synced, order alerts configured, revenue tracking active. First daily report scheduled for tonight at closing time.

### Example 2: Updating Menu Prices After Supplier Cost Increase
User says: "My meat supplier raised prices 15%, I need to update all meat dishes across platforms"
Actions:
1. Identify all meat-based items in master menu
2. Calculate new prices (15% increase, rounded to nearest 1 NIS)
3. Preview changes before applying
4. Push updated prices to Wolt, 10bis, and Mishlocha simultaneously
5. Verify updates on each platform
Result: 12 menu items updated across all 3 platforms. Average price increase: 14 NIS per item. Changes are live within 5 minutes.

### Example 3: Handling Negative Wolt Review with Hebrew Response
User says: "I got a 2-star review on Wolt saying the food arrived cold"
Actions:
1. Pull the review details (customer name, order ID, items)
2. Check delivery timing for that order
3. Draft Hebrew response acknowledging the issue
4. Present response for owner approval
5. Post response on Wolt
6. Flag the delivery timing issue for the weekly report
Result: Professional Hebrew response posted: "שלום [שם], מצטערים מאוד שהמנה הגיעה קרה. בדקנו ומצאנו שהיה עיכוב באיסוף. נשמח להזמין אותך שוב על חשבוננו — צרו קשר ב-03-XXX-XXXX."

## Bundled Resources

### References
- `references/platform-guides.md` — Integration guides for Wolt Israel, 10bis, and Mishlocha restaurant portals. Covers portal URLs, login methods, menu management features, order tracking, and analytics dashboards. Consult when connecting to a specific platform in Step 1 or syncing menus in Step 2.

## Troubleshooting

### Error: "Platform portal login failed"
Cause: Delivery platforms frequently update their portal interfaces and may require 2FA.
Solution: Check if the platform requires SMS/email OTP. Configure browser automation to pause for 2FA input. Verify credentials are current. See references/platform-guides.md for portal-specific notes.

### Error: "Menu sync failed — item not found on platform"
Cause: Menu item names or categories don't match between master menu and the platform.
Solution: Check for Hebrew encoding issues. Verify the item exists on the target platform. Some platforms have category restrictions — check if the item needs to be in a specific category first.

### Error: "Commission calculation mismatch"
Cause: Commission rates vary by contract, promotional periods, and order type (delivery vs pickup).
Solution: Verify contract commission rates with each platform. Check for promotional commission periods. Note that delivery orders and pickup orders may have different commission rates.

### Error: "Review response not posted"
Cause: Some platforms have response character limits or moderation delays.
Solution: Ensure response is within platform's character limit (typically 500 chars). Response may be in moderation queue — check back after 24 hours. Some platforms require verified restaurant accounts for review responses.
