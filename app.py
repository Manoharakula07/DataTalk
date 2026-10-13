import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DataTalk | Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
[data-testid="stMetric"] {
    background: #172033;
    padding: 20px;
    border: 1px solid #28364f;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8;
}
[data-testid="stMetricValue"] {
    color: #60a5fa;
}
div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}
div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 DataTalk")
st.caption("INTELLIGENT CONVERSATIONAL ANALYTICS")
st.markdown(
    "Upload your dataset, explore your data, and ask questions in simple English."
)

st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ DataTalk")
    st.write("Your personal data analytics assistant.")
    st.divider()

    uploaded_file = st.file_uploader(
        "📁 Upload your CSV file",
        type=["csv"]
    )

    st.divider()
    st.caption("DataTalk V3")
    st.caption("Conversational Analytics System")


# ---------------- LOAD DATA ----------------
if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to get started.")

    st.markdown("### ✨ What you can do")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📈 Explore")
        st.write("View your data and summary statistics.")

    with col2:
        st.markdown("#### 📊 Visualize")
        st.write("Understand patterns using interactive charts.")

    with col3:
        st.markdown("#### 💬 Ask questions")
        st.write("Ask questions about revenue, products, and quantities.")

    st.stop()


# ---------------- READ CSV ----------------
try:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.astype(str).str.strip()

except Exception as e:
    st.error(f"Unable to read the CSV file: {e}")
    st.stop()


if df.empty:
    st.warning("Your CSV file is empty.")
    st.stop()


# ---------------- DATA PREPARATION ----------------
column_map = {
    str(col).strip().lower(): col
    for col in df.columns
}


def get_column(name):
    return column_map.get(name.lower())


product_col = get_column("Product")
category_col = get_column("Category")
revenue_col = get_column("Revenue")
quantity_col = get_column("Quantity")
price_col = get_column("UnitPrice")


# Convert known numeric columns to numeric values
for col in [revenue_col, quantity_col, price_col]:
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# ---------------- KPI CARDS ----------------
st.subheader("📌 Dashboard Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Rows", f"{len(df):,}")

with k2:
    st.metric("Total Columns", f"{len(df.columns):,}")

with k3:
    missing_values = int(df.isna().sum().sum())
    st.metric("Missing Values", f"{missing_values:,}")

with k4:
    if revenue_col is not None:
        total_revenue = df[revenue_col].sum()
        st.metric("Total Revenue", f"{total_revenue:,.2f}")
    else:
        st.metric("Total Revenue", "N/A")


st.divider()


# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📄 Explore Data",
    "💬 Ask DataTalk",
    "📋 Data Quality"
])


