# Latihan Ujian Universitas Terbuka · Sistem Informasi

Kumpulan **277 soal pilihan ganda** dan **43 latihan esai** untuk persiapan ujian akhir Universitas Terbuka (UT), program studi Sistem Informasi. Saat ini berisi **semester 1**; semester berikutnya ditambahkan di repo yang sama. Bisa dipakai langsung di browser, tanpa instalasi dan tanpa internet.

> **Tidak resmi.** Proyek ini tidak berafiliasi dengan Universitas Terbuka. Soal-soalnya adalah **latihan buatan sendiri** berdasarkan materi tutorial dan rangkuman Buku Materi Pokok (BMP), **bukan bocoran soal ujian**. Gunakan sebagai pendamping BMP, bukan pengganti.

## Mata kuliah · Semester 1

| Kode | Mata kuliah | Soal | Esai | BMP acuan |
|---|---|---|---|---|
| MKDI4201 | Bahasa Inggris | 26 | 7 | MKWI4201 |
| MKWN4101 | Pendidikan Agama Islam | 20 | 7 | MKWN4101 |
| MKWN4109 | Pendidikan Kewarganegaraan | 20 | 7 | MKWN4109 |
| STMA4112 | Matematika Dasar | 61 | 7 | MATA4101 |
| STSI4101 | Pengantar Sistem Informasi | 52 | 5 | EMBS4321 |
| STSI4102 | Algoritma dan Pemrograman | 47 | 5 | MSIM4203 |
| STSI4103 | Sistem Operasi | 51 | 5 | MSIM4201 |

## Fitur

### Dashboard dan perkiraan nilai
- **Perkiraan nilai ujian (0–100) ± rentang** muncul setelah 20 soal dijawab, lengkap dengan status *Siap* (≥80), *Hampir siap* (65–79), atau *Perlu belajar lagi* (<65).
- **Progres per sesi:** batang menunjukkan berapa soal sudah dijawab, warnanya menunjukkan akurasi. Klik untuk langsung berlatih sesi itu.
- **Rekomendasi fokus:** sesi dengan akurasi terendah, atau sesi yang belum dicoba.
- **Statistik:** akurasi, jumlah soal yang pernah dijawab, soal yang dikuasai, dan jumlah hari belajar berturut-turut.
- **Riwayat simulasi:** grafik 10 simulasi terakhir, termasuk naik-turunnya skor.
- **Halaman utama dan halaman semester** menampilkan perkiraan nilai tiap mata kuliah serta rata-ratanya per semester.

**Cara menghitung perkiraan.** Soal yang pernah dijawab memakai hasil jawaban terakhir. Soal yang belum pernah dijawab dihitung 25%, setara menebak satu dari empat pilihan. Jika ada simulasi, rata-rata tiga simulasi terakhir ikut dihitung dengan bobot setengah. Rentangnya mengecil saat makin banyak soal dijawab. Angka ini **perkiraan kasar dari latihan**, bukan jaminan nilai ujian, karena soal ujian asli bisa berbeda.

### Mode latihan
1. **Latihan per sesi.** Jawaban dan penjelasan langsung muncul, disertai progress bar dan skor berjalan.
2. **Simulasi ujian.** 20, 30, atau 50 soal acak dengan batas waktu 30, 60, atau 90 menit. Skor, perbandingan dengan simulasi sebelumnya, dan pembahasan soal yang salah muncul di akhir. Jumlah soal dan waktunya hanya untuk latihan, bukan aturan resmi UT.
3. **Ulangi yang salah.** Hanya menampilkan soal yang pernah dijawab salah. Soal keluar dari daftar setelah dijawab benar.
4. **Kartu hafalan.** Tebak jawabannya dalam kepala, lalu buka kuncinya.
5. **Latihan esai.** Tulis jawaban sendiri, lalu cocokkan dengan poin kunci.

### Kenyamanan pemakaian
- Layar pertama langsung berisi tombol **Lanjut** ke sesi yang paling perlu dilatih, dan tombol **Ulangi soal salah**.
- **Pintasan keyboard:** `A`–`D` atau `1`–`4` untuk menjawab, `Enter` untuk lanjut; di kartu hafalan, `Spasi` untuk membuka jawaban.
- Benar-salah ditandai dengan warna **dan** teks (✓ Benar / ✗ Kurang tepat), pilihan berlabel huruf, tombol cukup besar untuk layar sentuh, serta mendukung mode gelap dan pembaca layar.
- Saat simulasi, sisa waktu berubah merah di 5 menit terakhir. Tombol **Akhiri simulasi** meminta konfirmasi agar tidak tertekan tanpa sengaja.

Urutan pilihan jawaban diacak setiap kali tampil. Semua progres tersimpan di browser Anda sendiri lewat `localStorage`, tidak dikirim ke mana pun. Tombol **Hapus riwayat** perlu diklik dua kali agar tidak terhapus tanpa sengaja.

## Cara memakai

Tidak perlu memasang apa pun. Cukup browser modern seperti Chrome, Edge, Firefox, atau Safari, di laptop maupun HP.

### Pilihan 1: unduh dan buka
1. Di halaman GitHub ini, klik **Code → Download ZIP**.
2. Ekstrak ZIP-nya.
3. Klik dua kali **`index.html`**, lalu pilih semester dan mata kuliah.

