import { useState, useEffect } from "react";
import ProductCard from "../components/ProductCard";
import productService from "../services/productService";
import "./ProductList.css";

export function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await productService.getAllProducts();
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError("Gagal mengambil data produk. Pastikan backend berjalan.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getCategories = () => {
    const categories = [...new Set(products.map((p) => p.category))];
    return categories;
  };

  const filteredProducts =
    filter === "all" ? products : products.filter((p) => p.category === filter);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Memuat produk...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">❌ {error}</p>
        <button onClick={fetchProducts} className="btn btn-retry">
          Coba Lagi
        </button>
      </div>
    );
  }

  return (
    <div className="product-list-page">
      <div className="container">
        <div className="page-header">
          <h1>Daftar Produk</h1>
          <p>Temukan produk yang Anda cari</p>
        </div>

        <div className="filter-section">
          <button
            className={`filter-btn ${filter === "all" ? "active" : ""}`}
            onClick={() => setFilter("all")}
          >
            Semua Produk ({products.length})
          </button>
          {getCategories().map((category) => (
            <button
              key={category}
              className={`filter-btn ${filter === category ? "active" : ""}`}
              onClick={() => setFilter(category)}
            >
              {category} (
              {products.filter((p) => p.category === category).length})
            </button>
          ))}
        </div>

        {filteredProducts.length === 0 ? (
          <div className="no-products">
            <p>Tidak ada produk ditemukan</p>
          </div>
        ) : (
          <div className="product-grid">
            {filteredProducts.map((product) => (
              <ProductCard key={product._id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductList;
