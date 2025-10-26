# test_application.py

# Script untuk testing aplikasi Computer Vision
# Menjalankan semua modul dan memverifikasi output

import os
import sys
import numpy as np
from skimage import data
import cv2

def verify_outputs():
    """
    Memverifikasi bahwa semua output yang diperlukan telah dibuat.
    """
    print("\n" + "="*60)
    print("VERIFIKASI OUTPUT")
    print("="*60)
    
    required_folders = [
        "01_filtering/output",
        "02_edge/output", 
        "03_featurepoints/output",
        "04_geometry/output"
    ]
    
    all_good = True
    
    for folder in required_folders:
        if os.path.exists(folder):
            files = os.listdir(folder)
            print(f"{folder}: {len(files)} file(s)")
            if len(files) == 0:
                print(f"Folder kosong")
                all_good = False
        else:
            print(f"{folder}: Tidak ditemukan")
            all_good = False
    
    # Cek file laporan
    if os.path.exists("SUMMARY_REPORT.txt"):
        print("SUMMARY_REPORT.txt: Ditemukan")
    else:
        print("SUMMARY_REPORT.txt: Tidak ditemukan")
        all_good = False
    
    return all_good

def main():
    """
    Fungsi utama untuk testing aplikasi.
    """
    print("TESTING APLIKASI COMPUTER VISION")
    print("="*40)
    
    # Jalankan aplikasi utama
    print("\nMenjalankan aplikasi utama...")
    try:
        from main_integration import main as run_app
        run_app()
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")
        return False
    
    # Verifikasi output
    success = verify_outputs()
    
    if success:
        print("\nSEMUA TEST BERHASIL!")
    else:
        print("\nAda masalah dengan output")
        print("Periksa error di atas")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
