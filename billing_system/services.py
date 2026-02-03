from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from billing_system.models import Customer, Invoice, Item, _to_decimal


class BillingCalculator:
    def create_invoice(
        self,
        *,
        customer: Customer,
        items: Iterable[Item],
        tax_rate: float | Decimal = 0,
        discount: float | Decimal = 0,
    ) -> Invoice:
        invoice = Invoice(
            customer=customer,
            items=list(items),
            tax_rate=_to_decimal(tax_rate),
            discount=_to_decimal(discount),
        )
        return invoice
