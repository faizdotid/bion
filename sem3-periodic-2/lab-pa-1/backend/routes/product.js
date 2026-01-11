const express = require("express");
const router = express.Router();
const Product = require("../models/Product");

// GET - ambil semua produk
router.get("/", async (req, res) => {
  try {
    const products = await Product.find().sort({ createdAt: -1 });
    res.json({
      success: true,
      count: products.length,
      data: products,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Gagal mengambil data produk",
      error: error.message,
    });
  }
});

// GET - ambil produk berdasarkan ID
router.get("/:id", async (req, res) => {
  try {
    const product = await Product.findById(req.params.id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: "Produk tidak ditemukan",
      });
    }

    res.json({
      success: true,
      data: product,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Gagal mengambil data produk",
      error: error.message,
    });
  }
});

// POST - buat produk baru
router.post("/", async (req, res) => {
  try {
    const product = await Product.create(req.body);

    res.status(201).json({
      success: true,
      message: "Produk berhasil ditambahkan",
      data: product,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Gagal menambahkan produk",
      error: error.message,
    });
  }
});

// PUT - update produk
router.put("/:id", async (req, res) => {
  try {
    const product = await Product.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    if (!product) {
      return res.status(404).json({
        success: false,
        message: "Produk tidak ditemukan",
      });
    }

    res.json({
      success: true,
      message: "Produk berhasil diupdate",
      data: product,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Gagal mengupdate produk",
      error: error.message,
    });
  }
});

// DELETE - hapus produk
router.delete("/:id", async (req, res) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: "Produk tidak ditemukan",
      });
    }

    res.json({
      success: true,
      message: "Produk berhasil dihapus",
      data: {},
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Gagal menghapus produk",
      error: error.message,
    });
  }
});

module.exports = router;
