# main_integration.py

# Nama: Rayendra Althaf Taraka Noor
# NIM: 13522107
# Fitur unik: Script utama yang mengintegrasikan semua modul Computer Vision (filtering, edge detection, feature points, dan geometry).

import os
import sys
import time
import importlib
from datetime import datetime

def run_module(module_name, script_path):
    """
    Menjalankan modul tertentu dan menangani error.
    """
    print(f"\n{'='*60}")
    print(f"Menjalankan modul: {module_name}")
    print(f"{'='*60}")
    
    try:
        # Import dan jalankan modul
        if module_name == "filtering":
            module = importlib.import_module("01_filtering.filtering")
            module.main()
        elif module_name == "edge":
            module = importlib.import_module("02_edge.edge")
            module.main()
        elif module_name == "featurepoints":
            module = importlib.import_module("03_featurepoints.featurepoints")
            module.main()
        elif module_name == "geometry":
            module = importlib.import_module("04_geometry.geometry")
            module.main()
        
        print(f"✓ Modul {module_name} berhasil dijalankan")
        return True
        
    except Exception as e:
        print(f"✗ Error dalam modul {module_name}: {str(e)}")
        return False

def create_summary_report():
    """
    Membuat laporan ringkasan dari semua output yang dihasilkan.
    """
    print(f"\n{'='*60}")
    print("MEMBUAT LAPORAN RINGKASAN")
    print(f"{'='*60}")
    
    summary_file = "SUMMARY_REPORT.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("LAPORAN RINGKASAN APLIKASI COMPUTER VISION\n")
        f.write("="*50 + "\n\n")
        f.write(f"Tanggal Eksekusi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Cek output dari setiap modul
        modules = [
            ("01_filtering", "Filtering"),
            ("02_edge", "Edge Detection"),
            ("03_featurepoints", "Feature Points"),
            ("04_geometry", "Geometry")
        ]
        
        for folder, name in modules:
            output_dir = f"{folder}/output"
            f.write(f"{name}:\n")
            f.write("-" * 20 + "\n")
            
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                f.write(f"  Output directory: {output_dir}\n")
                f.write(f"  Jumlah file: {len(files)}\n")
                f.write(f"  File yang dihasilkan:\n")
                for file in sorted(files):
                    f.write(f"    - {file}\n")
            else:
                f.write(f"  Output directory tidak ditemukan: {output_dir}\n")
            f.write("\n")
        
        f.write("CATATAN:\n")
        f.write("- Pastikan semua gambar standar diproses dengan benar\n")
        f.write("- Periksa file CSV untuk parameter dan statistik\n")
        f.write("- Gunakan output ini untuk membuat laporan PDF\n")
    
    print(f"✓ Laporan ringkasan disimpan di: {summary_file}")

def main():
    """
    Fungsi utama untuk menjalankan seluruh pipeline Computer Vision.
    """
    print(f"Dimulai pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Daftar modul yang akan dijalankan
    modules = [
        ("filtering", "01_filtering/filtering.py"),
        ("edge", "02_edge/edge.py"),
        ("featurepoints", "03_featurepoints/featurepoints.py"),
        ("geometry", "04_geometry/geometry.py")
    ]
    
    successful_modules = []
    failed_modules = []
    
    # Jalankan setiap modul
    for module_name, script_path in modules:
        if os.path.exists(script_path):
            success = run_module(module_name, script_path)
            if success:
                successful_modules.append(module_name)
            else:
                failed_modules.append(module_name)
        else:
            print(f"✗ Script tidak ditemukan: {script_path}")
            failed_modules.append(module_name)
        
        # Jeda singkat antar modul
        time.sleep(1)
    
    # Buat laporan ringkasan
    create_summary_report()
    
    # Tampilkan hasil akhir
    print(f"\n{'='*60}")
    print("HASIL AKHIR")
    print(f"{'='*60}")
    print(f"Modul berhasil: {len(successful_modules)}")
    for module in successful_modules:
        print(f"{module}")
    
    print(f"Modul gagal: {len(failed_modules)}")
    for module in failed_modules:
        print(f"{module}")
    
    if len(failed_modules) == 0:
        print("\nSemua modul berhasil dijalankan!")
        print("Periksa folder output untuk melihat hasil")
        print("Gunakan SUMMARY_REPORT.txt untuk referensi")
    else:
        print(f"\nAda {len(failed_modules)} modul yang gagal")
        print("Periksa error message di atas untuk troubleshooting")
    
    print(f"\nSelesai pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
