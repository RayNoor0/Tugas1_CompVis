# 02_edge/edge.py

# Nama: Rayendra Althaf Taraka Noor
# NIM: 13522107
# Fitur unik: Script ini menerapkan deteksi tepi Sobel dan Canny pada semua gambar.

import cv2
import numpy as np
from skimage import data
import os
import pandas as pd

def detect_edges(image, image_name, output_dir):
    """
    Mendeteksi tepi menggunakan Sobel dan Canny dengan berbagai parameter,
    menyimpan hasilnya, dan mengembalikan parameter dalam DataFrame.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Pastikan gambar dalam format 8-bit grayscale
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    all_params = []

    # --- 1. Sobel Edge Detection dengan berbagai kernel size ---
    for ksize in [3, 5]:
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_output = cv2.normalize(sobel_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        filename = f"{image_name}_sobel_k{ksize}.png"
        cv2.imwrite(os.path.join(output_dir, filename), sobel_output)
        
        all_params.append({
            'Image Source': image_name,
            'Edge Detection Method': 'Sobel',
            'Parameters': f'ksize = {ksize}',
            'Output Filename': filename
        })

    # --- 2. Canny Edge Detection dengan berbagai threshold ---
    threshold_combinations = [
        (50, 150, "low"),
        (100, 200, "medium"),
        (150, 250, "high")
    ]
    
    for low_thresh, high_thresh, label in threshold_combinations:
        canny_output = cv2.Canny(image, low_thresh, high_thresh)
        filename = f"{image_name}_canny_{label}_{low_thresh}_{high_thresh}.png"
        cv2.imwrite(os.path.join(output_dir, filename), canny_output)
        
        all_params.append({
            'Image Source': image_name,
            'Edge Detection Method': 'Canny',
            'Parameters': f'low_threshold = {low_thresh}, high_threshold = {high_thresh}',
            'Output Filename': filename
        })

    # --- 3. Analisis Sampling dengan Downsampling ---
    # Downsample dengan faktor 2
    downsampled = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2), interpolation=cv2.INTER_AREA)
    canny_downsampled = cv2.Canny(downsampled, 50, 150)
    filename_downsampled = f"{image_name}_canny_downsampled.png"
    cv2.imwrite(os.path.join(output_dir, filename_downsampled), canny_downsampled)
    
    all_params.append({
        'Image Source': image_name,
        'Edge Detection Method': 'Canny Downsampled',
        'Parameters': 'low_threshold = 50, high_threshold = 150, scale = 0.5',
        'Output Filename': filename_downsampled
    })

    df_params = pd.DataFrame(all_params)
    print(f"Deteksi tepi selesai untuk gambar: {image_name}")
    return df_params

def main():
    """
    Fungsi utama untuk menjalankan pipeline deteksi tepi pada semua gambar standar.
    """
    output_dir_edge = "02_edge/output"
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
        params = detect_edges(img_data, img_name, output_dir_edge)
        all_params_list.append(params)
    
    # --- Memproses Gambar Pribadi ---
    personal_image_path = 'my_photo.jpg'
    if os.path.exists(personal_image_path):
        print(f"Memproses gambar pribadi '{personal_image_path}'...")
        img_personal = cv2.imread(personal_image_path, cv2.IMREAD_GRAYSCALE)
        if img_personal is not None:
            params_personal = detect_edges(img_personal, "personal_image", output_dir_edge)
            all_params_list.append(params_personal)
        else:
            print(f"Error: Gagal memuat gambar dari '{personal_image_path}'")
    else:
        print(f"Peringatan: File gambar pribadi '{personal_image_path}' tidak ditemukan. Langkah ini dilewati.")

    if all_params_list:
        final_params_df = pd.concat(all_params_list, ignore_index=True)
        csv_path = os.path.join(output_dir_edge, "tabel_parameter_edge.csv")
        final_params_df.to_csv(csv_path, index=False)
        print(f"\nProses deteksi tepi selesai. Hasil disimpan di: '{output_dir_edge}'")
        print(f"Tabel parameter disimpan di: '{csv_path}'")
        print(f"Total gambar diproses: {len(all_params_list)}")
        print(f"Total metode deteksi: {len(final_params_df)}")
    else:
        print("Tidak ada gambar yang diproses.")

if __name__ == "__main__":
    main()