#!/usr/bin/env python3
"""Parse Israeli supermarket XML price feeds into normalized JSON.

Supports feeds published under the Price Transparency Law (חוק שקיפות מחירים).
Handles gzipped XML files and various chain-specific format differences.

Usage:
    python parse_price_xml.py --chain shufersal --input PriceFull.xml.gz --output prices.json
    python parse_price_xml.py --chain rami-levy --input PriceFull.xml --output prices.json
    python parse_price_xml.py --help
"""

import argparse
import codecs
import gzip
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Two XML dialects exist in the wild. Verified against live feeds on 2026-08-27.
#
#   "standard"  -- Cerberus chains (Rami Levy, Yochananof, Tiv Taam, Dor Alon, ...)
#                  ChainId / ItemName / ManufacturerName / PriceUpdateDate
#   "shufersal" -- Shufersal Direct and Carrefour Israel Direct
#                  ChainID / ItemName / ManufactureName / PriceUpdateTime
#
# The dialect is NOT predictable from the chain name alone: chains migrate between
# publishing platforms. Always detect it from the document (see detect_dialect).
DIALECT_FIELD_MAP = {
    "standard": {
        "item_code": "ItemCode",
        "item_name": "ItemName",
        "manufacturer": "ManufacturerName",
        "price": "ItemPrice",
        "unit_price": "UnitOfMeasurePrice",
        "quantity": "Quantity",
        "unit_of_measure": "UnitOfMeasure",
        "update_date": "PriceUpdateDate",
        "is_weighted": "bIsWeighted",
    },
    "shufersal": {
        "item_code": "ItemCode",
        "item_name": "ItemName",
        "manufacturer": "ManufactureName",
        "price": "ItemPrice",
        "unit_price": "UnitOfMeasurePrice",
        "quantity": "Quantity",
        "unit_of_measure": "UnitOfMeasure",
        "update_date": "PriceUpdateTime",
        "is_weighted": "bIsWeighted",
    },
}

# Tags whose presence identifies the shufersal-style dialect.
_SHUFERSAL_MARKERS = ("ManufactureName", "PriceUpdateTime", "LastSaleDateTime")

SUPPORTED_CHAINS = [
    "shufersal",
    "rami-levy",
    "yochananof",
    "victory",
    "osher-ad",
    "carrefour-israel",
    "tiv-taam",
]


GZIP_MAGIC = b"\x1f\x8b"


