# 04_geometry/geometry.py

# Nama: Rayendra Althaf Taraka Noor
# NIM: 13522107
# Fitur: Script ini melakukan simulasi kalibrasi kamera dan transformasi geometri pada semua gambar.

import cv2
import numpy as np
from skimage import data
import os
import pandas as pd

def simulate_camera_calibration(image, image_name, output_dir):
    """
    Melakukan simulasi kalibrasi kamera dan transformasi geometri.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Pastikan gambar dalam format BGR untuk menggambar
    if len(image.shape) == 2:
        image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        image_bgr = image.copy()
        
    rows, cols, _ = image_bgr.shape

    all_params = []

    # --- 1. Simulasi Transformasi Perspektif ---
    # Tentukan 4 titik pada gambar sumber (sudut gambar)
    src_points = np.float32([
        [0, 0],         # Kiri atas
        [cols - 1, 0],  # Kanan atas
        [0, rows - 1],  # Kiri bawah
        [cols - 1, rows - 1] # Kanan bawah
    ])

    # Tentukan 4 titik tujuan untuk efek perspektif
    dst_points = np.float32([
        [cols * 0.15, rows * 0.15], # Kiri atas bergeser ke dalam
        [cols * 0.85, rows * 0.1],  # Kanan atas bergeser
        [cols * 0.05, rows * 0.9],  # Kiri bawah bergeser
        [cols * 0.95, rows * 0.85]  # Kanan bawah bergeser
    ])

    # Hitung matriks transformasi perspektif
    M_perspective = cv2.getPerspectiveTransform(src_points, dst_points)

    # Terapkan transformasi
    transformed_img = cv2.warpPerspective(image_bgr, M_perspective, (cols, rows))
    
    # Simpan hasil
    cv2.imwrite(os.path.join(output_dir, f"{image_name}_perspective_transformed.png"), transformed_img)

    all_params.append({
        'Image Source': image_name,
        'Transform Type': 'Perspective Transform',
        'Matrix Shape': f'{M_perspective.shape}',
        'Output Files': f'{image_name}_perspective_transformed.png'
    })

    # --- 2. Simulasi Rotasi dan Scaling ---
    # Matriks rotasi 30 derajat
    angle = 30
    center = (cols // 2, rows // 2)
    M_rotation = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Terapkan rotasi
    rotated_img = cv2.warpAffine(image_bgr, M_rotation, (cols, rows))
    cv2.imwrite(os.path.join(output_dir, f"{image_name}_rotated_{angle}deg.png"), rotated_img)

    all_params.append({
        'Image Source': image_name,
        'Transform Type': f'Rotation {angle}°',
        'Matrix Shape': f'{M_rotation.shape}',
        'Output Files': f'{image_name}_rotated_{angle}deg.png'
    })

    # --- 3. Simulasi Camera Calibration dengan Checkerboard ---
    if "checkerboard" in image_name.lower():
        # Deteksi corner checkerboard untuk simulasi kalibrasi
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # Parameter checkerboard (sesuaikan dengan gambar)
        pattern_size = (7, 7)  # Internal corners
        
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            # Refine corner detection
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            # Gambar corner yang terdeteksi
            corner_img = image_bgr.copy()
            cv2.drawChessboardCorners(corner_img, pattern_size, corners_refined, ret)
            cv2.imwrite(os.path.join(output_dir, f"{image_name}_calibration_corners.png"), corner_img)
            
            # Simulasi parameter kamera intrinsik
            camera_matrix = np.array([
                [800, 0, cols/2],
                [0, 800, rows/2],
                [0, 0, 1]
            ], dtype=np.float32)
            
            dist_coeffs = np.zeros((4, 1), dtype=np.float32)
            
            # Simulasi kalibrasi (dalam praktik nyata, ini akan menggunakan objek points 3D)
            obj_points = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
            obj_points[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
            
            # Simulasi pose estimation
            ret, rvecs, tvecs = cv2.solvePnP(obj_points, corners_refined, camera_matrix, dist_coeffs)
            
            all_params.append({
                'Image Source': image_name,
                'Transform Type': 'Camera Calibration',
                'Matrix Shape': f'Camera Matrix: {camera_matrix.shape}',
                'Output Files': f'{image_name}_calibration_corners.png'
            })

    # --- Simpan Parameter dan Matriks ke File Teks ---
    matrix_file_path = os.path.join(output_dir, f"{image_name}_geometry_parameters.txt")
    with open(matrix_file_path, 'w') as f:
        f.write("--- Parameter Transformasi Geometri ---\n\n")
        f.write(f"Gambar Sumber: {image_name}\n")
        f.write(f"Dimensi Gambar: {cols} x {rows}\n\n")
        
        f.write("1. Transformasi Perspektif:\n")
        f.write(f"Titik Sumber:\n{src_points}\n\n")
        f.write(f"Titik Tujuan:\n{dst_points}\n\n")
        f.write(f"Matriks Transformasi Perspektif:\n{M_perspective}\n\n")
        
        f.write("2. Transformasi Rotasi:\n")
        f.write(f"Sudut Rotasi: {angle} derajat\n")
        f.write(f"Pusat Rotasi: {center}\n")
        f.write(f"Matriks Rotasi:\n{M_rotation}\n\n")
        
        if "checkerboard" in image_name.lower() and ret:
            f.write("3. Parameter Kalibrasi Kamera:\n")
            f.write(f"Camera Matrix:\n{camera_matrix}\n\n")
            f.write(f"Distortion Coefficients:\n{dist_coeffs}\n\n")
            f.write(f"Rotation Vector:\n{rvecs}\n\n")
            f.write(f"Translation Vector:\n{tvecs}\n\n")

    df_params = pd.DataFrame(all_params)
    print(f"Transformasi geometri selesai untuk gambar: {image_name}")
    print(f"Parameter dan matriks disimpan di: '{matrix_file_path}'")
    return df_params

def main():
    """
    Fungsi utama untuk menjalankan pipeline transformasi geometri pada semua gambar standar.
    """
    output_dir_geometry = "04_geometry/output"
    all_params_list = []

    # --- Memproses Semua Gambar Standar ---
    standard_images = [
        ("cameraman", data.camera()),
        ("coins", data.coins()),
        ("checkerboard", data.checkerboard()),
        ("astronaut", cv2.cvtColor(data.astronaut(), cv2.COLOR_RGB2GRAY))
    ]

    for img_name, img_data in standard_images:
        print(f"Memproses gambar standar '{img_name}'...")
        params = simulate_camera_calibration(img_data, img_name, output_dir_geometry)
        all_params_list.append(params)
    
    # --- Memproses Gambar Pribadi ---
    personal_image_path = 'my_photo.jpg'
    if os.path.exists(personal_image_path):
        print(f"Memproses gambar pribadi '{personal_image_path}'...")
        img_personal = cv2.imread(personal_image_path, cv2.IMREAD_GRAYSCALE)
        if img_personal is not None:
            params_personal = simulate_camera_calibration(img_personal, "personal_image", output_dir_geometry)
            all_params_list.append(params_personal)
        else:
            print(f"Error: Gagal memuat gambar dari '{personal_image_path}'")
    else:
        print(f"Peringatan: File gambar pribadi '{personal_image_path}' tidak ditemukan. Langkah ini dilewati.")

    if all_params_list:
        final_params_df = pd.concat(all_params_list, ignore_index=True)
        csv_path = os.path.join(output_dir_geometry, "tabel_parameter_geometry.csv")
        final_params_df.to_csv(csv_path, index=False)
        print(f"\nProses transformasi geometri selesai. Hasil disimpan di: '{output_dir_geometry}'")
        print(f"Tabel parameter disimpan di: '{csv_path}'")
        print(f"Total gambar diproses: {len(all_params_list)}")
        print(f"Total transformasi diterapkan: {len(final_params_df)}")
    else:
        print("Tidak ada gambar yang diproses.")

if __name__ == "__main__":
    main()