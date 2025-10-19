# Dashboard Progress Report - Divisi INTEL Fasilkom UNSRI

Dashboard interaktif untuk tracking progress **Program Pengajaran Newscasting** oleh Divisi INTEL Fasilkom UNSRI.

## 🎯 Fitur Utama

### 6 Section Komprehensif:
1. **📊 Overview Dashboard** - Ringkasan keseluruhan dengan KPI dan visualisasi
2. **📚 Progress Pengajaran** - Tracking 12 weekly teaching sessions
3. **👥 Keaktifan Staf** - Monitoring kehadiran dan partisipasi staf newscasting
4. **🎬 Live Practice** - Tracking 4 sesi practice per staf dengan auto-calculation
5. **📝 Evaluasi Divisi** - Evaluasi kualitas program pengajaran
6. **⭐ Penilaian Staf** - Penilaian 6 aspek newscasting per staf

### Teknologi:
- **Interactive tables** dengan st.data_editor
- **Auto-calculation** untuk progress, persentase, dan overall scores
- **Color-coded metrics** dan progress bars
- **Interactive charts** menggunakan Altair
- **Export data** ke JSON/CSV

## 🚀 Cara Menjalankan (Windows PowerShell)

1. **Buat virtual environment** (opsional tapi disarankan):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Jalankan dashboard**:
   ```powershell
   cd "g:\KULIAH\@INTEL\PROGRES REPORT\PROGRESS REPORT 3"
   streamlit run dashboard.py
   ```

4. **Buka browser** - Dashboard akan terbuka otomatis di `http://localhost:8501`

## 📝 Cara Pakai

1. **Pilih section** dari sidebar navigation
2. **Edit data** langsung di tabel (klik cell untuk edit)
3. **Auto-calculation** untuk kolom Total Selesai, Persentase, Overall Score
4. **Lihat visualisasi** - Charts update otomatis
5. **Export data** - Download JSON atau CSV dari sidebar

## ⚙️ Konfigurasi

Edit variabel di file `dashboard.py` (baris 22-57):

- `STAF_NEWSCASTING` - Daftar nama staf (9 orang)
- `WEEKLY_TOPICS` - 12 topik pengajaran mingguan
- `EVALUASI_CATEGORIES` - 5 kategori evaluasi divisi

## 📦 Data Persistence

- Data tersimpan di **Streamlit session state** (hilang saat refresh)
- Untuk backup: gunakan tombol **Export JSON/CSV** di sidebar
- Untuk restore: copy-paste data dari export ke tabel

## 🎨 Customization

Ubah tema/warna di file `dashboard.py`:
- Line 1018-1030: Custom CSS styling
- Chart colors di setiap render function

## 📌 Catatan

- Streamlit >= 1.26 diperlukan untuk `st.data_editor`
- Data initial sudah ter-set untuk semua staf
- Overall scores dihitung otomatis (read-only)
- Practice percentages auto-update saat edit

## 🆘 Troubleshooting

**Dashboard tidak muncul?**
- Pastikan Streamlit terinstall: `pip show streamlit`
- Check port 8501 tidak dipakai aplikasi lain

**Error saat edit tabel?**
- Update Streamlit: `pip install --upgrade streamlit`

**Data hilang saat refresh?**
- Export JSON dulu sebelum refresh
- Atau tambahkan fitur auto-save (contact developer)

---

**Dashboard v2.0** - Divisi INTEL Fasilkom UNSRI  
Program Pengajaran Newscasting 2025