# ---------------- DASHBOARD TAB ----------------
with tab1:
    st.subheader("Revenue Analysis")

    if revenue_col is not None and product_col is not None:

        product_revenue = (
            df.groupby(product_col, dropna=False)[revenue_col]
            .sum()
            .reset_index()
            .sort_values(revenue_col, ascending=False)
        )

        fig = px.bar(
            product_revenue,
            x=product_col,
            y=revenue_col,
            title="Revenue by Product",
            text_auto=".2s",
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            font_color="#f1f5f9"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif revenue_col is not None and category_col is not None:

        category_revenue = (
            df.groupby(category_col, dropna=False)[revenue_col]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_revenue,
            x=category_col,
            y=revenue_col,
            title="Revenue by Category",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(
            "A Revenue column is required for revenue charts. "
            "Check your CSV column names."
        )

    if quantity_col is not None and product_col is not None:
        st.subheader("Quantity Sold by Product")

        quantity_data = (
            df.groupby(product_col, dropna=False)[quantity_col]
            .sum()
            .reset_index()
            .sort_values(quantity_col, ascending=False)
        )

        fig2 = px.bar(
            quantity_data,
            x=product_col,
            y=quantity_col,
            title="Units Sold",
            template="plotly_dark"
        )

        st.plotly_chart(fig2, use_container_width=True)


# ---------------- EXPLORE DATA TAB ----------------
with tab2:
    st.subheader("📄 Dataset Preview")

    st.write(f"Showing {len(df)} rows and {len(df.columns)} columns.")

    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Summary Statistics")

    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True
    )

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        st.subheader("Explore a Numeric Column")

        selected_column = st.selectbox(
            "Select a column",
            numeric_cols
        )

        fig3 = px.histogram(
            df,
            x=selected_column,
            title=f"Distribution of {selected_column}",
            template="plotly_dark"
        )

        st.plotly_chart(fig3, use_container_width=True)


# ---------------- ASK DATATALK TAB ----------------
with tab3:
    st.subheader("💬 Ask Questions About Your Data")

    st.write(
        "Try questions like 'What is the total revenue?' "
        "or 'Which product sold the most units?'"
    )

    example_questions = [
        "What is the total revenue?",
        "What is the average revenue?",
        "Which product has the highest revenue?",
        "Which product sold the most units?",
        "How many units were sold?",
        "Show all products",
        "Which category has the highest revenue?"
    ]

    selected_question = st.selectbox(
        "Choose an example question",
        ["Choose a question..."] + example_questions
    )

    user_question = st.text_input(
        "Or type your own question",
        placeholder="Example: How many Backpacks were sold?"
    )

    ask_button = st.button("🔍 Ask DataTalk")

    if ask_button:

        question = user_question.strip()

        if not question and selected_question != "Choose a question...":
            question = selected_question

        q = question.lower().strip()

        if not q:
            st.warning("Please enter or select a question.")

        else:
            answer = None

            # TOTAL REVENUE
            if "revenue" in q and any(
                word in q for word in ["total", "overall", "sum"]
            ):
                if revenue_col is not None:
                    answer = (
                        f"💰 Total revenue is "
                        f"{df[revenue_col].sum():,.2f}."
                    )

            # AVERAGE REVENUE
            elif "average revenue" in q or "mean revenue" in q:
                if revenue_col is not None:
                    avg = df[revenue_col].mean()
                    answer = f"📊 Average revenue is {avg:,.2f}."

            # HIGHEST REVENUE PRODUCT
            elif (
                product_col is not None
                and revenue_col is not None
                and "revenue" in q
                and any(word in q for word in [
                    "highest", "most", "top", "maximum", "best"
                ])
            ):
                totals = df.groupby(product_col)[revenue_col].sum()

                if not totals.empty:
                    product = totals.idxmax()
                    answer = (
                        f"🏆 {product} has the highest revenue: "
                        f"{totals.max():,.2f}."
                    )

            # LOWEST REVENUE PRODUCT
            elif (
                product_col is not None
                and revenue_col is not None
                and "revenue" in q
                and any(word in q for word in [
                    "lowest", "least", "minimum"
                ])
            ):
                totals = df.groupby(product_col)[revenue_col].sum()

                if not totals.empty:
                    product = totals.idxmin()
                    answer = (
                        f"📉 {product} has the lowest revenue: "
                        f"{totals.min():,.2f}."
                    )

            # TOTAL QUANTITY
            elif quantity_col is not None and any(
                phrase in q for phrase in [
                    "total quantity",
                    "total units",
                    "how many units were sold",
                    "total items sold",
                    "total quantity sold"
                ]
            ):
                answer = (
                    f"📦 Total quantity sold is "
                    f"{df[quantity_col].sum():,.0f} units."
                )

            # MOST UNITS SOLD
            elif (
                quantity_col is not None
                and product_col is not None
                and any(word in q for word in [
                    "most", "highest", "maximum", "top"
                ])
                and any(word in q for word in [
                    "units", "quantity", "sold"
                ])
            ):
                totals = df.groupby(product_col)[quantity_col].sum()

                if not totals.empty:
                    product = totals.idxmax()
                    answer = (
                        f"🥇 {product} sold the most units: "
                        f"{totals.max():,.0f}."
                    )

            # SHOW ALL PRODUCTS
            elif (
                product_col is not None
                and any(phrase in q for phrase in [
                    "show all products",
                    "list products",
                    "what products",
                    "which products",
                    "all products"
                ])
            ):
                products = (
                    df[product_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                answer = "🛍️ Products: " + ", ".join(products)

            # HIGHEST REVENUE CATEGORY
            elif (
                category_col is not None
                and revenue_col is not None
                and "category" in q
                and any(word in q for word in [
                    "highest", "most", "top", "best"
                ])
            ):
                totals = df.groupby(category_col)[revenue_col].sum()

                if not totals.empty:
                    category = totals.idxmax()
                    answer = (
                        f"🏆 {category} has the highest revenue: "
                        f"{totals.max():,.2f}."
                    )

            # PRODUCT-SPECIFIC QUESTION
            if answer is None and product_col is not None:

                product_names = (
                    df[product_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                matched_product = None

                for product in sorted(
                    product_names,
                    key=len,
                    reverse=True
                ):
                    if product.lower() in q:
                        matched_product = product
                        break

                if matched_product is not None:

                    product_rows = df[
                        df[product_col].astype(str).str.lower()
                        == matched_product.lower()
                    ]

                    # PRODUCT PRICE
                    if (
                        price_col is not None
                        and any(word in q for word in [
                            "price", "cost", "unit price"
                        ])
                    ):
                        price = product_rows[price_col].dropna()

                        if not price.empty:
                            answer = (
                                f"💵 {matched_product} unit price is "
                                f"{price.iloc[0]:,.2f}."
                            )

                    # PRODUCT QUANTITY
                    elif (
                        quantity_col is not None
                        and any(word in q for word in [
                            "how many", "quantity", "units", "sold"
                        ])
                    ):
                        qty = product_rows[quantity_col].sum()

                        answer = (
                            f"📦 {matched_product}: "
                            f"{qty:,.0f} units sold."
                        )

                    # PRODUCT REVENUE
                    elif revenue_col is not None and "revenue" in q:
                        rev = product_rows[revenue_col].sum()

                        answer = (
                            f"💰 {matched_product} total revenue is "
                            f"{rev:,.2f}."
                        )

            if answer:
                st.success(answer)
            else:
                st.warning(
                    "I couldn't understand that question yet. "
                    "Try one of the example questions above."
                )


# ---------------- DATA QUALITY TAB ----------------
with tab4:
    st.subheader("📋 Data Quality Report")

    quality = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(dtype) for dtype in df.dtypes],
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": [
            round(df[col].isna().mean() * 100, 2)
            for col in df.columns
        ],
        "Unique Values": [
            df[col].nunique(dropna=True)
            for col in df.columns
        ]
    })

    st.dataframe(quality, use_container_width=True)

    duplicate_count = int(df.duplicated().sum())

    st.metric("Duplicate Rows", duplicate_count)

    if missing_values == 0 and duplicate_count == 0:
        st.success("No missing values or duplicate rows detected.")
    else:
        st.info(
            "Review the report above to identify missing values "
            "and duplicate rows."
        )


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "DataTalk V3 | Intelligent Conversational Analytics System"
)