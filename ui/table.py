import pandas as pd
import streamlit as st


def render_supplier_table(suppliers):

    table_data = []

    for supplier in suppliers:

        table_data.append({
            "Поставщик": supplier["name"],
            "Город": supplier["city"],
            "Категория": supplier["category"],
            "Рейтинг пользователей": supplier["rating"],
            "Рейтинг системы": supplier["score"],
            "Мин. заказ (₽)": supplier["min_order"],
            "Бесплатная доставка (₽)": supplier["free_delivery"],
            "Сертификат": ("✅"if supplier["certificates"]else "❌"),
            "Условия оплаты": supplier["payment_terms"],
            "Уровень цен": supplier["price_level"],
            "Сайт": supplier["website"],
            "Email": supplier["email"],
            "Телефон": supplier["phone"]
        })

    st.dataframe(pd.DataFrame(table_data),use_container_width=True,hide_index=True)