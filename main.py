import streamlit as st
from services.supplier_service import SupplierService
from ui.components import render_supplier_cards
from streamlit.components.v1 import html
from services.llm_service import LLMService
from ui.table import render_supplier_table
from ui.info import render_rating_info

service = SupplierService()
llm_service = LLMService()

if "suppliers" not in st.session_state:
    st.session_state.suppliers = None

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "cards"

def load_css():
    with open("ui/styles.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def get_css_for_iframe():
    with open("ui/styles.css", encoding="utf-8") as f:
        return f.read()

st.set_page_config(
    page_title="AI Supplier Assistant",
    page_icon="🤖",
    layout="wide"
)

load_css()

st.title("🤖 ИИ-помощник для поиска поставщиков")

st.markdown("""Найдите поставщиков, сравните предложения и получите рекомендации на основе ИИ.""")

col1, col2 = st.columns(2)

with col1:
    category = st.text_input("Категория товара", placeholder="Например: молочная продукция")

with col2:
    city = st.text_input("Регион", placeholder="Например: Екатеринбург")

if st.button("Найти поставщиков"):

    suppliers = service.search(category, city)

    if not suppliers:
        st.warning("Поставщики не найдены")

        st.session_state.suppliers = None
        st.session_state.recommendation = None

    else:

        for supplier in suppliers:
            supplier["score"] = service.calculate_score(supplier)

        suppliers.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        st.session_state.suppliers = suppliers
        st.session_state.recommendation = None

        st.success(
            f"Найдено {len(suppliers)} поставщиков"
        )

if st.session_state.suppliers:

    suppliers = st.session_state.suppliers

    col1, col2 = st.columns([8, 1])

    with col2:
        button_text = (
            "📊 Таблица"
            if st.session_state.view_mode == "cards"
            else "📇 Карточки"
        )

        if st.button(button_text):
            st.session_state.view_mode = (
                "table"
                if st.session_state.view_mode == "cards"
                else "cards"
            )
            st.rerun()

    if st.session_state.view_mode == "cards":

        cards_html = render_supplier_cards(
            suppliers
        )

        css_content = get_css_for_iframe()

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {css_content}
            </style>
        </head>
        <body style="margin: 0; padding: 0;">
            {cards_html}
        </body>
        </html>
        """

        html(
            full_html,
            height=500,
            scrolling=True
        )

    else:
        render_supplier_table(suppliers)

    st.divider()

    if st.button("Получить AI-рекомендацию", use_container_width=True):
        with st.spinner("ИИ анализирует поставщиков..."):

            st.session_state.recommendation = (
                llm_service.generate_recommendation(
                    suppliers,
                    category
                )
            )

if st.session_state.recommendation:
    st.subheader("🤖 AI-анализ")
    st.markdown(st.session_state.recommendation)

st.divider()

col1, col2 = st.columns([12, 1])

with col2:
    render_rating_info()