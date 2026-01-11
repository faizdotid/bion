import { Link } from "react-router";
import "./Home.css";

export function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1>Selamat Datang di Toko Online</h1>
          <p>Temukan produk terbaik dengan harga termurah</p>
          <Link to="/products" className="btn btn-hero">
            Lihat Produk
          </Link>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2>Mengapa Berbelanja di Sini?</h2>
          <div className="feature-grid">
            <div className="feature-item">
              <h3>Pengiriman Cepat</h3>
              <p>Pengiriman ke seluruh Indonesia dengan cepat dan aman</p>
            </div>
            <div className="feature-item">
              <h3>Pembayaran Mudah</h3>
              <p>Berbagai metode pembayaran yang aman dan terpercaya</p>
            </div>
            <div className="feature-item">
              <h3>Produk Berkualitas</h3>
              <p>Produk original dengan kualitas terjamin</p>
            </div>
            <div className="feature-item">
              <h3>Promo Menarik</h3>
              <p>Dapatkan promo dan diskon spesial setiap hari</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta">
        <div className="container">
          <h2>Mulai Belanja Sekarang!</h2>
          <p>Jangan lewatkan penawaran terbaik kami</p>
          <Link to="/products" className="btn btn-cta">
            Jelajahi Produk
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;