def read_xml(input_path: str) -> ET.Element:
    """Read XML from a plain or gzipped file, handling encoding issues.

    Decides gzip by MAGIC BYTES, not by filename: both documented failure modes
    (a Cerberus redirect stub, an expired Shufersal signed URL) return a body
    whose name ends .gz but which is not gzip.
    """
    path = Path(input_path)
    if not path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw = path.read_bytes()

    if raw[:2] == GZIP_MAGIC:
        try:
            raw = gzip.decompress(raw)
        except OSError as exc:
            print(f"Error: file looks gzipped but could not be decompressed: {exc}", file=sys.stderr)
            sys.exit(1)
    elif path.name.endswith(".gz"):
        head = raw[:200].decode("utf-8", "replace").strip()
        print(
            "Error: filename ends .gz but the body is not gzip. This is usually a "
            "Cerberus redirect stub (you are not logged in) or an expired Shufersal "
            f"signed URL. First bytes: {head!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Stores files are frequently UTF-16 with a BOM and NO XML declaration
    # (verified on a live Carrefour Stores file). Handle BOMs explicitly.
    for bom, encoding in (
        (codecs.BOM_UTF8, "utf-8-sig"),
        (codecs.BOM_UTF16_LE, "utf-16"),
        (codecs.BOM_UTF16_BE, "utf-16"),
    ):
        if raw.startswith(bom):
            text = raw.decode(encoding)
            return ET.fromstring(_strip_declaration(text))

    for encoding in ("utf-8", "utf-16", "windows-1255", "iso-8859-8"):
        try:
            text = raw.decode(encoding)
        except (UnicodeDecodeError, UnicodeError):
            continue
        try:
            return ET.fromstring(_strip_declaration(text))
        except ET.ParseError:
            continue

    # Last resort: hand ET the raw bytes so it can honour the declaration itself.
    try:
        return ET.fromstring(raw)
    except ET.ParseError as exc:
        print(f"Error: Could not parse XML with any supported encoding: {exc}", file=sys.stderr)
        sys.exit(1)


def _strip_declaration(text: str) -> str:
    """Drop the XML declaration so a decoded str never conflicts with it."""
    text = text.lstrip("\ufeff")
    if text.startswith("<?xml"):
        text = text[text.index("?>") + 2 :]
    return text.lstrip()


def detect_dialect(root: ET.Element) -> str:
    """Detect which XML dialect this feed uses by inspecting the tags present.

    Chain names are unreliable (chains move between publishing platforms), so the
    document itself is the only trustworthy signal.
    """
    # The root tag casing is the reliable discriminator and is always present:
    # Cerberus uses <ChainId>, Shufersal/Carrefour use <ChainID>.
    root_tags = {child.tag for child in root}
    if "ChainID" in root_tags:
        return "shufersal"
    if "ChainId" in root_tags:
        return "standard"
    # Fall back to item-level markers if the root is unusual.
    present = {node.tag for node in root.iter()}
    if present & set(_SHUFERSAL_MARKERS):
        return "shufersal"
    return "standard"


def get_field_map(dialect: str) -> dict:
    """Get the field mapping for a detected dialect."""
    return DIALECT_FIELD_MAP.get(dialect, DIALECT_FIELD_MAP["standard"])


def extract_text(element: ET.Element, tag: str) -> str:
    """Safely extract text from an XML child element."""
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return ""


KG_UNITS = {'ק"ג', "קג", "1קילוגרם", "קילוגרם", "קילו", "kg", "1 ק\"ג"}


def parse_header(root: ET.Element) -> dict:
    """Extract the chain/sub-chain/store identity every feed file carries.

    Feeds are published ONE FILE PER STORE, so without these a merged dataset
    has no dedup key and cannot be joined to the Stores feed.
    """
    def first(*tags):
        for tag in tags:
            node = root.find(tag)
            if node is not None and node.text:
                return node.text.strip()
        return ""

    return {
        "chain_id": first("ChainId", "ChainID"),
        "sub_chain_id": first("SubChainId", "SubChainID"),
        "store_id": first("StoreId", "StoreID"),
    }


def parse_promotions(root: ET.Element, dialect: str) -> list[dict]:
    """Parse PromoFull promotions from either dialect.

    The dialects differ structurally: Cerberus puts RewardType/MinQty on the
    <Promotion>, Shufersal/Carrefour put them on each PromotionItem inside
    Groups/Group. Club id is a nested integer on Cerberus and a flat
    "<code> - <label>" string on Shufersal.
    """
    promotions = []
    for promo in root.findall(".//Promotion"):
        club_raw = extract_text(promo, "ClubID") or extract_text(promo, "Clubs/ClubId")
        club_code = _leading_int(club_raw)
        entry = {
            "promotion_id": extract_text(promo, "PromotionId") or extract_text(promo, "PromotionID"),
            "description": extract_text(promo, "PromotionDescription"),
            "club_id_raw": club_raw,
            "club_id": club_code,
            "club_only": club_code is not None and club_code != 0,
            "start": extract_text(promo, "PromotionStartDate") or extract_text(promo, "PromotionStartDateTime"),
            "end": extract_text(promo, "PromotionEndDate") or extract_text(promo, "PromotionEndDateTime"),
            "start_hour": extract_text(promo, "PromotionStartHour"),
            "end_hour": extract_text(promo, "PromotionEndHour"),
            "promotion_days": extract_text(promo, "PromotionDays"),
            "items": [],
        }

        if dialect == "shufersal":
            for group in promo.findall("Groups/Group"):
                min_purchase = extract_text(group, "MinPurchaseAmount")
                for pit in group.findall("PromotionItems/PromotionItem"):
                    entry["items"].append({
                        "item_code": extract_text(pit, "ItemCode"),
                        "reward_type": extract_text(pit, "RewardType"),
                        "min_qty": extract_text(pit, "MinQty"),
                        "max_qty": extract_text(pit, "MaxQty"),
                        "discount_rate": extract_text(pit, "DiscountRate"),
                        "min_purchase_amount": min_purchase,
                    })
        else:
            shared = {
                "reward_type": extract_text(promo, "RewardType"),
                "min_qty": extract_text(promo, "MinQty"),
                "max_qty": extract_text(promo, "MaxQty"),
                "discounted_price": extract_text(promo, "DiscountedPrice"),
                "discount_rate": extract_text(promo, "DiscountRate"),
                "min_purchase_amount": extract_text(promo, "MinPurchaseAmnt"),
            }
            for item in promo.findall("PromotionItems/Item"):
                entry["items"].append({"item_code": extract_text(item, "ItemCode"),
                                       "is_gift": extract_text(item, "IsGiftItem") == "1",
                                       **shared})
            if not entry["items"]:
                entry["items"].append(shared)
        promotions.append(entry)
    return promotions


def _leading_int(value: str):
    """Parse the leading integer of a club id.

    Cerberus gives a bare integer; Shufersal gives "0 - כלל הלקוחות". Comparing
    the Shufersal string to 0 is always unequal, which would mark every
    promotion club-only.
    """
    if not value:
        return None
    token = value.strip().split()[0].split("-")[0].strip()
    try:
        return int(token)
    except ValueError:
        return None


def parse_items(root: ET.Element, chain: str, dialect: str) -> list[dict]:
    """Parse item elements from the XML tree into normalized dicts."""
    field_map = get_field_map(dialect)
    items = []

    # A PromoFull carries <Item> stubs inside each promotion (ItemCode/IsGiftItem
    # only). Parsing those as products yields a phantom catalogue of nameless
    # rows, so only read products from a price document.
    if root.find(".//Promotions") is not None and root.find(".//Items") is None:
        return items

    # Prefer the real product container; fall back to a bare scan.
    item_elements = root.findall("./Items/Item") or root.findall(".//Items/Item")
    if not item_elements:
        item_elements = root.findall(".//Item")
    if not item_elements:
        item_elements = root.findall(".//Product")
    if not item_elements:
        item_elements = root.findall(".//{*}Item")

    for item_el in item_elements:
        price_str = extract_text(item_el, field_map["price"])
        unit_price_str = extract_text(item_el, field_map["unit_price"])

        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            price = 0.0

        try:
            unit_price = float(unit_price_str) if unit_price_str else 0.0
        except ValueError:
            unit_price = 0.0

        is_weighted = extract_text(item_el, field_map["is_weighted"]) == "1"

        # Weighted items: ItemPrice is per the item's declared UnitOfMeasure,
        # which is normally kilograms but is NOT guaranteed to be. Only assert
        # price_per_kg when the unit is recognisably kg; otherwise leave it None
        # and let the caller normalise, rather than emitting a wrong number
        # under a name that invites downstream code to trust it.
        unit_of_measure = extract_text(item_el, field_map["unit_of_measure"])
        unit_is_kg = unit_of_measure.replace(" ", "") in {u.replace(" ", "") for u in KG_UNITS}
        price_per_kg = price if (is_weighted and unit_is_kg) else None

        normalized = {
            "item_code": extract_text(item_el, field_map["item_code"]),
            "item_name": extract_text(item_el, field_map["item_name"]),
            "manufacturer": extract_text(item_el, field_map["manufacturer"]),
            "price": price,
            "unit_price": unit_price,
            "price_per_kg": price_per_kg,
            "quantity": extract_text(item_el, field_map["quantity"]),
            "unit_of_measure": unit_of_measure,
            "item_status": extract_text(item_el, "ItemStatus"),
            "update_date": extract_text(item_el, field_map["update_date"]),
            "is_weighted": is_weighted,
            "chain": chain,
            "dialect": dialect,
        }
        items.append(normalized)

    return items


def main():
    parser = argparse.ArgumentParser(
        description="Parse Israeli supermarket XML price feeds into normalized JSON."
    )
    parser.add_argument(
        "--chain",
        required=True,
        help=(
            "Supermarket chain name, recorded in the output for provenance. Any chain "
            "is accepted: the field mapping is auto-detected from the file, so this is "
            "a label, not a switch. Known chains: " + ", ".join(SUPPORTED_CHAINS)
        ),
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to XML or gzipped XML price feed file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path (default: stdout)",
    )

    args = parser.parse_args()

    root = read_xml(args.input)
    dialect = detect_dialect(root)
    header = parse_header(root)
    items = parse_items(root, args.chain, dialect)
    promotions = parse_promotions(root, dialect)

    blank_names = sum(1 for i in items if not i["item_name"])
    if items and blank_names == len(items):
        print(
            "Warning: every item_name is empty. The feed's schema may have changed; "
            "re-check the tag names against the live file before trusting this output.",
            file=sys.stderr,
        )

    result = {
        "chain": args.chain,
        "dialect": dialect,
        **header,
        "item_count": len(items),
        "promotion_count": len(promotions),
        "items": items,
        "promotions": promotions,
    }

    if not items and not promotions:
        print(
            "Warning: no items and no promotions found. Check the file is the type "
            "you expected (PriceFull vs PromoFull vs Stores).",
            file=sys.stderr,
        )

    json_output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output, encoding="utf-8")
        print(f"Wrote {len(items)} items to {args.output}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == "__main__":
    main()
