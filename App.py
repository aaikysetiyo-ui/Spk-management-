import os
import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Manajemen Arsip SPK Profesional",
    page_icon="ðŸ“",
    layout="wide"
)

# Direktori Utama Penyimpanan
BASE_DIR = "DATABASE_SPK_UTAMA"

# Fungsi untuk membuat struktur folder otomatis 2026 - 2027
def create_folder_structure():
    tahun_list = ["2026", "2027"]
    bulan_list = [
        "01_Januari", "02_Februari", "03_Maret", "04_April", 
        "05_Mei", "06_Juni", "07_Juli", "08_Agustus", 
        "09_September", "10_Oktober", "11_November", "12_Desember"
    ]
    status_list = ["Masuk", "Proses", "Selesai"]
    
    for tahun in tahun_list:
        for bulan in bulan_list:
            for status in status_list:
                folder_path = os.path.join(BASE_DIR, tahun, f"{bulan}_{tahun}", status)
                os.makedirs(folder_path, exist_ok=True)

# Jalankan pembuatan folder saat aplikasi dimuat
create_folder_structure()

# Sidebar Navigasi
st.sidebar.title("ðŸ“‚ Navigasi SPK")
menu = st.sidebar.radio("Pilih Menu:", ["Dashboard", "Unggah SPK (Upload)", "Cari & Kelola Arsip"])

# --- MENU 1: DASHBOARD ---
if menu == "Dashboard":
    st.title("ðŸ“Š Dashboard Arsip SPK (2026 - 2027)")
    st.markdown("Selamat datang di sistem manajemen Surat Perintah Kerja (SPK) yang terstruktur rapi.")
    
    # Statistik Singkat
    col1, col2, col3 = st.columns(3)
    
    # Hitung total file
    total_files = 0
    if os.path.exists(BASE_DIR):
        for root, dirs, files in os.walk(BASE_DIR):
            total_files += len(files)
            
    col1.metric("Total File SPK Tersimpan", f"{total_files} File")
    col2.metric("Tahun Aktif", "2026 & 2027")
    col3.metric("Status Sistem", "Aktif & Aman âœ…")
    
    st.info("ðŸ’¡ Gunakan menu **Unggah SPK** di samping untuk memasukkan data baru ke folder yang sesuai secara otomatis.")

# --- MENU 2: UNGGAH SPK ---
elif menu == "Unggah SPK (Upload)":
    st.title("ðŸ“¤ Unggah Dokumen SPK")
    st.write("Unggah dokumen SPK Anda dan sistem akan menyimpannya secara otomatis ke dalam folder yang dipilih.")
    
    with st.form("upload_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tahun = st.selectbox("Pilih Tahun", ["2026", "2027"])
        with col2:
            bulan = st.selectbox("Pilih Bulan", [
                "01_Januari", "02_Februari", "03_Maret", "04_April", 
                "05_Mei", "06_Juni", "07_Juli", "08_Agustus", 
                "09_September", "10_Oktober", "11_November", "12_Desember"
            ])
        with col3:
            status = st.selectbox("Status SPK", ["Masuk", "Proses", "Selesai"])
            
        uploaded_files = st.file_uploader(
            "Pilih file SPK (Bisa pilih banyak file sekaligus)", 
            accept_multiple_files=True,
            type=["pdf", "docx", "xlsx", "jpg", "png", "zip"]
        )
        
        submitted = st.form_submit_button("Simpan ke Folder")
        
        if submitted:
            if uploaded_files:
                target_folder = os.path.join(BASE_DIR, tahun, f"{bulan}_{tahun}", status)
                os.makedirs(target_folder, exist_ok=True)
                
                count = 0
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(target_folder, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    count += 1
                    
                st.success(f"Berhasil! {count} file telah disimpan rapi ke direktori: `{target_folder}`")
            else:
                st.warning("Silakan pilih minimal satu file untuk diunggah.")

# --- MENU 3: CARI & KELOLA ARSIP ---
elif menu == "Cari & Kelola Arsip":
    st.title("ðŸ” Pencarian & Daftar Arsip SPK")
    st.write("Telusuri file berdasarkan tahun dan bulan penyimpanan.")
    
    selected_tahun = st.selectbox("Filter Tahun", ["2026", "2027"])
    selected_bulan = st.selectbox("Filter Bulan", [
        "01_Januari", "02_Februari", "03_Maret", "04_April", 
        "05_Mei", "06_Juni", "07_Juli", "08_Agustus", 
        "09_September", "10_Oktober", "11_November", "12_Desember"
    ])
    
    target_dir = os.path.join(BASE_DIR, selected_tahun, f"{selected_bulan}_{selected_tahun}")
    
    if os.path.exists(target_dir):
        file_data = []
        for status_folder in ["Masuk", "Proses", "Selesai"]:
            status_path = os.path.join(target_dir, status_folder)
            if os.path.exists(status_path):
                for f in os.listdir(status_path):
                    file_path = os.path.join(status_path, f)
                    if os.path.isfile(file_path):
                        file_size = round(os.path.getsize(file_path) / 1024, 2) # dalam KB
                        file_data.append({
                            "Nama File": f,
                            "Status": status_folder,
                            "Ukuran (KB)": file_size,
                            "Path": file_path
                        })
        
        if file_data:
            df = pd.DataFrame(file_data)
            st.dataframe(df[["Nama File", "Status", "Ukuran (KB)"]], use_container_width=True)
            st.success(dapatkan_info := f"Ditemukan {len(file_data)} dokumen pada periode ini.")
        else:
            st.info("Belum ada file yang diunggah di periode ini.")
    else:
        st.warning("Folder periode ini belum tersedia.")
