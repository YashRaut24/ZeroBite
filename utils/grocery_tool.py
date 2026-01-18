def grocery_tool(missing_items):
    price_map = {
        "tomato": 20,
        "onion": 25,
        "potato": 30,
        "milk": 28,
        "bread": 40,
        "egg": 6
    }

    items = []
    total = 0

    for item in missing_items:
        price = price_map.get(item.lower(), 35)
        items.append({
            "item": item,
            "price": price
        })
        total += price

    return {
        "platform": "Zepto",
        "delivery_time": "10–15 minutes",
        "items": items,
        "total_price": total
    }
