const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Cek koneksi MongoDB
mongoose
  .connect(process.env.MONGODB_URI)
  .then(() => {
    console.log("Berhasil terhubung ke MongoDB");
  })
  .catch((error) => {
    console.error("Gagal terhubung ke MongoDB:", error.message);
    process.exit(1);
  });

// Routes
app.use("/api/products", require("./routes/product"));

app.get("/", (req, res) => {
  res.json({
    message: "Selamat datang di API Toko Online",
    version: "0.0.1",
    endpoints: {
      products: "/api/products",
    },
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: "Terjadi kesalahan pada server",
    error: err.message,
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "Endpoint tidak ditemukan",
  });
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server berjalan di port ${PORT}`);
  console.log(`Akses API di http://localhost:${PORT}/`);
});
