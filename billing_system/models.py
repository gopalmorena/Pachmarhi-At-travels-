from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import uuid4


def _to_decimal(value: float | str | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    phone: str | None = None


@dataclass(frozen=True)
class Item:
    description: str
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return _to_decimal(self.unit_price * self.quantity)


@dataclass
class Invoice:
    customer: Customer
    items: List[Item] = field(default_factory=list)
    tax_rate: Decimal = Decimal("0.00")
    discount: Decimal = Decimal("0.00")
    invoice_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def subtotal(self) -> Decimal:
        return _to_decimal(sum((item.line_total for item in self.items), Decimal("0.00")))

    def tax_amount(self) -> Decimal:
        return _to_decimal(self.subtotal() * (self.tax_rate / Decimal("100")))

    def total(self) -> Decimal:
        return _to_decimal(self.subtotal() + self.tax_amount() - self.discount)
