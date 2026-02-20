import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Sugar Trap Dashboard", layout="wide")

st.title("The Sugar Trap: Market Gap Analysis")
st.markdown("Identifying Blue Ocean opportunities in high-protein, low-sugar snacks.")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    # Load the cleaned sample CSV
    df = pd.read_csv("products_sample.csv")

    # Ensure numeric columns are numeric
    df["sugars_100g"] = pd.to_numeric(df["sugars_100g"], errors="coerce")
    df["proteins_100g"] = pd.to_numeric(df["proteins_100g"], errors="coerce")
    df["fat_100g"] = pd.to_numeric(df["fat_100g"], errors="coerce")

    # Drop missing values
    df = df.dropna(subset=["product_name", "sugars_100g", "proteins_100g"])

    # Remove unrealistic values
    df = df[
        (df["sugars_100g"].between(0, 100)) &
        (df["proteins_100g"].between(0, 80)) &
        (df["fat_100g"].between(0, 100))
    ]

    # Category cleaning
    df["categories_tags"] = df["categories_tags"].fillna("").str.lower()

    def assign_primary_category(tags):
        if "bar" in tags:
            return "Snack Bars"
        elif "chocolate" in tags:
            return "Chocolate & Candy"
        elif "biscuit" in tags or "cookie" in tags:
            return "Biscuits & Cookies"
        elif "nuts" in tags or "seeds" in tags:
            return "Nuts & Seeds"
        elif "protein" in tags:
            return "Protein Products"
        else:
            return "Other Snacks"

    df["primary_category"] = df["categories_tags"].apply(assign_primary_category)

    return df


df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["primary_category"].unique(),
    default=df["primary_category"].unique()
)

HIGH_PROTEIN = st.sidebar.slider("High Protein Threshold (g)", 5, 30, 10)
LOW_SUGAR = st.sidebar.slider("Low Sugar Threshold (g)", 1, 20, 5)

filtered_df = df[df["primary_category"].isin(categories)]

# ----------------------------
# Scatter Plot
# ----------------------------
st.subheader("📊 Sugar vs Protein Distribution")

gap_df = filtered_df[
    (filtered_df["proteins_100g"] >= HIGH_PROTEIN) &
    (filtered_df["sugars_100g"] <= LOW_SUGAR)
]

fig, ax = plt.subplots(figsize=(9, 6))

non_gap = filtered_df.drop(gap_df.index)

ax.scatter(
    non_gap["sugars_100g"],
    non_gap["proteins_100g"],
    alpha=0.3,
    label="Other Products"
)

ax.scatter(
    gap_df["sugars_100g"],
    gap_df["proteins_100g"],
    alpha=0.8,
    label="High-Protein Low-Sugar Gap"
)

ax.axvline(LOW_SUGAR, linestyle="--", label=f"Low Sugar ≤ {LOW_SUGAR}g")
ax.axhline(HIGH_PROTEIN, linestyle="--", label=f"High Protein ≥ {HIGH_PROTEIN}g")

ax.set_xlabel("Sugar (g per 100g)")
ax.set_ylabel("Protein (g per 100g)")
ax.set_title("Sugar vs Protein Across Snack Products")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

# ----------------------------
# Blue Ocean Insight
# ----------------------------
st.subheader("🔎 Strategic Insight")

if len(gap_df) > 0:
    top_category = gap_df["primary_category"].value_counts().idxmax()
    st.success(
        f"The largest Blue Ocean opportunity is in **{top_category}**, "
        f"targeting products with ≥ {HIGH_PROTEIN}g protein and ≤ {LOW_SUGAR}g sugar per 100g."
    )
else:
    st.warning(
        "Very few products exist in the high-protein, low-sugar quadrant. "
        "This indicates a strong market gap opportunity."
    )

st.write(f"Total Blue Ocean Products Identified: {len(gap_df)}")

# ----------------------------
# Top Gap Products Table
# ----------------------------
st.subheader("📋 Sample Blue Ocean Products")

if len(gap_df) > 0:
    st.dataframe(
        gap_df[[
            "product_name",
            "primary_category",
            "sugars_100g",
            "proteins_100g",
            "fat_100g"
        ]]
        .sort_values(by="proteins_100g", ascending=False)
        .head(20)
    )
