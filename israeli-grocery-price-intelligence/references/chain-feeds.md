# Israeli Supermarket Chain Price Feeds

## Overview

Under the Price Transparency Law (חוק שקיפות מחירים, 2015), supermarket chains with 3 or more stores must publish product prices as machine-readable XML files. Data must be updated daily.

## Feed Types

All chains publish three categories of data files:

| File Type | Content | Update Frequency |
|-----------|---------|-----------------|
| PricesFull | Complete product catalog with current prices | Daily (overnight) |
| PricesPromotions (Promos) | Active sales, discounts, multi-buy deals | Daily (may lag PricesFull) |
| Stores | Store locations, addresses, operating hours | Weekly or on change |

## Feed Platforms

Not every chain runs its own server. Most chains publish through one of three centralized platforms:

| Platform | URL | Chains Using It |
|----------|-----|-----------------|
| Shufersal Direct | http://prices.shufersal.co.il | Shufersal only |
| Cerberus (PublishedPrices) | https://url.publishedprices.co.il/login | Rami Levy, Yochananof, Osher Ad, Tiv Taam, Hazi Hinam, Keshet Teamim, Super Dosh, Doralon |
| Nibit (Matrix Catalog) | http://matrixcatalog.co.il/NBCompetitionRegulations.aspx | Victory, Mahsanei Lahav, Mahsanei Hashuk |
| Carrefour Israel Direct | https://prices.carrefour.co.il | Carrefour Israel (formerly Mega/Yeinot Bitan) |

Cerberus chains require selecting the chain name from a dropdown or passing a chain identifier. Nibit chains similarly require selecting the chain from a list. Shufersal and Carrefour Israel have dedicated portals with per-store file downloads.

## Per-Chain Feed Access

### Shufersal (שופרסל)
- **Platform:** Direct
- **Feed Portal:** http://prices.shufersal.co.il
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **File naming:** `PriceFull{StoreId}-{FileId}.xml.gz`
- **Schema:** Standard government format with extensions
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Largest chain (850+ stores). Most reliable and structured feed. Good baseline for testing parsers.

### Rami Levy (רמי לוי)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Rami Levy")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format. Uses `ItemNm` instead of `ItemName` in some feeds.
- **Update time:** Typically 01:00-04:00 Israel time
- **Notes:** Known for competitive pricing. 30+ stores nationwide.

### Yochananof (יוחננוף)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Yochananof")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 03:00-06:00 Israel time
- **Notes:** Central Israel focus. Fewer stores means faster full downloads.

### Victory (ויקטורי)
- **Platform:** Nibit (Matrix)
- **Feed Portal:** http://matrixcatalog.co.il/NBCompetitionRegulations.aspx (select "Victory")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Independently owned (Ravid family, publicly traded VCTR.TA). 20+ discount stores. Completely separate from Carrefour Israel.

### Carrefour Israel (קרפור ישראל, formerly Mega/Yeinot Bitan)
- **Platform:** Direct
- **Feed Portal:** https://prices.carrefour.co.il
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Operates under Carrefour, Mega, and Yeinot Bitan brands (same company, Electra Consumer Products franchise). 100+ stores. Legacy URL `publishprice.mega.co.il` redirects here.

### Osher Ad (אושר עד)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login
- **Access:** Username: `osherad`, no password required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format, minimal extensions
- **Update time:** Typically 01:00-03:00 Israel time
- **Notes:** Discount chain with 20+ large-format stores. Some products may have limited metadata.

### Tiv Taam (טיב טעם)
- **Platform:** Cerberus
- **Feed Portal:** https://url.publishedprices.co.il/login (select "Tiv Taam")
- **Access:** Public, no authentication required
- **Format:** Gzipped XML (.xml.gz)
- **Schema:** Standard format
- **Update time:** Typically 02:00-05:00 Israel time
- **Notes:** Includes non-kosher products. Product categories may differ from kosher-only chains.

### Additional Chains on Cerberus
The following smaller chains also publish via `https://url.publishedprices.co.il/login`:
- **Hazi Hinam (חצי חינם)**
- **Keshet Teamim (קשת טעמים)**
- **Super Dosh (סופר דוש)**
- **Doralon (דורלון)**

### Additional Chains on Nibit (Matrix)
- **Mahsanei Lahav (מחסני להב)** via http://matrixcatalog.co.il/NBCompetitionRegulations.aspx
- **Mahsanei Hashuk (מחסני השוק)** via http://matrixcatalog.co.il/NBCompetitionRegulations.aspx

## XML Schema Reference

### PricesFull Schema (common fields)

```xml
<Items>
  <Item>
    <ItemCode>7290000000001</ItemCode>
    <ItemType>0</ItemType>
    <ItemName>חלב תנובה 3% שומן 1 ליטר</ItemName>
    <ManufacturerName>תנובה</ManufacturerName>
    <ManufactureCountry>IL</ManufactureCountry>
    <ManufacturerItemDescription>חלב מפוסטר 3%</ManufacturerItemDescription>
    <UnitQty>1</UnitQty>
    <Quantity>1</Quantity>
    <UnitOfMeasure>ליטר</UnitOfMeasure>
    <bIsWeighted>0</bIsWeighted>
    <QtyInPackage>1</QtyInPackage>
    <ItemPrice>6.50</ItemPrice>
    <UnitOfMeasurePrice>6.50</UnitOfMeasurePrice>
    <AllowDiscount>1</AllowDiscount>
    <ItemStatus>1</ItemStatus>
    <PriceUpdateDate>2026-02-26</PriceUpdateDate>
  </Item>
</Items>
```

### Key Fields

| Field | Description | Notes |
|-------|-------------|-------|
| ItemCode | Barcode / product code | Use for cross-chain matching |
| ItemName | Product name (Hebrew) | Naming varies across chains |
| ManufacturerName | Manufacturer | Useful for fuzzy matching |
| ItemPrice | Current price in NIS | VAT included |
| UnitOfMeasurePrice | Price per unit (kg/liter) | For weight/volume comparison |
| bIsWeighted | 0=fixed, 1=sold by weight | Affects price calculation |
| PriceUpdateDate | Last price update date | Check for staleness |

## Known Format Variations

- **Field naming:** Some chains (notably Rami Levy on Cerberus) use `ItemNm` instead of `ItemName`, or `ManuName` instead of `ManufacturerName`
- **Encoding:** All feeds should be UTF-8, but some chains occasionally produce Windows-1255 encoded files
- **Weighted items:** Price for weighted items (bIsWeighted=1) is per kg; actual cost depends on purchase weight
- **Barcode formats:** Israeli barcodes typically start with 729. Some store-brand items use internal codes starting with 2
- **Promotion overlap:** A product may appear in both PricesFull (regular price) and PricesPromotions (sale price). Always check promotions feed for the effective price
- **Platform differences:** Cerberus and Nibit wrap XML files in their own download pages. The underlying XML schema is the same government standard, but the download method differs per platform.
