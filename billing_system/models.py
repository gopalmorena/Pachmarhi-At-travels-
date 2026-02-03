from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import List
from uuid import uuid4

MONEY_PLACES = Decimal("0.01")


def _round_money(amount: Decimal) -> Decimal:
    return amount.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


class InvoiceStatus(str, Enum):
    OPEN = "open"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    customer_id: str = field(default_factory=lambda: f"cus_{uuid4().hex}")
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class LineItem:
    description: str
    unit_price: Decimal
    quantity: Decimal = Decimal("1")
    item_id: str = field(default_factory=lambda: f"item_{uuid4().hex}")

    def total(self) -> Decimal:
        return _round_money(self.unit_price * self.quantity)


@dataclass(frozen=True)
class Payment:
    amount: Decimal
    paid_at: datetime = field(default_factory=datetime.utcnow)
    payment_id: str = field(default_factory=lambda: f"pay_{uuid4().hex}")
    reference: str | None = None


@dataclass
class Invoice:
    customer_id: str
    invoice_id: str = field(default_factory=lambda: f"inv_{uuid4().hex}")
    issued_on: date = field(default_factory=date.today)
    memo: str | None = None
    tax_rate: Decimal = Decimal("0.00")
    line_items: List[LineItem] = field(default_factory=list)
    payments: List[Payment] = field(default_factory=list)

    def add_item(self, item: LineItem) -> None:
        self.line_items.append(item)

    def add_payment(self, payment: Payment) -> None:
        self.payments.append(payment)

    def subtotal(self) -> Decimal:
        total = sum((item.total() for item in self.line_items), Decimal("0"))
        return _round_money(total)

    def tax(self) -> Decimal:
        return _round_money(self.subtotal() * self.tax_rate)

    def total(self) -> Decimal:
        return _round_money(self.subtotal() + self.tax())

    def paid_total(self) -> Decimal:
        total = sum((payment.amount for payment in self.payments), Decimal("0"))
        return _round_money(total)

    def balance_due(self) -> Decimal:
        return _round_money(self.total() - self.paid_total())

    def status(self) -> InvoiceStatus:
        balance = self.balance_due()
        if balance <= Decimal("0"):
            return InvoiceStatus.PAID
        if self.paid_total() > Decimal("0"):
            return InvoiceStatus.PARTIALLY_PAID
        return InvoiceStatus.OPEN
