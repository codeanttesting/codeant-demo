def calculate_discount(amount, customer_type):
    # DUPLICATE BLOCK 2 - First occurrence
    if amount <= 100:
        discount = amount * 0.05
    elif amount <= 500:
        discount = amount * 0.10
    elif amount <= 1000:
        discount = amount * 0.15
    else:
        discount = amount * 0.20
    
    final_amount = amount - discount
    return final_amount

def calculate_refund(amount, customer_type):
    # DUPLICATE BLOCK 2 - Exact copy (lines 40-49 repeated)
    if amount <= 100:
        discount = amount * 0.05
    elif amount <= 500:
        discount = amount * 0.10
    elif amount <= 1000:
        discount = amount * 0.15
    else:
        discount = amount * 0.20
    
    final_amount = amount - discount
    return final_amount