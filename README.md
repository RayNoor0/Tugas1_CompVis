# Aplikasi Sederhana Integratif Computer Vision
## Materi Minggu 3-6: Image Filtering, Edge Detection, Feature Points, dan Camera Geometry

**Nama:** Rayendra Althaf Taraka Noor
**NIM:** 13522107
**Kelas:** IF5152 Computer Vision

---

## Deskripsi Aplikasi

Aplikasi ini mengintegrasikan empat komponen utama Computer Vision:
1. **Image Filtering** - Gaussian, Median, dan Sobel filters
2. **Edge Detection** - Sobel dan Canny dengan analisis threshold
3. **Feature Points** - Harris, SIFT, dan FAST detectors
4. **Camera Geometry** - Transformasi perspektif dan simulasi kalibrasi

## Struktur Folder

```
Tugas1_CompVis/
├── 01_filtering/
│   ├── filtering.py          # Script filtering
│   └── output/               # Output gambar dan tabel parameter
├── 02_edge/
│   ├── edge.py               # Script edge detection
│   └── output/               # Output edge maps dan tabel threshold
├── 03_featurepoints/
│   ├── featurepoints.py      # Script feature detection
│   └── output/               # Output marking dan statistik
├── 04_geometry/
│   ├── geometry.py           # Script transformasi geometri
│   └── output/               # Output overlay dan matriks parameter
├── main_integration.py       # Script utama untuk menjalankan semua modul
├── requirements.txt          # Dependencies
└── README.md                 # File ini
```

## Instalasi dan Setup

### 1. Persyaratan Sistem
- Python 3.7 atau lebih baru
- OpenCV (cv2)
- NumPy
- Pandas
- scikit-image

### 2. Instalasi Dependencies

```bash
# Install menggunakan pip
pip install opencv-python numpy pandas scikit-image

# Atau install dari requirements.txt
pip install -r requirements.txt
```

### 3. Persiapan Gambar Pribadi (Opsional)
- Letakkan file gambar pribadi dengan nama `my_photo.jpg` di folder root
- Format yang didukung: JPG, PNG, BMP
- Gambar akan otomatis dikonversi ke grayscale

## Cara Menjalankan Aplikasi

### Opsi 1: Menjalankan Semua Modul Sekaligus
```bash
python main_integration.py
```

### Opsi 2: Menjalankan Modul Individu
```bash
# Filtering
python 01_filtering/filtering.py

# Edge Detection
python 02_edge/edge.py

# Feature Points
python 03_featurepoints/featurepoints.py

# Geometry
python 04_geometry/geometry.py
```

## Output yang Dihasilkan

### 1. Gambar Standar yang Diproses
- **cameraman.png** - Gambar grayscale 512x512
- **coins.png** - Gambar tumpukan koin
- **checkerboard.png** - Pola kotak catur untuk kalibrasi
- **astronaut.png** - Gambar berwarna (dikonversi ke grayscale)

### 2. File Output per Modul

#### 01_filtering/output/
- Gambar asli dan hasil filtering
- `tabel_parameter_filtering.csv` - Parameter semua filter

#### 02_edge/output/
- Edge maps dari berbagai metode dan parameter
- `tabel_parameter_edge.csv` - Threshold dan sampling analysis

#### 03_featurepoints/output/
- Gambar dengan feature points yang ditandai
- `statistik_fitur.csv` - Jumlah fitur yang terdeteksi

#### 04_geometry/output/
- Gambar transformasi dan overlay
- `*_geometry_parameters.txt` - Matriks transformasi
- `tabel_parameter_geometry.csv` - Parameter geometri

### 3. File Laporan
- `SUMMARY_REPORT.txt` - Ringkasan semua output

## Fitur Unik Aplikasi

### 1. Analisis Parameter Komprehensif
- Setiap modul menguji berbagai parameter
- Output tabel CSV untuk analisis kuantitatif
- Perbandingan hasil pada gambar standar vs pribadi

### 2. Pipeline Terintegrasi
- Script utama yang menjalankan semua modul
- Error handling dan progress tracking
- Laporan ringkasan otomatis

### 3. Dokumentasi Lengkap
- Header pada setiap script dengan informasi mahasiswa
- Komentar detail pada setiap fungsi
- README dengan instruksi lengkap

## Troubleshooting

### Error: "Module not found"
```bash
pip install opencv-python numpy pandas scikit-image
```

### Error: "Image file not found"
- Pastikan file `my_photo.jpg` ada di folder root
- Atau hapus/matikan bagian gambar pribadi di script

### Error: "Permission denied"
- Pastikan folder output dapat ditulis
- Jalankan dengan administrator jika diperlukan

### Output tidak lengkap
- Periksa `SUMMARY_REPORT.txt` untuk detail
- Jalankan modul individu untuk debugging

## Analisis dan Refleksi

### Parameter yang Digunakan
1. **Filtering**: Kernel size 3x3, 5x5, 7x7 untuk Gaussian dan Median
2. **Edge Detection**: Threshold 50-250 untuk Canny, kernel 3 dan 5 untuk Sobel
3. **Feature Points**: Threshold 10-30 untuk FAST, berbagai parameter untuk Harris
4. **Geometry**: Sudut rotasi 30°, transformasi perspektif dengan 4 titik kontrol

### Perbandingan Hasil
- **Gambar Standar**: Konsisten untuk perbandingan antar mahasiswa
- **Gambar Pribadi**: Menunjukkan adaptasi algoritma pada konten berbeda
- **Parameter Analysis**: Efek perubahan parameter pada kualitas output

## Kontak dan Support

Jika mengalami masalah atau memiliki pertanyaan:
1. Periksa error message di terminal
2. Baca `SUMMARY_REPORT.txt` untuk detail output
3. Jalankan modul individu untuk debugging
4. Pastikan semua dependencies terinstall