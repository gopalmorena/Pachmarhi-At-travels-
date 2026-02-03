from decimal import Decimal

from billing_system.service import BillingSystem


def test_invoice_totals_and_statuses():
    billing = BillingSystem(default_tax_rate=Decimal("0.10"))
    customer = billing.create_customer(name="Northwind", email="billing@northwind.test")
    invoice = billing.create_invoice(customer_id=customer.customer_id, memo="Quarterly support")

    billing.add_line_item(
        invoice_id=invoice.invoice_id,
        description="Support hours",
        unit_price=Decimal("200.00"),
        quantity=Decimal("2"),
    )

    billing.add_line_item(
        invoice_id=invoice.invoice_id,
        description="Incident response",
        unit_price=Decimal("150.00"),
        quantity=Decimal("1.5"),
    )

    assert invoice.subtotal() == Decimal("625.00")
    assert invoice.tax() == Decimal("62.50")
    assert invoice.total() == Decimal("687.50")
    assert invoice.balance_due() == Decimal("687.50")
    assert invoice.status().value == "open"

    billing.record_payment(invoice_id=invoice.invoice_id, amount=Decimal("300.00"))
    assert invoice.paid_total() == Decimal("300.00")
    assert invoice.balance_due() == Decimal("387.50")
    assert invoice.status().value == "partially_paid"

    billing.record_payment(invoice_id=invoice.invoice_id, amount=Decimal("387.50"))
    assert invoice.paid_total() == Decimal("687.50")
    assert invoice.balance_due() == Decimal("0.00")
    assert invoice.status().value == "paid"


def test_invoice_summary():
    billing = BillingSystem(default_tax_rate=Decimal("0.05"))
    customer = billing.create_customer(name="Adventure Works", email="ap@adventure.test")
    invoice = billing.create_invoice(customer_id=customer.customer_id)

    billing.add_line_item(
        invoice_id=invoice.invoice_id,
        description="Subscription",
        unit_price=Decimal("99.99"),
        quantity=Decimal("1"),
    )

    summary = billing.generate_invoice_summary(invoice.invoice_id)

    assert summary["customer"] == "Adventure Works"
    assert summary["subtotal"] == "99.99"
    assert summary["tax"] == "5.00"
    assert summary["total"] == "104.99"
