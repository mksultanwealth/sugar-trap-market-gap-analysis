#  The Sugar Trap: Market Gap Analysis

## A. Executive Summary

Helix CPG Partners engaged us to identify a “Blue Ocean” opportunity in the global snack aisle using real-world product data. By analyzing 30,000 products from the Open Food Facts dataset, we identified a significant market gap in the High-Protein, Low-Sugar segment. The Nutrient Matrix visualization reveals that most snack products cluster in high-sugar regions, while very few meet the ≥10g protein and ≤5g sugar threshold per 100g. The strongest opportunity lies in Snack Bars and Nuts & Seeds categories, suggesting a clear innovation pathway for a protein-forward, low-sugar product line.

---

## B. Project Links

📓 Notebook: https://github.com/mksultanwealth/sugar-trap-market-gap-analysis/blob/main/sugar_trap_analysis.ipynb

📊 Interactive Dashboard (Streamlit):   https://sugar-trap.streamlit.app/

📽 Presentation Slides: https://docs.google.com/presentation/d/1sCi6ivCoTGv3WdxiP7o_CCJj5eJD63gIfT5QFhy26cU/edit?usp=sharing

---

## C. Technical Explanation

### Data Cleaning

The dataset was filtered to ensure analytical reliability:
- Removed rows with missing product_name, sugars_100g, or proteins_100g.
- Removed biologically unrealistic values:
  - Sugars between 0–100g per 100g
  - Proteins between 0–80g per 100g
  - Fat between 0–100g per 100g
- Limited dataset to 30,000 rows for performance and reproducibility.

All file paths use relative paths to ensure portability.

---

### Category Engineering

The `categories_tags` column was parsed and normalized to lowercase.  
Keyword-based logic was used to assign a Primary Category into the following high-level buckets:

- Snack Bars
- Chocolate & Candy
- Biscuits & Cookies
- Nuts & Seeds
- Protein Products
- Other Snacks

This allowed for clean segmentation and interactive filtering in the dashboard.

---

### Nutrient Matrix & Market Gap Identification

A scatter plot was created comparing:
- Sugar (g per 100g) on the X-axis
- Protein (g per 100g) on the Y-axis

Threshold lines were added to define the “High-Protein / Low-Sugar” quadrant:

- High Protein: ≥10g
- Low Sugar: ≤5g

Products in this quadrant were highlighted dynamically in the dashboard to identify Blue Ocean opportunities.

---



## How to Run Locally

1. Clone the repository.
2. Install dependencies:

