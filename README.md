---
title: "Dokumentasi Sistem Inventori Toko"
author: "Kelommpok 18"
date: "`r Sys.Date()`"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## 🛒 Sistem Inventori Toko

**Sistem Inventori Toko** adalah aplikasi berbasis Python yang dirancang untuk mempermudah pengelolaan stok barang, transaksi keluar-masuk, dan pelaporan. Sistem ini memiliki antarmuka yang ramah pengguna dan mendukung berbagai peran: **Admin**, **Karyawan**, **Supplier**, dan **Pembeli**.

---

## 💡 Fitur Utama

### 🔐 Login & Logout
Semua jenis pengguna dapat melakukan login dan logout sesuai akun masing-masing.

---

### 👤 Admin

#### 1. CRUD User
- **Create**: Menambahkan akun pengguna baru (admin, karyawan, supplier, pembeli).
- **Read**: Melihat daftar pengguna yang telah terdaftar.
- **Update**: Mengubah data pengguna.
- **Delete**: Menghapus akun pengguna dari sistem.

#### 2. CRUD Barang
- **Create**: Menambahkan barang baru ke dalam sistem.
- **Read**: Melihat daftar semua barang (fitur **Lihat Daftar Barang**).
- **Update**: Mengedit data barang, seperti nama, kategori, harga, atau stok (**Edit Data Barang**).
- **Delete**: Menghapus barang dari sistem (**Hapus Data Barang**).

#### 3. CRUD Kategori
- Mengelola kategori barang yang tersedia (tambah, lihat, ubah, hapus).

#### 4. Cari & Data
- Mencari barang berdasarkan nama atau ID.
- Menampilkan data dalam bentuk tabel.

#### 5. Laporan Transaksi Barang
- Menampilkan riwayat transaksi masuk dan keluar barang.

---

### 👨‍🔧 Karyawan

#### 1. RUD User
- **Read**: Melihat daftar pengguna (supplier dan pembeli).
- **Update**: Mengubah data supplier atau pembeli.
- **Delete**: Menghapus akun supplier atau pembeli.

#### 2. CRUD Barang
- Sama seperti admin: bisa menambahkan, melihat, mengedit, dan menghapus barang.

#### 3. CRUD Kategori
- Mengelola kategori barang (tambah, lihat, ubah, hapus).

#### 4. Cari & Data
- Mencari barang dan menampilkan data sesuai kebutuhan.

#### 5. Laporan Transaksi Barang
- Melihat laporan transaksi barang yang terjadi selama periode tertentu.

---

### 🚚 Supplier

#### 1. CRUD Barang (Milik Sendiri)
- **Create**: Menambahkan barang yang dimiliki sendiri ke dalam sistem.
- **Read**: Melihat daftar barang milik sendiri.
- **Update**: Mengedit barang yang dimiliki.
- **Delete**: Menghapus barang milik sendiri dari sistem.

#### 2. Cari & Sorting Barang
- Mencari dan mengurutkan barang milik sendiri berdasarkan harga atau nama.

---

### 🛍️ Pembeli

#### 1. Lihat Daftar Barang
- Melihat semua barang yang tersedia di toko.

#### 2. Beli Barang
- Melakukan pembelian barang yang tersedia.

#### 3. Lihat Riwayat Pembelian
- Menampilkan daftar transaksi pembelian yang telah dilakukan.

#### 4. Cari & Sorting Barang
- Mencari dan mengurutkan barang berdasarkan nama atau harga.

---

### 📁 Ekspor Data JSON
Data yang dapat diekspor dalam format JSON:
- Data Pengguna
- Data Barang
- Laporan Transaksi

---

## 📚 Implementasi Struktur Data & Algoritma

1. **HashMap**
   - Untuk menyimpan data pengguna dan barang secara efisien.

2. **Quick Sort**
   - Untuk mengurutkan data barang saat fitur sorting digunakan.

3. **Linear Search**
   - Untuk pencarian cepat nama barang atau pengguna.

4. **List**
   - Digunakan untuk menyimpan data transaksi pembelian dan penjualan barang.

---

## 🔚 Penutup

Sistem Inventori Toko dirancang dengan mempertimbangkan kemudahan penggunaan, efisiensi pengolahan data, dan penerapan konsep algoritma yang relevan dengan pembelajaran di perguruan tinggi. Sistem ini membantu pengguna dari berbagai peran dalam mengelola data barang dan transaksi secara praktis.
