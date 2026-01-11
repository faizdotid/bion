import { Link } from "react-router";
import "./Navbar.css";

export function Navbar() {
  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="logo">
          🛒 Toko Online
        </Link>
        <ul className="nav-menu">
          <li>
            <Link to="/">Beranda</Link>
          </li>
          <li>
            <Link to="/products">Produk</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
