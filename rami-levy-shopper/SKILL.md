---
name: rami-levy-shopper
description: Use the unofficial Rami Levy CLI as a careful shopping assistant for a signed-in Rami Levy account. Use when the user asks to search or compare Rami Levy products, inspect current prices or promotions, view previous orders, check the live cart, or add, update, or remove cart items, including requests such as "what is in my cart?" or "הוסף לעגלה". Supports live server-cart reads, unit-price comparison, safe verified mutations, and private browser sign-in. Do NOT use for cross-chain supermarket comparison or raw Price Transparency feeds; use israeli-grocery-price-intelligence instead.
license: MIT
compatibility: Requires the rami CLI, Node.js 20 or newer, npm, and Google Chrome for sign-in.
metadata:
  author: bornio
  version: 1.0.0
  category: food-and-dining
---

# Rami Levy Shopper

Use the open-source [`rami` CLI](https://github.com/bornio/rami-levy-cli)
on the shopper's behalf. Keep the conversation focused on the shopping decision
and result, not the CLI implementation.

This is an unofficial community project and is not affiliated with or supported
by Rami Levy. Use it only with the shopper's own account and in accordance with
Rami Levy's terms.

## Instructions

### Step 1: Verify the CLI and authentication

Run `rami --version`. If the command is unavailable, follow the upstream
[installation instructions](https://github.com/bornio/rami-levy-cli#install--about-2-minutes).
Do not improvise direct calls to Rami Levy's private website APIs.

If an operation reports missing or expired authentication, run:

```sh
rami auth login
```

Let the shopper enter credentials and verification codes in the real Chrome
page. Never request credentials in chat. Prefer browser login; treat
`rami auth import <file.har>` as a sensitive manual fallback only.

### Step 2: Read current shopping data

Run read-only requests directly when the shopper asks:

```sh
rami cart
rami search "search terms"
rami search "search terms" --sort price
rami search "search terms" --sort unit-price
rami orders
```

Use `rami --help` or `rami help <command>` for current syntax. Prefer normal
output when showing results. Add `--json` when exact fields are needed for
reasoning, then summarize rather than dumping JSON unless requested.

Treat every cart command as live: it fetches the server cart and recalculates
current pricing. Never answer from a saved cart output when current state
matters.

### Step 3: Select and compare products

- Prefer available products, then the shopper's requested price, package, or
  brand criteria.
- Identify a product by name, package size or content, price, and product ID.
- If multiple products plausibly match, show a short list of the best matches
  and ask one concise selection question.
- Do not assume search results contain the complete catalog; Rami Levy may
  return fewer results than its reported match count.
- Use `--sort unit-price` for value by weight, volume, or count, but compare only
  compatible measurement families and inspect the package content. Rami Levy's
  unit metadata may be missing or wrong, so never present the ranking as
  unquestionable.
- Distinguish regular price, current cart price, savings, delivery quote, and
  conditional promotion text.
- Treat a promotion price as effective only when the server confirms that the
  current cart quantity qualifies. Do not assume adding one more unit has the
  same average price.
- Describe displayed totals as the latest quote, not a guaranteed checkout
  charge.

### Step 4: Change the cart safely

Resolve the exact product ID and quantity before changing the cart. Perform an
explicit, unambiguous request without asking for redundant confirmation; ask
one concise question if the product, variant, or quantity is ambiguous.

```sh
rami cart add <product-id> [quantity]
rami cart update <product-id> <quantity>
rami cart remove <product-id>
```

- Use `add` to increase the existing quantity; it does not set an absolute
  quantity.
- Use `update` to set the absolute quantity.
- Use `remove` to remove an item. Never substitute a zero quantity.
- Never empty the cart or remove unrelated items unless explicitly requested.
- Preserve product IDs exactly, including leading zeroes.
- Use only positive quantities with at most two decimal places.

After success, report the verified product name, resulting quantity,
availability, current line price, applied savings, and updated
available-products total when present.

If a mutation reports an error or says that the update was saved but details
could not be loaded, do not retry it. First run `rami cart` to discover the
authoritative result; retrying `add` could duplicate the quantity.

### Step 5: Protect shopper data and stay in scope

- Never display, inspect, copy, or commit stored profiles, tokens, cookies, or
  HAR contents.
- Use the default authenticated profile unless the shopper explicitly selects
  another one.
- Do not modify the CLI source code to complete a shopping request.
- Do not claim to place or complete an order. The CLI manages search, past
  orders, and the cart; final checkout remains on the Rami Levy website.

## Examples

### Example 1: Show the current cart

User says: "What is in my Rami Levy cart?"

Run `rami cart`. Return the available items first, note unavailable products,
show applied savings, and include the available-products total. State that the
amount is the latest quote and excludes delivery unless shown separately.

### Example 2: Find the best-value soda

User says: "Find the cheapest soda by liter at Rami Levy."

Run `rami search "סודה" --sort unit-price`. Compare only products with
compatible volume metadata. Show availability, package volume, current price,
and unit price, and briefly warn that package metadata should be checked.

### Example 3: Add an ambiguous product

User says: "Add two bottles of Mei Eden soda."

Search for `מי עדן סודה`. If bottle sizes or variants differ, show the best
matches and ask which one. Once resolved, run `rami cart add <product-id> 2` and
report the server-verified resulting quantity and current price.

## Troubleshooting

### Error: `rami: command not found`

Cause: The CLI is not installed or linked on the machine.

Solution: Follow the upstream installation instructions, then rerun
`rami --version`. Do not replace the CLI with ad hoc API requests.

### Error: Authentication is missing or expired

Cause: The saved reduced browser credentials are absent or no longer valid.

Solution: Run `rami auth login` and let the shopper finish sign-in in Chrome.
Never ask them to paste credentials or tokens into chat.

### Error: A cart mutation failed or its result is uncertain

Cause: The server may have accepted the write before a later pricing or network
request failed.

Solution: Run `rami cart` before considering any retry. Compare the live
quantity with the requested result, then explain the observed state.

### Error: Search results are ambiguous or unit metadata is missing

Cause: Product names, package variants, or Rami Levy metadata do not uniquely
identify a safe choice.

Solution: Present the small set of plausible products with their IDs, sizes,
availability, and prices. Ask the shopper to choose; do not guess.
