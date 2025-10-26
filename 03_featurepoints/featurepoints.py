# 03_featurepoints/featurepoints.py

# Nama: Rayendra Althaf Taraka Noor
# NIM: 13522107
# Fitur unik: Script ini mendeteksi feature points menggunakan Harris, SIFT, dan FAST pada semua gambar.
import cv2
import numpy as np
from skimage import data
import os
import pandas as pd

def find_and_draw_features(image, image_name, output_dir):
    """
    Mendeteksi, menggambar, dan menghitung feature points (Harris, SIFT, FAST).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Pastikan gambar adalah 8-bit grayscale
    if len(image.shape) > 2:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image.copy()

    # Buat versi berwarna dari gambar grayscale untuk menggambar fitur
    image_to_draw_on = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    all_stats = []

    # --- 1. Harris Corner Detection dengan berbagai parameter ---
    gray_float = np.float32(gray_image)
    
    # Parameter Harris yang berbeda
    harris_params = [
        (2, 3, 0.04, "default"),
        (3, 3, 0.04, "larger_block"),
        (2, 5, 0.04, "larger_kernel"),
        (2, 3, 0.06, "higher_k")
    ]
    
    for blockSize, ksize, k, label in harris_params:
        harris_response = cv2.cornerHarris(gray_float, blockSize, ksize, k)
        threshold = 0.01 * harris_response.max()
        
        harris_image = image_to_draw_on.copy()
        harris_image[harris_response > threshold] = [0, 0, 255]  # Merah
        
        num_corners = np.sum(harris_response > threshold)
        filename = f"{image_name}_harris_{label}.png"
        cv2.imwrite(os.path.join(output_dir, filename), harris_image)
        
        all_stats.append({
            'Image Source': image_name,
            'Feature Detector': f'Harris {label}',
            'Detected Points Count': num_corners,
            'Parameters': f'blockSize={blockSize}, ksize={ksize}, k={k}',
            'Output Filename': filename
        })

    # --- 2. SIFT Feature Detection ---
    sift = cv2.SIFT_create()
    keypoints_sift, descriptors = sift.detectAndCompute(gray_image, None)
    
    sift_image = image_to_draw_on.copy()
    cv2.drawKeypoints(sift_image, keypoints_sift, sift_image, 
                     flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    filename = f"{image_name}_sift_features.png"
    cv2.imwrite(os.path.join(output_dir, filename), sift_image)
    
    all_stats.append({
        'Image Source': image_name,
        'Feature Detector': 'SIFT',
        'Detected Points Count': len(keypoints_sift),
        'Parameters': 'default SIFT parameters',
        'Output Filename': filename
    })

    # --- 3. FAST Feature Detection dengan berbagai threshold ---
    fast_thresholds = [10, 20, 30]
    
    for threshold in fast_thresholds:
        fast = cv2.FastFeatureDetector_create(threshold=threshold)
        keypoints_fast = fast.detect(gray_image, None)
        
        fast_image = image_to_draw_on.copy()
        cv2.drawKeypoints(fast_image, keypoints_fast, fast_image, 
                         flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        filename = f"{image_name}_fast_thresh_{threshold}.png"
        cv2.imwrite(os.path.join(output_dir, filename), fast_image)
        
        all_stats.append({
            'Image Source': image_name,
            'Feature Detector': f'FAST thresh_{threshold}',
            'Detected Points Count': len(keypoints_fast),
            'Parameters': f'threshold = {threshold}',
            'Output Filename': filename
        })

    df_stats = pd.DataFrame(all_stats)
    print(f"Deteksi fitur selesai untuk gambar: {image_name}")
    return df_stats

def main():
    """
    Fungsi utama untuk menjalankan pipeline deteksi fitur pada semua gambar standar.
    """
    output_dir_features = "03_featurepoints/output"
    all_stats_list = []

    # --- Memproses Semua Gambar Standar ---
    standard_images = [
        ("cameraman", data.camera()),
        ("coins", data.coins()),
        ("checkerboard", data.checkerboard()),
        ("astronaut", cv2.cvtColor(data.astronaut(), cv2.COLOR_RGB2GRAY))
    ]

    for img_name, img_data in standard_images:
        print(f"Memproses gambar standar '{img_name}'...")
        stats = find_and_draw_features(img_data, img_name, output_dir_features)
        all_stats_list.append(stats)
    
    # --- Memproses Gambar Pribadi ---
    personal_image_path = 'my_photo.jpg'
    if os.path.exists(personal_image_path):
        print(f"Memproses gambar pribadi '{personal_image_path}'...")
        img_personal = cv2.imread(personal_image_path, cv2.IMREAD_GRAYSCALE)
        if img_personal is not None:
            stats_personal = find_and_draw_features(img_personal, "personal_image", output_dir_features)
            all_stats_list.append(stats_personal)
        else:
            print(f"Error: Gagal memuat gambar dari '{personal_image_path}'")
    else:
        print(f"Peringatan: File gambar pribadi '{personal_image_path}' tidak ditemukan. Langkah ini dilewati.")

    if all_stats_list:
        final_stats_df = pd.concat(all_stats_list, ignore_index=True)
        csv_path = os.path.join(output_dir_features, "statistik_fitur.csv")
        final_stats_df.to_csv(csv_path, index=False)
        print(f"\nProses deteksi fitur selesai. Hasil disimpan di: '{output_dir_features}'")
        print(f"Statistik fitur disimpan di: '{csv_path}'")
        print(f"Total gambar diproses: {len(all_stats_list)}")
        print(f"Total detektor digunakan: {len(final_stats_df)}")
        
        # Tampilkan ringkasan statistik
        print("\n--- RINGKASAN STATISTIK ---")
        summary = final_stats_df.groupby('Feature Detector')['Detected Points Count'].agg(['mean', 'std', 'min', 'max'])
        print(summary)
    else:
        print("Tidak ada gambar yang diproses.")

if __name__ == "__main__":
    main()