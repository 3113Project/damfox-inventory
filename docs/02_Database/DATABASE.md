Category
│
├── id
├── name
└── parent_id (per categorie annidate)

Product
│
├── id
├── sku
├── name
├── description
├── vat_rate_id
├── category_id
├── minimum_stock
└── active

Supplier
│
├── id
├── name
├── vat_number
├── phone
├── email
└── notes

ProductSupplier
│
├── id
├── product_id
├── supplier_id
├── supplier_code
├── lead_time_days
├── preferred
└── active

PurchasePriceHistory
│
├── id
├── product_supplier_id
├── net_price
├── valid_from
├── valid_to
└── notes

InventoryMovement
│
├── id
├── product_id
├── movement_type
├── quantity
├── reference
├── created_at
└── user


# MODULO 1 - CATALOGO

Entità:

- Category
- Product
- ProductFamily
- Barcode
- Image
- Document
- VATRate
- UnitOfMeasure
- Packaging