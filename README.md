# Food Delivery Order Processor 🍔🍕

A Python CLI application designed to process batch food delivery orders, validate item codes, calculate progressive discounts and delivery fees, track high-value sales, and generate a daily sales report.

---

## 🚀 Key Functionality

- **Menu & Order Validation**: Gracefully flags empty orders, negative item counts, and unknown menu codes without crashing.
- **Progressive Discounting**:
  - Subtotal ≥ $100 ➔ **15% off**
  - Subtotal ≥ $50 ➔ **10% off**
  - Subtotal ≥ $30 ➔ **5% off**
- **Delivery Fee Logic**: Standard **$4.99** fee; **FREE** delivery for orders with subtotal ≥ $50.00.
- **Highest-Value Order Tracking**: Identifies the single largest order processed during the execution run.
- **Summary Persistence**: Generates a formatted output file (`sales_summary.txt`).

---

## 🛠️ Repository File Overview

```text
├── food_delivery.py     # Main application script
├── sample_orders.json   # Sample input dataset containing 10 test orders
├── sales_summary.txt    # Generated daily sales log report
├── obstacle_log.md      # Development obstacle log & resolution notes
└── README.md            # Repository documentation
