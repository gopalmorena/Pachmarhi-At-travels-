# Billing System

यह एक सरल लेकिन पूरा किया गया billing system है जो इनवॉइस बनाने, टोटल निकालने, टैक्स/डिस्काउंट लगाने, और JSON फाइल में सेव करने की सुविधा देता है।

## Features
- ग्राहक (Customer) और आइटम (Item) मॉडल
- इनवॉइस जनरेशन और लाइन‑आइटम टोटल
- टैक्स और डिस्काउंट सपोर्ट
- JSON में सेव/लोड सपोर्ट
- CLI से इनवॉइस बनाना

## Quick Start
```bash
python -m billing_system.cli create \
  --customer-name "Rahul Sharma" \
  --customer-email "rahul@example.com" \
  --item "Notebook,2,120.0" \
  --item "Pen,5,10.0" \
  --tax-rate 18 \
  --discount 50
```

## Data Storage
इनवॉइस `data/invoices.json` में सेव होते हैं। यदि फाइल मौजूद नहीं है तो सिस्टम खुद बना देगा।

## Project Structure
```
billing_system/
  __init__.py
  cli.py
  models.py
  services.py
  storage.py
data/
  invoices.json
```
