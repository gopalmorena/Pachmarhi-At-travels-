from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List

from billing_system.models import Customer, Invoice, Item


class InvoiceRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, invoice: Invoice) -> None:
        invoices = self._load_raw()
        invoices.append(self._serialize_invoice(invoice))
        self.path.write_text(json.dumps(invoices, indent=2), encoding="utf-8")

    def list_invoices(self) -> List[Invoice]:
        return [self._deserialize_invoice(payload) for payload in self._load_raw()]

    def _load_raw(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []

    def _serialize_invoice(self, invoice: Invoice) -> Dict[str, Any]:
        data = asdict(invoice)
        data["created_at"] = invoice.created_at.isoformat()
        data["items"] = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "line_total": str(item.line_total),
            }
            for item in invoice.items
        ]
        data["tax_rate"] = str(invoice.tax_rate)
        data["discount"] = str(invoice.discount)
        data["subtotal"] = str(invoice.subtotal())
        data["tax_amount"] = str(invoice.tax_amount())
        data["total"] = str(invoice.total())
        return data

    def _deserialize_invoice(self, payload: Dict[str, Any]) -> Invoice:
        customer_payload = payload["customer"]
        customer = Customer(
            name=customer_payload["name"],
            email=customer_payload["email"],
            phone=customer_payload.get("phone"),
        )
        items = [
            Item(
                description=item["description"],
                quantity=int(item["quantity"]),
                unit_price=Decimal(str(item["unit_price"])),
            )
            for item in payload.get("items", [])
        ]
        return Invoice(
            customer=customer,
            items=items,
            tax_rate=Decimal(str(payload.get("tax_rate", "0.00"))),
            discount=Decimal(str(payload.get("discount", "0.00"))),
            invoice_id=payload.get("invoice_id", ""),
            created_at=datetime.fromisoformat(payload["created_at"]),
        )
