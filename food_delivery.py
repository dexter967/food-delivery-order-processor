"""
Food Delivery Order Processor
-----------------------------
A Python script to process food delivery orders, handle edge cases,
apply progressive discounts, calculate delivery charges, determine the
highest-value order, and persist daily sales summaries to a text file.
"""

import json
import os

# Delivery and Discount Configuration
FREE_DELIVERY_THRESHOLD = 50.0  # Free delivery on order subtotal >= $50
STANDARD_DELIVERY_FEE = 4.99   # Standard fee if subtotal < $50

DISCOUNT_TIERS = [
    (100.0, 0.15),  # 15% discount for orders $100 and above
    (50.0, 0.10),   # 10% discount for orders $50 and above
    (30.0, 0.05),   # 5% discount for orders $30 and above
]


# ==========================================
# Step 1: Setup Default Data Structures
# ==========================================

DEFAULT_MENU = {
    "BURGER": {"name": "Gourmet Cheeseburger", "price": 12.50},
    "PIZZA": {"name": "Margherita Pizza", "price": 16.00},
    "PASTA": {"name": "Truffle Penne Pasta", "price": 18.50},
    "SALAD": {"name": "Caesar Salad", "price": 9.50},
    "FRIES": {"name": "Crispy French Fries", "price": 4.50},
    "SODA": {"name": "Sparkling Soda", "price": 2.50},
    "DESSERT": {"name": "Chocolate Lava Cake", "price": 7.00},
}


