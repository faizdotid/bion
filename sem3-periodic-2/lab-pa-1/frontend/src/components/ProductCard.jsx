import { Link } from "react-router";
import "./ProductCard.css";

export function ProductCard({ product }) {
  const formatPrice = (price) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.image} alt={product.name} />
        {product.stock <= 5 && product.stock > 0 && (
          <span className="badge badge-warning">Stok Terbatas</span>
        )}
        {product.stock === 0 && (
          <span className="badge badge-danger">Habis</span>
        )}
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-category">{product.category}</p>
        <p className="product-price">{formatPrice(product.price)}</p>
        <p className="product-stock">Stok: {product.stock}</p>
        <Link to={`/products/${product._id}`} className="btn btn-primary">
          Lihat Detail
        </Link>
      </div>
    </div>
  );
}

export default ProductCard;
