from django import template

register = template.Library()

@register.filter
def total_price(stock_bills):
    total = sum(float(stock_bill.Total_Amount) for stock_bill in stock_bills)
    return f"{total:.2f}"