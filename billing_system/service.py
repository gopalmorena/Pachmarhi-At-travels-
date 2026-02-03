from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict

from billing_system.models import Customer, Invoice, LineItem, Payment


@dataclass
class BillingSystem:
    default_tax_rate: Decimal = Decimal("0.00")
    customers: Dict[str, Customer] = field(default_factory=dict)
    invoices: Dict[str, Invoice] = field(default_factory=dict)

    def create_customer(self, name: str, email: str) -> Customer:
        customer = Customer(name=name, email=email)
        self.customers[customer.customer_id] = customer
        return customer

    def get_customer(self, customer_id: str) -> Customer:
        return self.customers[customer_id]

    def create_invoice(self, customer_id: str, memo: str | None = None) -> Invoice:
        if customer_id not in self.customers:
            raise KeyError(f"Customer {customer_id} does not exist.")
        invoice = Invoice(customer_id=customer_id, memo=memo, tax_rate=self.default_tax_rate)
        self.invoices[invoice.invoice_id] = invoice
        return invoice

    def get_invoice(self, invoice_id: str) -> Invoice:
        return self.invoices[invoice_id]

    def add_line_item(
        self,
        invoice_id: str,
        description: str,
        unit_price: Decimal,
        quantity: Decimal = Decimal("1"),
    ) -> LineItem:
        invoice = self.get_invoice(invoice_id)
        item = LineItem(description=description, unit_price=unit_price, quantity=quantity)
        invoice.add_item(item)
        return item

    def record_payment(
        self,
        invoice_id: str,
        amount: Decimal,
        reference: str | None = None,
    ) -> Payment:
        invoice = self.get_invoice(invoice_id)
        payment = Payment(amount=amount, reference=reference)
        invoice.add_payment(payment)
        return payment

    def generate_invoice_summary(self, invoice_id: str) -> dict[str, str]:
        invoice = self.get_invoice(invoice_id)
        customer = self.get_customer(invoice.customer_id)
        return {
            "invoice_id": invoice.invoice_id,
            "customer": customer.name,
            "email": customer.email,
            "issued_on": invoice.issued_on.isoformat(),
            "memo": invoice.memo or "",
            "status": invoice.status().value,
            "subtotal": f"{invoice.subtotal():.2f}",
            "tax": f"{invoice.tax():.2f}",
            "total": f"{invoice.total():.2f}",
            "paid": f"{invoice.paid_total():.2f}",
            "balance_due": f"{invoice.balance_due():.2f}",
        }
