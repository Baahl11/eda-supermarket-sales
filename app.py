import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data/supermarket_sales.csv")

df = load_data()

# Título del dashboard
st.title("📊 Análisis de Ventas - Supermercado")

# Sidebar con filtros
st.sidebar.header("Filtros")
city = st.sidebar.multiselect(
    "Ciudad",
    options=df["City"].unique(),
    default=df["City"].unique()
)

product_line = st.sidebar.multiselect(
    "Línea de Producto",
    options=df["Product line"].unique(),
    default=df["Product line"].unique()
)

# Filtrar datos
df_filtered = df.query(
    "City == @city & `Product line` == @product_line"
)

# Mostrar métricas
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${df_filtered['Total'].sum():,.0f}")
col2.metric("Transacciones", df_filtered["Invoice ID"].nunique())
col3.metric("Rating Promedio", f"{df_filtered['Rating'].mean():.1f}/10")

# Gráfico 1: Ventas por género
st.subheader("Ventas por Género")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(
    x="Gender", 
    y="Total", 
    data=df_filtered.groupby("Gender")["Total"].sum().reset_index(),
    ax=ax1
)
st.pyplot(fig1)

# Gráfico 2: Ventas por producto
st.subheader("Ventas por Producto")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="Total", 
    y="Product line", 
    data=df_filtered.groupby("Product line")["Total"].sum().reset_index().sort_values("Total", ascending=False),
    palette="viridis",
    ax=ax2
)
st.pyplot(fig2)

# Mostrar tabla de datos
st.subheader("Datos Crudos")
st.dataframe(df_filtered)