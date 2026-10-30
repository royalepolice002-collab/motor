# MotorKita

Katalog motor Indonesia, dibuat dengan Vite dan JavaScript. Frontend statis tanpa backend berbayar, cocok untuk Cloudflare Pages Free. Tidak ada layanan hosting lain atau pembayaran yang terintegrasi.

## Pengembangan

Node.js 22+, lalu:

```sh
npm ci
npm run dev
```

```sh
npm run build
npm run preview
```

## Deploy hanya ke Cloudflare Pages melalui GitHub

1. Pastikan perubahan di branch `arena/4c74e579-motor` sudah dipush ke GitHub.
2. Masuk dashboard Cloudflare → Workers & Pages → Create → Pages → Connect to Git.
3. Hubungkan GitHub dan pilih repositori `royalepolice002-collab/motor`.
4. Nama project: `motorkita` (jika tersedia).
5. Production branch: `arena/4c74e579-motor`. Jika PR nanti digabung ke main, ubah production branch ke `main`.
6. Framework preset: **Vite**. Build command: **npm run build**. Build output directory: **dist**. Root directory: `/` (root repositori).
7. Environment variable: `NODE_VERSION=22` bila diperlukan. Tidak ada secret frontend yang dibutuhkan.
8. Pilih Save and Deploy. Cloudflare menyediakan alamat `*.pages.dev`; nama persis bergantung ketersediaan. Push berikutnya memicu build otomatis.

Cloudflare Pages Free cukup untuk situs statis ini, sesuai kuota dan ketentuan Cloudflare yang berlaku. Domain kustom opsional, biaya registrasi domain tidak termasuk. Repo ini tidak otomatis menyediakan akun Cloudflare atau mengklaim situs sudah online.

## Fitur

- Dashboard responsif, kategori, pencarian, filter merek, pengurutan harga.
- Dua belas contoh motor dari 11 merek dengan detail dan 48 foto referensi web; daftar filter mencakup 40 merek. Merek tanpa data menampilkan keadaan kosong, bukan stok palsu.
- Favorit disimpan lokal pada browser, tanpa akun.
- Simulasi kredit flat, DP/tenor/bunga dapat diubah; tabel referensi enam penyedia menggunakan asumsi bunga yang sama, bukan tarif resmi.
- Panduan cash/kredit, informasi pembayaran, syarat dan privasi.
- Halaman kontak dengan animasi peta ilustratif dan placeholder sosial media yang dijelaskan dengan jujur.

## Sebelum digunakan sebagai situs jual beli sungguhan

- Ganti data contoh di `src/main.js` dengan harga, stok, tahun model, varian, dan spesifikasi terverifikasi. Saat ini harga hanya referensi OTR Jakarta, bukan feed harga terkini.
- **Verifikasi izin komersial 48 foto referensi web** sebelum publikasi komersial. Sumber dan status hak cipta tercatat di `src/photos.json` dan ditampilkan di galeri. Foto dari sumber berbeda dapat menampilkan tahun/varian/pasar berbeda, bukan stok toko. Hero masih ilustrasi SVG.
- Lengkapi data semua model/merek yang ingin dijual; daftar ini belum merupakan katalog lengkap Indonesia.
- Isi alamat, koordinat, jam buka, WhatsApp, email, dan URL sosial resmi. Peta saat ini bukan peta navigasi.
- Verifikasi perjanjian dengan leasing dan tarif aktual sebelum menampilkan penawaran resmi. Nama perusahaan bukan bukti kemitraan.
- Tambahkan integrasi pembayaran melalui penyedia resmi dan backend aman bila ingin menerima transaksi. Tidak ada pengajuan kredit, checkout, atau pengumpulan KTP di versi ini.
- Google Fonts opsional di CSS; fallback sans-serif tetap berjalan bila akses font gagal.

## Rumus simulasi

Pokok = harga × (1 − DP%). Bunga total = pokok × bunga flat tahunan × tenor / 12. Cicilan = (pokok + bunga total) / tenor. Total bayar = DP + pokok + bunga total. Belum termasuk biaya administrasi, provisi, asuransi, fidusia, dan biaya lain. Teaser kartu memakai DP 30%, tenor 36 bulan, bunga flat 8% per tahun.

## Galeri dan pemesanan WhatsApp

- Masing-masing dari 12 model memiliki empat file foto web lokal di `public/photos/`, dengan sumber pada `src/photos.json`. File lokal tidak bergantung pada hotlink saat pengunjung membuka situs.
- Foto yang ditemukan melalui pencarian web bukan otomatis bebas lisensi. Watermark tidak dihapus. Pastikan izin dari pemilik sumber atau ganti dengan foto stok toko yang dimiliki sendiri sebelum penggunaan komersial.
- Hover mouse selama 320 ms membuka ringkasan harga/spesifikasi dan tombol tindakan. Keluar kartu, tombol ×, atau Escape menutup ringkasan. Klik foto/nama/kartu membuka galeri dialog; tombol panah, thumbnail, serta panah keyboard mengganti foto. Pada layar sentuh gunakan ketuk.
- Untuk mengaktifkan WhatsApp, salin `.env.example` ke `.env.local`, lalu isi `VITE_WHATSAPP_NUMBER` dengan nomor bisnis Indonesia asli dalam format `62...` (tanpa +). Di Cloudflare Pages tambahkan variabel yang sama ke build environment lalu deploy ulang. Ini nomor publik, bukan secret.
- Jika nomor belum terisi/valid, tombol menampilkan informasi bahwa kontak belum tersedia, tanpa membuka chat ke nomor fiktif.
- Pesan WhatsApp menyertakan nama motor dan harga referensi, bukan pesanan otomatis atau konfirmasi pembayaran.
- Empat model tambahan: TVS Ronin, Royal Enfield Hunter 350, United T1800, dan Yadea G6. Harga/spesifikasi tetap referensi indikatif, bukan feed dealer.

## Pengujian

`npm test` menjalankan pemeriksaan galeri empat foto, sumber/file foto, filter merek, favorit, hover, simulasi sesuai motor, serta WhatsApp dengan/tanpa nomor. `npm run build` memvalidasi bundle produksi. Pengujian interaksi memakai jsdom, bukan browser visual.

## Kontak bisnis aktif

Nomor WhatsApp dari pemilik: **08999329143**, dinormalisasi menjadi **628999329143** untuk tautan `wa.me`. Nomor ini menjadi default publik, sehingga tombol pemesanan langsung aktif tanpa environment variable. `VITE_WHATSAPP_NUMBER` tetap dapat digunakan untuk menggantinya saat build.

## Colorful interface update

- Compact, centered-in-card shortcut popover replaces the downward-expanding detail panel. Three icon actions: WhatsApp, specifications/gallery, and credit simulation. Hover/focus or tap the product photo opens it; × and Escape dismiss it.
- Header and sidebar link to a social-media page. Only WhatsApp is configured; other social accounts remain explicitly pending.
- Expanded brand filter directory (not additional inventory). The catalog still contains 12 models from 11 brands; brands with no records show an empty state.
- Colorful gradients, animated hero accents, entry transitions, and hover motion; reduced-motion preferences are respected.
- Six locally stored financing logos in the lower section link to the educational simulator. No official support or partnership is claimed. Logo attribution: `public/leasing/SOURCES.md`.
