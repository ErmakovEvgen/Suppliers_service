def render_supplier_cards(suppliers):
    cards_html = '<div class="cards-container">'
    
    for index, supplier in enumerate(suppliers):
        card_class = "supplier-card"
        if index == 0:
            card_class += " best-card"
        
        badge_html = '<div class="badge">🏆 Рекомендуемый</div>' if index == 0 else ''
        
        name = supplier["name"].replace('"', '&quot;')
        city_name = supplier["city"].replace('"', '&quot;')
        certificates_text = "✅" if supplier.get("certificates", False) else "❌"
        category_emoji = {
            "молочная продукция": "🥛 Молочная продукция",
            "мясо": "🥩 Мясо", 
            "овощи": "🥗 Овощи",
            "фрукты": "🍎 Фрукты",
            "рыба": "🐟 Рыба",
            "бакалея": "🌾 Бакалея"
        }.get(supplier.get("category", ""), "📦")

        cards_html += f"""
        <div class="{card_class}">
            {badge_html}
            <h3>{name}</h3>
            <p>{category_emoji}</p>
            <p>📍 {city_name}</p>
            <p>⭐ Рейтинг пользователей: {supplier['rating']}</p>
            <p>ℹ️ Рейтинг системы: {supplier['score']}</p>
            <p>📦 Минимальный заказ от {supplier['min_order']:,} ₽</p>
            <p>🚚 Бесплатная доставка от {supplier['free_delivery']:,} ₽</p>
            <p>💵 Уровень цен: {supplier['price_level']}</p>
            <p>💰 Условия оплаты:  {supplier['payment_terms']}</p>
            <p>📝 Наличие сертификата: {certificates_text} </p>
            <p>🌐 Сайт: {supplier['website']:} </p>
            <p>📧 e-mail: {supplier['email']:} </p>
            <p>📞 Телефон: {supplier['phone']:} </p>
        </div>
        """
    
    cards_html += "</div>"
    return cards_html