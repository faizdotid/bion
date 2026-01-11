# Import library yang diperlukan
import pandas as pd
from sklearn.datasets import load_iris
from plotnine import (
    ggplot,
    aes,
    geom_point,
    geom_smooth,
    labs,
    theme_minimal,
    theme,
    element_text,
    scale_color_manual,
)
from scipy import stats

# Import dataset Iris dari sklearn
iris_data = load_iris()
iris_df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
iris_df["species"] = iris_data.target
iris_df["species"] = iris_df["species"].map(
    {0: "setosa", 1: "versicolor", 2: "virginica"}
)

# Rename kolom
iris_df.columns = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species",
]

# Tampilkan informasi dataset
print("Dataset Iris - 5 baris pertama:")
print(iris_df.head())
print(f"\nJumlah data: {len(iris_df)} baris")
print(f"Jumlah spesies: {iris_df['species'].nunique()}")
print(f"Spesies: {list(iris_df['species'].unique())}")

# Membuat scatter plot dengan Grammar of Graphics
plot = (
    ggplot(iris_df, aes(x="sepal_length", y="petal_length", color="species"))
    + geom_point(size=2.5, alpha=0.7)
    + geom_smooth(method="lm", se=True)
    + labs(
        title="Scatter Plot dengan Grammar of Graphics + Regresi",
        x="Sepal Length (cm)",
        y="Petal Length (cm)",
        color="Species",
    )
    + theme_minimal()
    + theme(
        figure_size=(10, 6),
        plot_title=element_text(size=14, weight="bold"),
        legend_position="right",
    )
    + scale_color_manual(values=["#FF6B6B", "#4ECDC4", "#45B7D1"])
)

# Save plot ke dalam png
plot.save("plot2.png")

# Analisis korelasi untuk interpretasi
print("\n=== INTERPRETASI HASIL ===")
print("\n1. Korelasi antara Sepal Length dan Petal Length per spesies:")

for species in iris_df["species"].unique():
    subset = iris_df[iris_df["species"] == species]
    correlation = subset["sepal_length"].corr(subset["petal_length"])
    print(f"   - {species.capitalize()}: r = {correlation:.3f}")

# Statistik deskriptif
print("\n2. Statistik Deskriptif:")
summary_stats = iris_df.groupby("species")[["sepal_length", "petal_length"]].agg(
    ["mean", "std"]
)
print(summary_stats.round(2))

# Interpretasi pola
print("\n3. Interpretasi Pola yang Muncul:")
print("   a) Terdapat hubungan positif yang kuat antara sepal length dan petal length")
print(
    "   b) Spesies Setosa memiliki petal length yang jauh lebih pendek dibanding yang lain"
)
print(
    "   c) Virginica cenderung memiliki ukuran yang paling besar (sepal dan petal length)"
)
print("   d) Versicolor berada di posisi tengah antara Setosa dan Virginica")
print("   e) Setiap spesies menunjukkan pola linear yang jelas antara kedua variabel")
print("   f) Terdapat separasi yang baik antar spesies berdasarkan kedua dimensi ini")

# Menghitung R-squared untuk setiap spesies
print("\n4. Kekuatan Hubungan Linear (R-squared):")

for species in iris_df["species"].unique():
    subset = iris_df[iris_df["species"] == species]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        subset["sepal_length"], subset["petal_length"]
    )
    r_squared = r_value**2
    print(
        f"   - {species.capitalize()}: R² = {r_squared:.3f} (menjelaskan {r_squared * 100:.1f}% variasi)"
    )
