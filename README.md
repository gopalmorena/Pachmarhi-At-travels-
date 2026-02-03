# Billing System

This repository contains a small, in-memory billing system for managing customers,
invoices, line items, and payments. It is designed to be a starting point that you
can extend with persistent storage, authentication, or a web API.

## Features

- Create customers and invoices.
- Add line items with unit prices and quantities.
- Apply tax rates and calculate totals.
- Record payments and compute remaining balances.
- Generate invoice summaries for reporting or export.

## Quick Example

```python
from decimal import Decimal

from billing_system.service import BillingSystem

billing = BillingSystem(default_tax_rate=Decimal("0.0825"))
customer = billing.create_customer(name="Acme Corp", email="billing@acme.test")
invoice = billing.create_invoice(customer_id=customer.customer_id, memo="March retainer")

billing.add_line_item(
    invoice_id=invoice.invoice_id,
    description="Consulting hours",
    unit_price=Decimal("150.00"),
    quantity=Decimal("10"),
)

billing.record_payment(invoice_id=invoice.invoice_id, amount=Decimal("500.00"))

print(billing.generate_invoice_summary(invoice.invoice_id))
```
