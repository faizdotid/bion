const mongoose = require("mongoose");
const Product = require("./models/Product");
require("dotenv").config();

const products = [
  {
    name: "Laptop ASUS ROG",
    description: "Laptop gaming ngebut",
    price: 15000000,
    category: "Elektronik",
    stock: 10,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "iPhone 15 Pro",
    description: "HP dengan kamera bagus polll",
    price: 18000000,
    category: "Elektronik",
    stock: 15,
    image: "https://picsum.photos/200/300",
  },
  {
    name: 'Samsung Smart TV 55"',
    description: "TV canggih pokoknya",
    price: 8500000,
    category: "Elektronik",
    stock: 8,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "Nike Air Max 2024",
    description: "Sepatu aja sih",
    price: 1500000,
    category: "Fashion",
    stock: 25,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "Sony WH-1000XM5",
    description: "Headphone noise-cancelling, prefer beli nasi goreng sih saya",
    price: 4500000,
    category: "Elektronik",
    stock: 12,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "Mechanical Keyboard RGB",
    description: "Keyboard berisik intinya",
    price: 1200000,
    category: "Aksesoris",
    stock: 20,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "Gaming Mouse Logitech",
    description: "Mouse aja",
    price: 800000,
    category: "Aksesoris",
    stock: 30,
    image: "https://picsum.photos/200/300",
  },
  {
    name: "Smartwatch Samsung Galaxy",
    description: "Jam tangan tapi modern",
    price: 3500000,
    category: "Elektronik",
    stock: 18,
    image: "https://picsum.photos/200/300",
  },
];

const seedDatabase = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI);

    console.log("Terhubung ke MongoDB");

    // Hapus data lama
    await Product.deleteMany();
    console.log("Data lama berhasil dihapus");

    // Insert data baru
    // await Product.insertMany(products);

    for (const item of products) {
      const response = await fetch("https://picsum.photos/200/300", {
        method: "GET",
        redirect: "follow",
      });
      if (!response.ok) {
        console.error(await response.url);
        continue;
      }
      item.image = response.url;
      const product = new Product(item);
      await product.save();
    }
    console.log("Data dummy berhasil ditambahkan");
    console.log(`Total produk: ${products.length}`);

    process.exit(0);
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
};

seedDatabase();
