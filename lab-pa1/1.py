# Clustering dengan GMM & EM Algorithm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
import warnings

warnings.filterwarnings("ignore")

# Set random seed
np.random.seed(42)

# Generate data menggunakan make_blobs
X, y_true = make_blobs(
    n_samples=300, centers=3, random_state=42, cluster_std=1.5, center_box=(-10.0, 10.0)
)

print(f"Dataset dibuat: {X.shape[0]} samples, {X.shape[1]} features")
print(f"Jumlah cluster asli: {len(np.unique(y_true))}")


# KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
y_kmeans = kmeans.fit_predict(X)

# Gaussian Mixture Model
gmm = GaussianMixture(n_components=3, random_state=42, covariance_type="full")
y_gmm = gmm.fit_predict(X)

# Probabilitas untuk setiap cluster (untuk visualisasi confidence)
gmm_proba = gmm.predict_proba(X)
gmm_confidence = np.max(gmm_proba, axis=1)

# Visualisasi hasil clustering
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle(
    "Perbandingan KMeans vs Gaussian Mixture Model", fontsize=16, fontweight="bold"
)

# Color maps
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

# Plot 1: Data asli (Ground Truth)
for i in range(3):
    mask = y_true == i
    axes[0, 0].scatter(
        X[mask, 0], X[mask, 1], c=colors[i], alpha=0.7, s=50, label=f"Cluster {i}"
    )
axes[0, 0].set_title("Data Asli (Ground Truth)", fontweight="bold")
axes[0, 0].set_xlabel("Feature 1")
axes[0, 0].set_ylabel("Feature 2")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: KMeans hasil
for i in range(3):
    mask = y_kmeans == i
    axes[0, 1].scatter(
        X[mask, 0], X[mask, 1], c=colors[i], alpha=0.7, s=50, label=f"Cluster {i}"
    )

# Tambahkan centroid KMeans
centers = kmeans.cluster_centers_
axes[0, 1].scatter(
    centers[:, 0],
    centers[:, 1],
    c="red",
    marker="x",
    s=200,
    linewidths=3,
    label="Centroids",
)
axes[0, 1].set_title("KMeans Clustering", fontweight="bold")
axes[0, 1].set_xlabel("Feature 1")
axes[0, 1].set_ylabel("Feature 2")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: GMM hasil
for i in range(3):
    mask = y_gmm == i
    axes[1, 0].scatter(
        X[mask, 0], X[mask, 1], c=colors[i], alpha=0.7, s=50, label=f"Cluster {i}"
    )
axes[1, 0].set_title("Gaussian Mixture Model", fontweight="bold")
axes[1, 0].set_xlabel("Feature 1")
axes[1, 0].set_ylabel("Feature 2")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: GMM dengan confidence level
scatter_conf = axes[1, 1].scatter(
    X[:, 0], X[:, 1], c=gmm_confidence, cmap="RdYlBu", alpha=0.7, s=50
)
axes[1, 1].set_title("GMM - Confidence Level", fontweight="bold")
axes[1, 1].set_xlabel("Feature 1")
axes[1, 1].set_ylabel("Feature 2")
cbar = plt.colorbar(scatter_conf, ax=axes[1, 1])
cbar.set_label("Confidence Level")
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nEvaluasi hasil clustering:")


# Adjusted Rand Index (mengukur similarity dengan ground truth)
kmeans_ari = adjusted_rand_score(y_true, y_kmeans)
gmm_ari = adjusted_rand_score(y_true, y_gmm)

# Silhouette Score (mengukur kualitas clustering internal)
kmeans_silhouette = silhouette_score(X, y_kmeans)
gmm_silhouette = silhouette_score(X, y_gmm)

print("KMeans:")
print(f"  - Adjusted Rand Index: {kmeans_ari:.4f}")
print(f"  - Silhouette Score: {kmeans_silhouette:.4f}")

print("\nGaussian Mixture Model:")
print(f"  - Adjusted Rand Index: {gmm_ari:.4f}")
print(f"  - Silhouette Score: {gmm_silhouette:.4f}")

# Analisis tambahan GMM
print("\nAnalisis tambahan GMM:")
print(f"Log-likelihood: {gmm.score(X):.4f}")
print(f"AIC: {gmm.aic(X):.4f}")
print(f"BIC: {gmm.bic(X):.4f}")

# Tampilkan mean confidence untuk setiap cluster
for i in range(3):
    mask = y_gmm == i
    mean_conf = gmm_confidence[mask].mean()
    print(f"Mean confidence Cluster {i}: {mean_conf:.4f}")


# Contoh prediksi probabilitas untuk beberapa titik
print("\nContoh probabilitas keanggotaan (5 titik pertama):")
print("Point | Cluster 0 | Cluster 1 | Cluster 2 | Predicted")
print("-" * 55)
for i in range(5):
    probs = gmm_proba[i]
    pred = y_gmm[i]
    print(f"{i:5d} | {probs[0]:8.4f} | {probs[1]:8.4f} | {probs[2]:8.4f} | {pred:9d}")
