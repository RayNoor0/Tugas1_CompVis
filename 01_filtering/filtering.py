# 01_filtering/filtering.py

# Nama: Rayendra Althaf Taraka Noor
# NIM: 13522107
# Fitur unik: Script ini menerapkan multiple filter (Gaussian, Median, Sobel) pada semua gambar.

import cv2
import numpy as np
from skimage import data
import os
import pandas as pd

def process_and_filter_image(image, image_name, output_dir):
    """
    Menerapkan beberapa filter ke gambar, menyimpan hasilnya, 
    dan mengembalikan parameter yang digunakan dalam bentuk DataFrame.
    """
    # Pastikan direktori output ada, jika tidak, buat direktori tersebut
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Simpan gambar asli untuk perbandingan
    cv2.imwrite(os.path.join(output_dir, f"{image_name}_original.png"), image)
    
    # --- 1. Gaussian Filter dengan berbagai kernel size ---
    gaussian_params = []
    for kernel_size in [(3, 3), (5, 5), (7, 7)]:
        gaussian_filtered = cv2.GaussianBlur(image, kernel_size, 0)
        filename = f"{image_name}_gaussian_{kernel_size[0]}x{kernel_size[1]}.png"
        cv2.imwrite(os.path.join(output_dir, filename), gaussian_filtered)
        gaussian_params.append({
            'Image Source': image_name,
            'Filter Type': 'Gaussian Blur',
            'Parameters': f'Kernel Size = {kernel_size}, Sigma = 0 (auto)',
            'Output Filename': filename
        })

    # --- 2. Median Filter dengan berbagai kernel size ---
    median_params = []
    for kernel_size in [3, 5, 7]:
        median_filtered = cv2.medianBlur(image, kernel_size)
        filename = f"{image_name}_median_{kernel_size}x{kernel_size}.png"
        cv2.imwrite(os.path.join(output_dir, filename), median_filtered)
        median_params.append({
            'Image Source': image_name,
            'Filter Type': 'Median Blur',
            'Parameters': f'Kernel Size = {kernel_size}x{kernel_size}',
            'Output Filename': filename
        })

    # --- 3. Sobel Filter (untuk edge detection) ---
    sobel_params = []
    # Sobel X
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x_abs = np.absolute(sobel_x)
    sobel_x_normalized = np.uint8(255 * sobel_x_abs / np.max(sobel_x_abs))
    filename_x = f"{image_name}_sobel_x.png"
    cv2.imwrite(os.path.join(output_dir, filename_x), sobel_x_normalized)
    sobel_params.append({
        'Image Source': image_name,
        'Filter Type': 'Sobel X',
        'Parameters': 'ksize = 3, dx = 1, dy = 0',
        'Output Filename': filename_x
    })

    # Sobel Y
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y_abs = np.absolute(sobel_y)
    sobel_y_normalized = np.uint8(255 * sobel_y_abs / np.max(sobel_y_abs))
    filename_y = f"{image_name}_sobel_y.png"
    cv2.imwrite(os.path.join(output_dir, filename_y), sobel_y_normalized)
    sobel_params.append({
        'Image Source': image_name,
        'Filter Type': 'Sobel Y',
        'Parameters': 'ksize = 3, dx = 0, dy = 1',
        'Output Filename': filename_y
    })

    # Sobel Magnitude
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_mag_normalized = np.uint8(255 * sobel_magnitude / np.max(sobel_magnitude))
    filename_mag = f"{image_name}_sobel_magnitude.png"
    cv2.imwrite(os.path.join(output_dir, filename_mag), sobel_mag_normalized)
    sobel_params.append({
        'Image Source': image_name,
        'Filter Type': 'Sobel Magnitude',
        'Parameters': 'Magnitude of X and Y gradients',
        'Output Filename': filename_mag
    })

    # Gabungkan semua parameter
    all_params = gaussian_params + median_params + sobel_params
    df_params = pd.DataFrame(all_params)
    
    print(f"Filtering selesai untuk gambar: {image_name}")
    return df_params

def main():
    """
    Fungsi utama untuk menjalankan pipeline filtering pada semua gambar standar.
    """
    output_dir_filtering = "01_filtering/output"
    all_params_list = []

    # --- Memproses Semua Gambar Standar ---
    standard_images = [
        ("cameraman", data.camera()),
        ("coins", data.coins()),
        ("checkerboard", (data.checkerboard() * 255).astype(np.uint8)),
        ("astronaut", cv2.cvtColor(data.astronaut(), cv2.COLOR_RGB2GRAY))
    ]

    for img_name, img_data in standard_images:
        print(f"Memproses gambar standar '{img_name}'...")
        params = process_and_filter_image(img_data, img_name, output_dir_filtering)
        all_params_list.append(params)
    
    # --- Memproses Gambar Pribadi ---
    personal_image_path = 'my_photo.jpg' 
    if os.path.exists(personal_image_path):
        print(f"Memproses gambar pribadi '{personal_image_path}'...")
        img_personal = cv2.imread(personal_image_path, cv2.IMREAD_GRAYSCALE)
        
        if img_personal is not None:
            params_personal = process_and_filter_image(img_personal, "personal_image", output_dir_filtering)
            all_params_list.append(params_personal)
        else:
            print(f"Error: Gagal memuat gambar dari '{personal_image_path}'")
    else:
        print(f"Peringatan: File gambar pribadi '{personal_image_path}' tidak ditemukan. Langkah ini dilewati.")

    # Gabungkan semua DataFrame parameter dan simpan ke file CSV
    if all_params_list:
        final_params_df = pd.concat(all_params_list, ignore_index=True)
        csv_path = os.path.join(output_dir_filtering, "tabel_parameter_filtering.csv")
        final_params_df.to_csv(csv_path, index=False)
        print(f"\nProses filtering selesai. Semua hasil disimpan di direktori: '{output_dir_filtering}'")
        print(f"Tabel parameter disimpan di: '{csv_path}'")
        print(f"Total gambar diproses: {len(all_params_list)}")
        print(f"Total filter diterapkan: {len(final_params_df)}")
    else:
        print("Tidak ada gambar yang diproses.")

if __name__ == "__main__":
    main()
