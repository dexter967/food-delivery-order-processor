# Obstacle Log: Food Delivery Order Processor

This document outlines technical obstacles encountered during development and details how each issue was resolved.

---

### Obstacle 1: Unhandled Invalid Menu Items and Bad Quantities
* **Issue:** Sample orders containing non-existent item keys (e.g., `'TACO'`) or negative quantities (`-1`) resulted in `KeyError` crashes or incorrect subtotal reductions.
* **Resolution:** Implemented explicit validation in `calculate_subtotal()`. Every item code is checked against `menu.keys()`, and quantities are confirmed to be positive integers (`isinstance(qty, int) and qty > 0`). Flagged items are skipped, and error descriptions are attached to the order result object.

---

### Obstacle 2: Order of Discount and Delivery Charge Application
* **Issue:** Applying delivery charges *before* calculating percentage discounts generated unexpected bill totals and altered threshold eligibility.
* **Resolution:** Standardized order calculation sequence:
  1. Compute raw subtotal.
  2. Determine discount rate based on subtotal.
  3. Determine delivery fee eligibility based on raw subtotal ($50 threshold for free delivery).
  4. Sum discounted subtotal and delivery fee for final total.

---

### Obstacle 3: Text Report Punctuation and Alignment Errors
* **Issue:** Missing spaces and inconsistent punctuation in the rejected orders section degraded readability when order IDs or reasons varied in length.
* **Resolution:** Refined output formatting in `sales_summary.txt` using explicit field width specifiers (e.g., `{b['order_id']:<10}`) and standardized punctuation formats across status messages.