def load_orders(file_path="sample_orders.json"):
    """Loads sample orders from JSON file if present, otherwise returns defaults."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Fallback dataset with 10 sample orders (including edge cases)
    return [
        {"order_id": "ORD-101", "customer": "Alice", "items": [{"item_code": "BURGER", "quantity": 2}, {"item_code": "FRIES", "quantity": 2}, {"item_code": "SODA", "quantity": 2}]},
        {"order_id": "ORD-102", "customer": "Bob", "items": [{"item_code": "PIZZA", "quantity": 1}, {"item_code": "SODA", "quantity": 1}]},
        {"order_id": "ORD-103", "customer": "Charlie", "items": [{"item_code": "PASTA", "quantity": 4}, {"item_code": "DESSERT", "quantity": 3}, {"item_code": "PIZZA", "quantity": 2}]},
        {"order_id": "ORD-104", "customer": "Diana", "items": []},  # Empty order test
        {"order_id": "ORD-105", "customer": "Evan", "items": [{"item_code": "SALAD", "quantity": 1}]},
        {"order_id": "ORD-106", "customer": "Fiona", "items": [{"item_code": "TACO", "quantity": 3}]},  # Invalid item test
        {"order_id": "ORD-107", "customer": "George", "items": [{"item_code": "PIZZA", "quantity": 3}, {"item_code": "PASTA", "quantity": 2}, {"item_code": "DESSERT", "quantity": 4}]},
        {"order_id": "ORD-108", "customer": "Hannah", "items": [{"item_code": "BURGER", "quantity": 1}, {"item_code": "FRIES", "quantity": -1}]},  # Negative quantity test
        {"order_id": "ORD-109", "customer": "Ian", "items": [{"item_code": "PASTA", "quantity": 1}, {"item_code": "SALAD", "quantity": 1}, {"item_code": "SODA", "quantity": 1}]},
        {"order_id": "ORD-110", "customer": "Julia", "items": [{"item_code": "BURGER", "quantity": 5}, {"item_code": "PIZZA", "quantity": 3}, {"item_code": "PASTA", "quantity": 2}, {"item_code": "DESSERT", "quantity": 5}]},
    ]


# ==========================================
# Step 2 & 3: Core Calculations & Validation
# ==========================================

def calculate_subtotal(order, menu):
    """Calculates order subtotal and validates item presence and quantities."""
    items = order.get("items", [])
    if not items:
        return 0.0, ["Order contains no items (empty order)."]

    subtotal = 0.0
    errors = []

    for entry in items:
        code = entry.get("item_code")
        qty = entry.get("quantity", 0)

        if code not in menu:
            errors.append(f"Invalid menu item code: '{code}'")
            continue
        
        if not isinstance(qty, int) or qty <= 0:
            errors.append(f"Invalid quantity ({qty}) for item '{code}'")
            continue

        item_price = menu[code]["price"]
        subtotal += item_price * qty

    return round(subtotal, 2), errors


def calculate_discount(subtotal):
    """Applies percentage discount based on progressive value tiers."""
    for threshold, rate in DISCOUNT_TIERS:
        if subtotal >= threshold:
            discount_amount = round(subtotal * rate, 2)
            return discount_amount, int(rate * 100)
    return 0.0, 0


def calculate_delivery_charge(subtotal):
    """Determines delivery fee based on order subtotal."""
    if subtotal >= FREE_DELIVERY_THRESHOLD:
        return 0.0
    return STANDARD_DELIVERY_FEE


def process_order(order, menu):
    """Processes a single order and returns structured bill details or rejection notice."""
    order_id = order.get("order_id", "UNKNOWN")
    customer = order.get("customer", "Guest")

    subtotal, errors = calculate_subtotal(order, menu)

    # Reject if errors exist or subtotal is 0
    if errors or subtotal == 0.0:
        return {
            "order_id": order_id,
            "customer": customer,
            "status": "REJECTED",
            "reasons": errors if errors else ["Zero order value."],
            "final_total": 0.0,
        }

    discount, discount_pct = calculate_discount(subtotal)
    discounted_subtotal = subtotal - discount
    delivery_fee = calculate_delivery_charge(subtotal)
    final_total = round(discounted_subtotal + delivery_fee, 2)

    return {
        "order_id": order_id,
        "customer": customer,
        "status": "PROCESSED",
        "subtotal": subtotal,
        "discount": discount,
        "discount_pct": discount_pct,
        "delivery_fee": delivery_fee,
        "final_total": final_total,
    }


# ==========================================
# Step 4 & 5: Batch Processing & File Export
# ==========================================

def process_all_orders(orders, menu):
    """Processes all orders, tracks metrics, and identifies the highest-value order."""
    processed_bills = []
    rejected_orders = []
    total_revenue = 0.0
    highest_order = None

    for order in orders:
        result = process_order(order, menu)
        
        if result["status"] == "PROCESSED":
            processed_bills.append(result)
            total_revenue += result["final_total"]
            
            if highest_order is None or result["final_total"] > highest_order["final_total"]:
                highest_order = result
        else:
            rejected_orders.append(result)

    return {
        "processed_bills": processed_bills,
        "rejected_orders": rejected_orders,
        "total_orders": len(orders),
        "successful_orders": len(processed_bills),
        "failed_orders": len(rejected_orders),
        "total_revenue": round(total_revenue, 2),
        "highest_order": highest_order,
    }


def write_sales_summary(summary, output_file="sales_summary.txt"):
    """Writes the processed sales report and metrics to a text file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=====================================================\n")
        f.write("            DAILY SALES SUMMARY REPORT              \n")
        f.write("=====================================================\n\n")

        f.write(f"Total Orders Received  : {summary['total_orders']}\n")
        f.write(f"Successfully Processed : {summary['successful_orders']}\n")
        f.write(f"Rejected / Failed      : {summary['failed_orders']}\n")
        f.write(f"Total Revenue Generated: ${summary['total_revenue']:.2f}\n")
        f.write("-" * 53 + "\n\n")

        # Highest Value Order Section
        ho = summary["highest_order"]
        f.write("🏆 HIGHEST-VALUE ORDER\n")
        f.write("-" * 53 + "\n")
        if ho:
            f.write(f"Order ID     : {ho['order_id']}\n")
            f.write(f"Customer     : {ho['customer']}\n")
            f.write(f"Subtotal     : ${ho['subtotal']:.2f}\n")
            f.write(f"Discount     : -${ho['discount']:.2f} ({ho['discount_pct']}% off)\n")
            f.write(f"Delivery Fee : ${ho['delivery_fee']:.2f}\n")
            f.write(f"Final Total  : ${ho['final_total']:.2f}\n")
        else:
            f.write("No valid orders were processed.\n")
        f.write("-" * 53 + "\n\n")

        # Itemized Successful Orders
        f.write("📋 PROCESSED ORDERS BREAKDOWN\n")
        f.write("-" * 53 + "\n")
        f.write(f"{'ID':<10} | {'Customer':<10} | {'Subtotal':<9} | {'Disc.':<7} | {'Total':<9}\n")
        f.write("-" * 53 + "\n")
        for b in summary["processed_bills"]:
            f.write(f"{b['order_id']:<10} | {b['customer']:<10} | ${b['subtotal']:<8.2f} | -${b['discount']:<5.2f} | ${b['final_total']:<8.2f}\n")
        f.write("\n")

        # Rejected Orders Section
        f.write("⚠️ REJECTED ORDERS & ISSUES\n")
        f.write("-" * 53 + "\n")
        for r in summary["rejected_orders"]:
            reasons = "; ".join(r["reasons"])
            f.write(f"[{r['order_id']}] Customer: {r['customer']} | Reason: {reasons}\n")

        f.write("\n=====================================================\n")
        f.write("End of Report\n")

    print(f"✅ Sales report successfully exported to '{output_file}'.")


# ==========================================
# Main Execution
# ==========================================

def main():
    print("🚀 Starting Food Delivery Order Processor...\n")
    orders = load_orders()
    summary = process_all_orders(orders, DEFAULT_MENU)

    # Console Output Overview
    print(f"Processed {summary['successful_orders']}/{summary['total_orders']} orders successfully.")
    print(f"Total Daily Revenue: ${summary['total_revenue']:.2f}")
    if summary["highest_order"]:
        ho = summary["highest_order"]
        print(f"Highest-Value Order: {ho['order_id']} by {ho['customer']} (${ho['final_total']:.2f})")

    # Export Report
    write_sales_summary(summary)


if __name__ == "__main__":
    main()