### Pilihan 2: buka online lewat GitHub Pages
Pemilik repo bisa mengaktifkan **Settings → Pages → Branch: `main` / root → Save**. Setelah satu atau dua menit, latihan bisa dibuka di `https://<username>.github.io/<nama-repo>/`.

### Pilihan 3: clone dengan Git
```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
```
Lalu buka `index.html` di browser.

**Catatan:** riwayat latihan tersimpan per browser dan per perangkat. Membuka di browser lain, mode penyamaran, atau setelah menghapus data situs akan mulai dari nol.

## Struktur folder

```
.
├── index.html                 # Halaman utama: daftar semester
├── semester-1/
│   ├── index.html             # Daftar mata kuliah semester 1
│   └── soal/
│       ├── MKDI4201.html      # Halaman latihan (hasil build)
│       └── ...
├── src/
│   ├── build.py               # Membuat ulang semua halaman di atas
│   ├── template.html          # Tampilan dan logika halaman latihan
│   └── semester-1/
│       └── soal.py            # Daftar MK, bank soal, dan esai semester 1
└── README.md
```

Setiap file di `semester-N/soal/` berdiri sendiri: data soal, tampilan, dan skrip ada dalam satu file HTML, tanpa library atau koneksi dari luar. Folder `semester-*` di root adalah **hasil build**, jadi jangan diedit langsung; edit `src/` lalu jalankan build.

## Menambah atau memperbaiki soal

Butuh **Python 3.8+**, tanpa paket tambahan.

1. Buka `src/semester-N/soal.py`. Format satu soal pilihan ganda di `SOAL["KODE"]`:
   ```python
   (sesi, "Teks soal ...", ["Opsi A", "Opsi B", "Opsi C", "Opsi D"], indeks_kunci, "Penjelasan singkat (boleh kosong)"),
   ```
   - `sesi` adalah nomor sesi tutorial (1–9).
   - `indeks_kunci` dihitung dari 0, jadi `0` berarti opsi pertama.

   Format satu esai di `ESAI["KODE"]`:
   ```python
   ("Pertanyaan esai ...", "Poin-poin jawaban kunci ..."),
   ```
2. Bangun ulang semua halaman:
   ```bash
   python3 src/build.py
   ```
   Skrip akan menolak soal yang formatnya salah, punya opsi kembar, atau soal ganda. Semua `index.html` ikut dibuat ulang otomatis.
3. Buka halaman hasilnya di browser untuk mengecek.

## Menambah semester baru

1. Buat folder `src/semester-2/` dan file `soal.py` di dalamnya dengan bentuk yang sama seperti semester 1:
   ```python
   MK = {"KODE1": "Nama Mata Kuliah 1", "KODE2": "Nama Mata Kuliah 2"}
   SOAL = {"KODE1": [ ... ], "KODE2": [ ... ]}
   ESAI = {"KODE1": [ ... ], "KODE2": [ ... ]}
   ```
2. Jalankan `python3 src/build.py`. Folder `semester-2/` dan kartunya di halaman utama akan dibuat otomatis.
3. Tambahkan tabel mata kuliah semester tersebut di README ini.

Kode mata kuliah dipakai sebagai kunci penyimpanan progres, jadi pastikan setiap kode unik di seluruh semester.

## Sumber dan akurasi

- Soal ditulis berdasarkan pemahaman atas materi inisiasi tutorial online dan **rangkuman** BMP, lalu dirumuskan ulang dengan kata-kata sendiri. Teks BMP dan soal Tes Formatif tidak disalin.
- Soal hitungan (Matematika, penjadwalan CPU, penelusuran sorting dan kode Java) sudah dicek manual, tetapi kesalahan tetap mungkin terjadi. Jika menemukan kunci yang keliru, buka **Issue** atau kirim **Pull Request** dengan rujukan halaman BMP.
- Jika ada perbedaan, **BMP edisi terbaru dan tutor Anda yang berlaku**.

## Hak cipta

- Isi BMP dan materi tutorial adalah hak cipta Universitas Terbuka. Repo ini tidak memuat salinan BMP, soal Tes Formatif, maupun soal kuis tutorial.
- Lisensi untuk kode dan soal buatan sendiri di repo ini belum ditetapkan. Jika ingin orang lain bebas memakai ulang, tambahkan file `LICENSE`, misalnya MIT untuk kode dan CC BY-NC 4.0 untuk soal.

## Ikuti dan dukung pembuat

Latihan ini **gratis dan akan tetap gratis**. Ikuti pembuatnya untuk kabar semester berikutnya, atau dukung secara sukarela:

- Instagram: [@himisbah_](https://instagram.com/himisbah_)
- TikTok: [@himisbah](https://www.tiktok.com/@himisbah)
- LinkedIn: [himisbah](https://www.linkedin.com/in/himisbah)
- Saweria: [saweria.co/himisbah](https://saweria.co/himisbah) ☕

Untuk pemilik repo: semua link ini diatur di bagian **Pengaturan** paling atas `src/build.py` (`INSTAGRAM`, `TIKTOK`, `LINKEDIN`, `SAWERIA`, `REPO`). Kosongkan salah satunya untuk menyembunyikan tombolnya, lalu jalankan `python3 src/build.py`.

## Kontribusi

Perbaikan kunci jawaban, soal baru, dan mata kuliah lain sangat diterima. Sertakan rujukan modul atau Kegiatan Belajar di deskripsi Pull Request agar mudah dicek.

Semoga sukses ujiannya! 🎓
