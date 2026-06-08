import json

class SupplierService:
    def __init__(self):
        with open("data/suppliers.json", "r", encoding="utf-8") as file:
            self.suppliers = json.load(file)

    def search(self, category, city):
        return [
            supplier
            for supplier in self.suppliers
            if category.lower() in supplier["category"].lower()
            and city.lower() in supplier["city"].lower()
        ]
    def calculate_score(self, supplier):
        weights = {
            "rating": 0.40,
            "certificates": 0.15,
            "free_delivery": 0.10,
            "min_order": 0.10,
            "price": 0.15,
            "payment_terms": 0.10
        }
    
        rating_score = supplier.get("rating", 0) / 5.0
        cert_score = 1.0 if supplier.get("certificates", False) else 0.0
        max_free_delivery = 50000
        free_delivery_score = max(0, 1 - supplier.get("free_delivery", 50000) / max_free_delivery)
        max_min_order = 50000
        min_order_score = max(0, 1 - supplier.get("min_order", 50000) / max_min_order)
        price_scores = {"низкий": 1.0, "средний": 0.6, "высокий": 0.2}
        price_score = price_scores.get(supplier.get("price_level", "средний"), 0.6)
        payment_scores = {"отсрочка": 1.0, "предоплата": 0.3}
        payment_score = payment_scores.get(supplier.get("payment_terms", "предоплата"), 0.3)

        total_score = (
            rating_score * weights["rating"] * 100 + cert_score * weights["certificates"] * 100 + free_delivery_score * weights["free_delivery"] * 100 +
            min_order_score * weights["min_order"] * 100 + price_score * weights["price"] * 100 + payment_score * weights["payment_terms"] * 100
            )
    
        return round(total_score, 1)