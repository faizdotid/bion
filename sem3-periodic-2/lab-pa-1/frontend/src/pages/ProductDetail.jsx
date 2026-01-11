import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router";
import productService from "../services/productService";
import "./ProductDetail.css";

export function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const response = await productService.getProductById(id);
      setProduct(response.data);
      setError(null);
    } catch (err) {
      setError("Produk tidak ditemukan");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(price);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Memuat detail produk...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="error-container">
        <p className="error-message">❌ {error}</p>
        <button onClick={() => navigate("/products")} className="btn btn-back">
          Kembali ke Daftar Produk
        </button>
      </div>
    );
  }

  return (
    <div className="product-detail-page">
      <div className="container">
        <button
          onClick={() => navigate("/products")}
          className="btn-back-simple"
        >
          ← Kembali
        </button>

        <div className="product-detail-container">
          <div className="product-image-section">
            <img src={product.image} alt={product.name} />
          </div>

          <div className="product-info-section">
            <span className="product-category-badge">{product.category}</span>
            <h1>{product.name}</h1>

            <div className="price-section">
              <span className="price">{formatPrice(product.price)}</span>
              <span
                className={`stock-badge ${
                  product.stock > 5 ? "in-stock" : "low-stock"
                }`}
              >
                {product.stock > 0 ? `Stok: ${product.stock}` : "Habis"}
              </span>
            </div>

            <div className="description-section">
              <h3>Deskripsi Produk</h3>
              <p>{product.description}</p>
            </div>

            <div className="product-specs">
              <div className="spec-item">
                <span className="spec-label">Kategori:</span>
                <span className="spec-value">{product.category}</span>
              </div>
              <div className="spec-item">
                <span className="spec-label">Ketersediaan:</span>
                <span className="spec-value">
                  {product.stock > 0 ? "Tersedia" : "Tidak Tersedia"}
                </span>
              </div>
              <div className="spec-item">
                <span className="spec-label">ID Produk:</span>
                <span className="spec-value">{product._id}</span>
              </div>
            </div>

            <div className="action-buttons">
              <button
                onClick={() => {
                  alert("Fitur beli belum tersedia");
                }}
                className="btn btn-buy"
                disabled={product.stock === 0}
              >
                {product.stock > 0 ? "🛒 Beli Sekarang" : "Stok Habis"}
              </button>
              <button
                onClick={() => alert("Fitur wishlist belum tersedia")}
                className="btn btn-cart"
              >
                💙 Tambah ke Wishlist
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
