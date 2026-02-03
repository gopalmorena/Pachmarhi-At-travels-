from __future__ import annotations

import argparse
from decimal import Decimal

from billing_system.models import Customer, Item
from billing_system.services import BillingCalculator
from billing_system.storage import InvoiceRepository


def _parse_item(raw: str) -> Item:
    try:
        description, quantity, unit_price = raw.split(",", 2)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Item format should be: description,quantity,unit_price"
        ) from exc
    return Item(description=description, quantity=int(quantity), unit_price=Decimal(unit_price))


def create_invoice(args: argparse.Namespace) -> None:
    customer = Customer(
        name=args.customer_name,
        email=args.customer_email,
        phone=args.customer_phone,
    )
    calculator = BillingCalculator()
    invoice = calculator.create_invoice(
        customer=customer,
        items=args.item,
        tax_rate=args.tax_rate,
        discount=args.discount,
    )
    repo = InvoiceRepository(args.storage)
    repo.save(invoice)
    print(f"Invoice created: {invoice.invoice_id}")
    print(f"Subtotal: {invoice.subtotal()}")
    print(f"Tax: {invoice.tax_amount()}")
    print(f"Total: {invoice.total()}")


def list_invoices(args: argparse.Namespace) -> None:
    repo = InvoiceRepository(args.storage)
    invoices = repo.list_invoices()
    if not invoices:
        print("No invoices found.")
        return
    for invoice in invoices:
        print(
            f"{invoice.invoice_id} | {invoice.customer.name} | "
            f"{invoice.total()} | {invoice.created_at.isoformat()}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Billing system CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    parser.add_argument(
        "--storage",
        default="data/invoices.json",
        help="Path to storage JSON file",
    )

    subparsers = parser.add_subparsers(dest="command")
    create_parser = subparsers.add_parser("create", help="Create a new invoice")
    create_parser.set_defaults(func=create_invoice)
    create_parser.add_argument("--customer-name", required=True)
    create_parser.add_argument("--customer-email", required=True)
    create_parser.add_argument("--customer-phone")
    create_parser.add_argument(
        "--item",
        required=True,
        action="append",
        type=_parse_item,
        help='Item format: "description,quantity,unit_price"',
    )
    create_parser.add_argument("--tax-rate", type=Decimal, default=Decimal("0.00"))
    create_parser.add_argument("--discount", type=Decimal, default=Decimal("0.00"))

    list_parser = subparsers.add_parser("list", help="List invoices")
    list_parser.set_defaults(func=list_invoices)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
