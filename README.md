# Food & Dining Skills

AI agent skills for Israeli food industry, restaurant operations, grocery prices, and food business compliance.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [israeli-food-business-compliance](./israeli-food-business-compliance/) | Israeli food business regulatory compliance — licensing, kashrut certification, health ministry requirements, and food labeling | -- | `health-ministry-requirements.md`, `labeling-requirements.md` |
| [israeli-grocery-price-intelligence](./israeli-grocery-price-intelligence/) | Access and compare Israeli supermarket prices using mandatory Price Transparency Law data feeds | `parse_price_xml.py` | `chain-feeds.md` |
| [israeli-restaurant-ops](./israeli-restaurant-ops/) | Manage Israeli restaurant operations across delivery platforms — Wolt, 10bis, and Mishlocha | -- | `platform-guides.md` |

## Install

```bash
# Claude Code - install a specific skill
claude install github:skills-il/food-and-dining/israeli-restaurant-ops

# Or clone the full repo
git clone https://github.com/skills-il/food-and-dining.git
```

## Structure

```
food-and-dining/
├── israeli-food-business-compliance/   # Food business licensing and compliance
│   ├── SKILL.md
│   ├── SKILL_HE.md
│   └── references/
├── israeli-grocery-price-intelligence/ # Supermarket price comparison
│   ├── SKILL.md
│   ├── SKILL_HE.md
│   ├── scripts/
│   └── references/
├── israeli-restaurant-ops/             # Restaurant delivery platform management
│   ├── SKILL.md
│   ├── SKILL_HE.md
│   └── references/
├── scripts/validate-skill.sh
├── CLAUDE.md
├── LICENSE
└── README.md
```

## Contributing

See the org-level [Contributing Guide](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md).

## License

MIT

---

Built with care in Israel.
