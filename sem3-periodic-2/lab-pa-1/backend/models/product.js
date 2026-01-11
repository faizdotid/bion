const mongoose = require("mongoose");

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Nama produk harus diisi"],
      trim: true,
    },
    description: {
      type: String,
      required: [true, "Deskripsi produk harus diisi"],
    },
    price: {
      type: Number,
      required: [true, "Harga produk harus diisi"],
      min: [0, "Harga tidak boleh negatif"],
    },
    category: {
      type: String,
      required: [true, "Kategori produk harus diisi"],
    },
    stock: {
      type: Number,
      required: [true, "Stok produk harus diisi"],
      min: [0, "Stok tidak boleh negatif"],
      default: 0,
    },
    image: {
      type: String,
      default: "https://picsum.photos/200/300",
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("Product", productSchema);
