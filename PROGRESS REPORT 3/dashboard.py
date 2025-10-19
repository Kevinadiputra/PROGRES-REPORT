import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, datetime
import json

# ============================================================================
# Dashboard Progress Report - Divisi INTEL Fasilkom UNSRI
# Program Pengajaran Newscasting untuk Staf Newscasting
# ============================================================================
# Sections:
# 1. 📊 Overview Dashboard - Ringkasan keseluruhan
# 2. 📚 Progress Pengajaran (12 Weekly Sessions)
# 3. 👥 Keaktifan Staf Newscasting
# 4. 🎬 Live Practice Tracking
# 5. 📝 Evaluasi Divisi
# 6. ⭐ Penilaian Staf
# ============================================================================

# ============================================================================
# CONFIGURATION - Edit data di sini untuk customize
# ============================================================================

STAF_NEWSCASTING = [
    "rafi",
    "ashila",
    "nabila",
    "zazkia",
    "zaskia",
    "arsyil",
    "vania",
    "dara utami",
    "palina",
]

WEEKLY_TOPICS = [
    "Week 1: Introduction to Newscasting",
    "Week 2: Voice Modulation & Diction",
    "Week 3: News Script Writing Basics",
    "Week 4: Teleprompter & On-Camera Presence",
    "Week 5: Live Reporting Techniques",
    "Week 6: Interviewing Skills",
    "Week 7: Crisis Reporting & Ethics",
    "Week 8: Editing & News Production",
    "Week 9: Podcast & Radio Broadcasting",
    "Week 10: Debate & Panel Discussion",
    "Week 11: Digital Journalism & The Modern Media Landscape",
    "Week 12: Media Law & Journalistic Accountability",
]

# Real attendance data from files (Week: [absent_list, izin_list])
ATTENDANCE_DATA = {
    "Week 1": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 2": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 3": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 4": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 5": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 6": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "zaskia", "arsyil", "vania", "dara utami", "palina"],
        "tidak_hadir": [],
    },
    "Week 7": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "arsyil"],
        "tidak_hadir": ["palina", "dara utami", "vania"],
    },
    "Week 8": {
        "tanggal": "",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "arsyil"],
        "tidak_hadir": ["palina", "vania"],
    },
    "Week 9": {
        "tanggal": "2025-07-12",
        "hadir": ["rafi", "nabila", "zazkia", "arsyil", "ashila", "dara utami", "palina"],
        "tidak_hadir": ["vania"],
    },
    "Week 10": {
        "tanggal": "2025-08-03",
        "hadir": ["rafi", "ashila", "nabila", "zazkia", "arsyil"],
        "tidak_hadir": ["palina", "vania", "dara utami"],
    },
    "Week 11": {
        "tanggal": "2025-08-09",
        "hadir": ["rafi", "ashila", "nabila", "arsyil", "dara utami", "palina", "zaskia"],
        "tidak_hadir": ["vania"],
    },
    "Week 12": {
        "tanggal": "2025-08-09",
        "hadir": ["rafi", "ashila", "nabila", "arsyil", "dara utami", "palina", "zaskia"],
        "tidak_hadir": ['vania'],
    },
}

# Practice data (staf: [weeks practiced])
PRACTICE_DATA = {
    "rafi": ["Week 5", "Week 7", "Week 10"],
    "ashila": ["Week 9", "Week 11"],
    "nabila": ["Week 6", 'Week 9'],
    "zazkia": ["Week 7", "Week 11"],
    "zaskia": ['Week 8', "Week 11"],
    "arsyil": ["Week 5", "Week 10", "Week 12"],
    "vania": [],
    "dara utami": ['Week 9'],
    "palina": [],
}

EVALUASI_CATEGORIES = [
    "Engagement Staf",
    "Fasilitas & Resources",
    "Pencapaian Target",
    "Kolaborasi Tim",
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_status_color(status):
    """Return color based on status."""
    colors = {
        "Belum Mulai": "🔴",
        "Sedang Berjalan": "🟡",
        "Selesai": "🟢",
        "Tertunda": "🟠",
    }
    return colors.get(status, "⚪")


def calculate_completion_rate(df, status_col="Status"):
    """Calculate completion rate from dataframe."""
    if len(df) == 0:
        return 0
    completed = (df[status_col] == "Selesai").sum()
    return (completed / len(df)) * 100


def render_progress_bar(value, max_value=100, label=""):
    """Render a custom progress bar."""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    color = "🟢" if percentage >= 80 else "🟡" if percentage >= 50 else "🔴"
    st.markdown(f"{label} {color}")
    st.progress(percentage / 100)
    st.caption(f"{value}/{max_value} ({percentage:.1f}%)")


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables with real data from files."""
    
    # Progress Pengajaran (12 Weekly Sessions) with real attendance data
    if "progress_pengajaran" not in st.session_state:
        data = []
        for i, topic in enumerate(WEEKLY_TOPICS, 1):
            week_key = f"Week {i}"
            attendance_info = ATTENDANCE_DATA.get(week_key, {})
            
            # Calculate attendance percentage
            if attendance_info:
                total_staf = len(STAF_NEWSCASTING)
                hadir = len(attendance_info.get("hadir", []))
                kehadiran_pct = (hadir / total_staf * 100) if total_staf > 0 else 0
                status = "Selesai" if attendance_info else "Belum Mulai"
                tanggal = attendance_info.get("tanggal", "")
                materi_delivered = 100 if attendance_info else 0
            else:
                kehadiran_pct = 0
                status = "Belum Mulai"
                tanggal = ""
                materi_delivered = 0
            
            data.append({
                "Week": topic,
                "Tanggal": tanggal,
                "Instruktur": "Ara and Kevin" if attendance_info else "",
                "Status": status,
                "Kehadiran (%)": round(kehadiran_pct, 1),
                "Materi Delivered (%)": materi_delivered,
                "Catatan": "",
            })
        
        st.session_state.progress_pengajaran = pd.DataFrame(data)
    
    # Keaktifan Staf - calculate real attendance from data
    if "keaktifan_staf" not in st.session_state:
        data = []
        total_weeks = len(ATTENDANCE_DATA)
        
        for staf in STAF_NEWSCASTING:
            # Count attendance
            hadir_count = 0
            for week_data in ATTENDANCE_DATA.values():
                if staf in week_data.get("hadir", []):
                    hadir_count += 1
            
            # Calculate percentage
            kehadiran_pct = (hadir_count / total_weeks * 100) if total_weeks > 0 else 0
            
            data.append({
                "Nama": staf,
                "Kehadiran (%)": round(kehadiran_pct, 1),
                "Partisipasi (1-10)": 8 if kehadiran_pct >= 80 else 7 if kehadiran_pct >= 60 else 6,
                "Catatan": "",
            })
        
        st.session_state.keaktifan_staf = pd.DataFrame(data)
    
    # Live Practice Tracking - map practices to 4 sessions
    if "live_practice" not in st.session_state:
        data = []
        
        for staf in STAF_NEWSCASTING:
            practices = PRACTICE_DATA.get(staf, [])
            jumlah_practice = len(practices)
            catatan_weeks = ", ".join(practices) if practices else "Belum ada practice"
            
            data.append({
                "Nama": staf,
                "Jumlah Practice": jumlah_practice,
                "Catatan": catatan_weeks,
            })
        
        st.session_state.live_practice = pd.DataFrame(data)
    
    # Evaluasi Divisi
    if "evaluasi_divisi" not in st.session_state:
        st.session_state.evaluasi_divisi = pd.DataFrame([
            {
                "Kategori": cat,
                "Rating (1-10)": 7,
                "Kekuatan": "",
                "Area Perbaikan": "",
                "Action Plan": "",
            }
            for cat in EVALUASI_CATEGORIES
        ])
    
    # Penilaian Staf (Komprehensif)
    if "penilaian_staf" not in st.session_state:
        st.session_state.penilaian_staf = pd.DataFrame([
            {
                "Nama": staf,
                "Teknik Vokal (1-10)": 7,
                "Artikulasi (1-10)": 7,
                "Bahasa Tubuh (1-10)": 7,
                "On-Camera Presence (1-10)": 7,
                "Penulisan Naskah (1-10)": 7,
                "Improvisasi (1-10)": 7,
                "Overall (1-10)": 7,
                "Catatan": "",
            }
            for staf in STAF_NEWSCASTING
        ])


# ============================================================================
# RENDER FUNCTIONS FOR EACH SECTION
# ============================================================================

def render_overview():
    """Section 1: Overview Dashboard."""
    st.title("📊 Dashboard Overview")
    st.markdown("**Divisi INTEL Fasilkom UNSRI** - Program Pengajaran Newscasting")
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Weekly completion
    weekly_completion = calculate_completion_rate(st.session_state.progress_pengajaran)
    col1.metric(
        "📚 Weekly Sessions",
        f"{(st.session_state.progress_pengajaran['Status'] == 'Selesai').sum()}/12",
        f"{weekly_completion:.1f}%"
    )
    
    # Average kehadiran staf
    avg_kehadiran = st.session_state.keaktifan_staf["Kehadiran (%)"].mean()
    col2.metric("👥 Kehadiran Rata-rata", f"{avg_kehadiran:.1f}%")
    
    # Live practice total
    total_practice = st.session_state.live_practice["Jumlah Practice"].sum()
    col3.metric("🎬 Total Practice", f"{total_practice}")
    
    # Overall rating
    avg_penilaian = st.session_state.penilaian_staf["Overall (1-10)"].mean()
    col4.metric("⭐ Rating Rata-rata", f"{avg_penilaian:.1f}/10")
    
    st.markdown("---")
    
    # Progress Bars
    st.subheader("🎯 Progress Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📚 Progress Pengajaran 12 Weeks")
        completed_weeks = (st.session_state.progress_pengajaran['Status'] == 'Selesai').sum()
        render_progress_bar(completed_weeks, 12, "")
        
        st.markdown("##### 👥 Keaktifan Staf")
        active_staf = (st.session_state.keaktifan_staf["Kehadiran (%)"] >= 75).sum()
        render_progress_bar(active_staf, len(STAF_NEWSCASTING), "Staf Aktif (≥75% kehadiran)")
    
    with col2:
        st.markdown("##### 🎬 Live Practice")
        staf_with_practice = (st.session_state.live_practice["Jumlah Practice"] > 0).sum()
        render_progress_bar(staf_with_practice, len(STAF_NEWSCASTING), "Staf Sudah Practice")
        
    
    st.markdown("---")
    
    # Charts
    st.subheader("📈 Visualisasi")
    
    tab1, tab2 = st.tabs(["Weekly Progress", "Keaktifan Staf"])
    
    with tab1:
        # Weekly progress chart
        weekly_data = st.session_state.progress_pengajaran.copy()
        weekly_data["Week_Num"] = range(1, 13)
        chart = alt.Chart(weekly_data).mark_bar().encode(
            x=alt.X("Week_Num:O", title="Week"),
            y=alt.Y("Materi Delivered (%):Q", title="Materi Delivered (%)"),
            color=alt.Color("Status:N", scale=alt.Scale(
                domain=["Belum Mulai", "Sedang Berjalan", "Selesai", "Tertunda"],
                range=["#ff4444", "#ffaa00", "#44ff44", "#ff8800"]
            )),
            tooltip=["Week", "Status", "Materi Delivered (%)", "Kehadiran (%)"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)
    
    with tab2:
        # Keaktifan chart
        keaktifan_data = st.session_state.keaktifan_staf.copy()
        chart = alt.Chart(keaktifan_data).mark_bar().encode(
            x=alt.X("Nama:N", title="Staf", sort="-y"),
            y=alt.Y("Kehadiran (%):Q", title="Kehadiran (%)"),
            color=alt.condition(
                alt.datum["Kehadiran (%)"] >= 75,
                alt.value("#44ff44"),
                alt.value("#ff4444")
            ),
            tooltip=["Nama", "Kehadiran (%)", "Partisipasi (1-10)"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")


def render_progress_pengajaran():
    """Section 2: Progress Pengajaran (12 Weekly Sessions)."""
    st.header("📚 Progress Pengajaran - 12 Weekly Sessions")
    st.markdown("Kelola progress pengajaran newscasting untuk 12 minggu.")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    total_weeks = 12
    completed = (st.session_state.progress_pengajaran["Status"] == "Selesai").sum()
    ongoing = (st.session_state.progress_pengajaran["Status"] == "Sedang Berjalan").sum()
    avg_kehadiran = st.session_state.progress_pengajaran["Kehadiran (%)"].mean()
    
    col1.metric("Total Weeks", f"{completed}/{total_weeks}")
    col2.metric("Sedang Berjalan", ongoing)
    col3.metric("Avg Kehadiran", f"{avg_kehadiran:.1f}%")
    col4.metric("Completion", f"{(completed/total_weeks*100):.1f}%")
    
    st.markdown("---")
    
    # Editable table
    st.subheader("📝 Data Pengajaran")
    st.caption("Klik cell untuk edit. Tambah/hapus baris dengan tombol di tabel.")
    
    edited_df = st.data_editor(
        st.session_state.progress_pengajaran,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Belum Mulai", "Sedang Berjalan", "Selesai", "Tertunda"],
                required=True,
            ),
            "Kehadiran (%)": st.column_config.NumberColumn(
                "Kehadiran (%)",
                min_value=0,
                max_value=100,
                step=5,
            ),
            "Materi Delivered (%)": st.column_config.NumberColumn(
                "Materi Delivered (%)",
                min_value=0,
                max_value=100,
                step=5,
            ),
        },
        key="editor_pengajaran"
    )
    st.session_state.progress_pengajaran = edited_df
    
    # Visual breakdown
    st.markdown("---")
    st.subheader("📊 Status Breakdown")
    
    status_counts = edited_df["Status"].value_counts()
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("🟢 Selesai", status_counts.get("Selesai", 0))
    col2.metric("🟡 Sedang Berjalan", status_counts.get("Sedang Berjalan", 0))
    col3.metric("🔴 Belum Mulai", status_counts.get("Belum Mulai", 0))
    col4.metric("🟠 Tertunda", status_counts.get("Tertunda", 0))


def render_keaktifan_staf():
    """Section 3: Keaktifan Staf Newscasting."""
    st.header("👥 Keaktifan Staf Newscasting")
    st.markdown("Monitor dan evaluasi keaktifan staf dalam program pengajaran.")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    df = st.session_state.keaktifan_staf
    avg_kehadiran = df["Kehadiran (%)"].mean()
    avg_partisipasi = df["Partisipasi (1-10)"].mean()
    active_staf = (df["Kehadiran (%)"] >= 75).sum()
    
    col1.metric("Avg Kehadiran", f"{avg_kehadiran:.1f}%")
    col2.metric("Avg Partisipasi", f"{avg_partisipasi:.1f}/10")
    col3.metric("Staf Aktif (≥75%)", f"{active_staf}/{len(STAF_NEWSCASTING)}")
    
    st.markdown("---")
    
    # Editable table
    st.subheader("📝 Data Keaktifan Staf")
    
    edited_df = st.data_editor(
        st.session_state.keaktifan_staf,
        use_container_width=True,
        column_config={
            "Kehadiran (%)": st.column_config.NumberColumn(
                "Kehadiran (%)",
                min_value=0,
                max_value=100,
                step=5,
            ),
            "Partisipasi (1-10)": st.column_config.NumberColumn(
                "Partisipasi (1-10)",
                min_value=1,
                max_value=10,
                step=1,
            ),
        },
        key="editor_keaktifan"
    )
    st.session_state.keaktifan_staf = edited_df
    
    # Chart
    st.markdown("---")
    st.subheader("📊 Visualisasi Keaktifan")
    
    chart_data = edited_df.copy()
    
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("Nama:N", title="Staf", sort="-y"),
        y=alt.Y("Kehadiran (%):Q", title="Kehadiran (%)"),
        color=alt.Color("Partisipasi (1-10):Q", scale=alt.Scale(scheme="viridis"), title="Partisipasi"),
        tooltip=["Nama", "Kehadiran (%)", "Partisipasi (1-10)"]
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)


def render_live_practice():
    """Section 4: Live Practice Tracking."""
    st.header("🎬 Live Practice Tracking")
    st.markdown("Track jumlah practice setiap staf dari weekly meetings.")
    
    df = st.session_state.live_practice.copy()
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    total_practices = df["Jumlah Practice"].sum()
    avg_practice = df["Jumlah Practice"].mean()
    max_practice = df["Jumlah Practice"].max()
    staf_with_practice = (df["Jumlah Practice"] > 0).sum()
    
    col1.metric("Total Practice", f"{total_practices}")
    col2.metric("Avg Practice per Staf", f"{avg_practice:.1f}")
    col3.metric("Staf Sudah Practice", f"{staf_with_practice}/{len(STAF_NEWSCASTING)}")
    
    st.markdown("---")
    
    # Editable table
    st.subheader("📝 Data Live Practice")
    st.caption("Jumlah practice adalah akumulasi dari practice saat weekly meeting")
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        column_config={
            "Jumlah Practice": st.column_config.NumberColumn(
                "Jumlah Practice",
                min_value=0,
                max_value=20,
                step=1,
                help="Total berapa kali practice saat weekly meeting"
            ),
        },
        key="editor_practice"
    )
    
    st.session_state.live_practice = edited_df
    
    # Chart
    st.markdown("---")
    st.subheader("📊 Practice per Staf")
    
    # Add color category for visualization
    edited_df_chart = edited_df.copy()
    edited_df_chart["Kategori"] = edited_df_chart["Jumlah Practice"].apply(
        lambda x: "Aktif (≥3x)" if x >= 3 else "Cukup (1-2x)" if x >= 1 else "Belum Practice"
    )
    
    chart = alt.Chart(edited_df_chart).mark_bar().encode(
        x=alt.X("Nama:N", title="Staf", sort="-y"),
        y=alt.Y("Jumlah Practice:Q", title="Jumlah Practice"),
        color=alt.Color("Kategori:N", 
            scale=alt.Scale(
                domain=["Aktif (≥3x)", "Cukup (1-2x)", "Belum Practice"],
                range=["#44ff44", "#ffaa00", "#ff4444"]
            ),
            title="Kategori"
        ),
        tooltip=["Nama", "Jumlah Practice", "Catatan"]
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)


def render_evaluasi_divisi():
    """Section 5: Evaluasi Divisi."""
    st.header("📝 Evaluasi Divisi")
    st.markdown("Evaluasi komprehensif untuk divisi INTEL dalam pelaksanaan program pengajaran.")
    
    # Quick stats
    df = st.session_state.evaluasi_divisi
    avg_rating = df["Rating (1-10)"].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Rating", f"{avg_rating:.1f}/10")
    col2.metric("Total Kategori", len(EVALUASI_CATEGORIES))
    excellent = (df["Rating (1-10)"] >= 8).sum()
    col3.metric("Excellent (≥8)", f"{excellent}/{len(EVALUASI_CATEGORIES)}")
    
    st.markdown("---")
    
    # Editable table
    st.subheader("📝 Data Evaluasi")
    
    edited_df = st.data_editor(
        st.session_state.evaluasi_divisi,
        use_container_width=True,
        column_config={
            "Rating (1-10)": st.column_config.NumberColumn(
                "Rating (1-10)",
                min_value=1,
                max_value=10,
                step=1,
            ),
        },
        key="editor_evaluasi"
    )
    st.session_state.evaluasi_divisi = edited_df
    
    # Chart
    st.markdown("---")
    st.subheader("📊 Rating per Kategori")
    
    chart = alt.Chart(edited_df).mark_bar().encode(
        x=alt.X("Kategori:N", title="Kategori"),
        y=alt.Y("Rating (1-10):Q", title="Rating", scale=alt.Scale(domain=[0, 10])),
        color=alt.Color("Rating (1-10):Q", scale=alt.Scale(scheme="goldred"), title="Rating"),
        tooltip=["Kategori", "Rating (1-10)", "Kekuatan", "Area Perbaikan"]
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)
    
    # Summary insights
    st.markdown("---")
    st.subheader("💡 Insights & Action Items")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Kekuatan (Strengths)**")
        for _, row in edited_df.iterrows():
            if row["Kekuatan"]:
                st.markdown(f"• **{row['Kategori']}**: {row['Kekuatan']}")
    
    with col2:
        st.markdown("**🔧 Area Perbaikan**")
        for _, row in edited_df.iterrows():
            if row["Area Perbaikan"]:
                st.markdown(f"• **{row['Kategori']}**: {row['Area Perbaikan']}")


def render_penilaian_staf():
    """Section 6: Penilaian Staf (Komprehensif)."""
    st.header("⭐ Penilaian Staf Newscasting")
    st.markdown("Penilaian komprehensif untuk setiap staf berdasarkan 6 aspek newscasting.")
    
    # Auto-calculate overall
    df = st.session_state.penilaian_staf.copy()
    aspect_cols = [
        "Teknik Vokal (1-10)", "Artikulasi (1-10)", "Bahasa Tubuh (1-10)",
        "On-Camera Presence (1-10)", "Penulisan Naskah (1-10)", "Improvisasi (1-10)"
    ]
    
    for idx, row in df.iterrows():
        avg = sum([row[col] for col in aspect_cols]) / len(aspect_cols)
        df.at[idx, "Overall (1-10)"] = round(avg, 1)
    
    st.session_state.penilaian_staf = df
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    avg_overall = df["Overall (1-10)"].mean()
    excellent_staf = (df["Overall (1-10)"] >= 8).sum()
    avg_vokal = df["Teknik Vokal (1-10)"].mean()
    avg_camera = df["On-Camera Presence (1-10)"].mean()
    
    col1.metric("Avg Overall", f"{avg_overall:.1f}/10")
    col2.metric("Excellent (≥8)", f"{excellent_staf}/{len(STAF_NEWSCASTING)}")
    col3.metric("Avg Teknik Vokal", f"{avg_vokal:.1f}/10")
    col4.metric("Avg On-Camera", f"{avg_camera:.1f}/10")
    
    st.markdown("---")
    
    # Editable table
    st.subheader("📝 Data Penilaian")
    st.caption("Overall score dihitung otomatis dari rata-rata 6 aspek.")
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        column_config={
            "Teknik Vokal (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "Artikulasi (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "Bahasa Tubuh (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "On-Camera Presence (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "Penulisan Naskah (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "Improvisasi (1-10)": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "Overall (1-10)": st.column_config.NumberColumn(disabled=True),
        },
        key="editor_penilaian"
    )
    
    # Recalculate overall
    for idx, row in edited_df.iterrows():
        avg = sum([row[col] for col in aspect_cols]) / len(aspect_cols)
        edited_df.at[idx, "Overall (1-10)"] = round(avg, 1)
    
    st.session_state.penilaian_staf = edited_df
    
    # Charts
    st.markdown("---")
    st.subheader("📊 Visualisasi Penilaian")
    
    tab1, tab2 = st.tabs(["Overall Ranking", "Detail per Aspek"])
    
    with tab1:
        # Overall ranking
        chart = alt.Chart(edited_df).mark_bar().encode(
            x=alt.X("Nama:N", title="Staf", sort="-y"),
            y=alt.Y("Overall (1-10):Q", title="Overall Score", scale=alt.Scale(domain=[0, 10])),
            color=alt.Color("Overall (1-10):Q", scale=alt.Scale(scheme="viridis"), title="Score"),
            tooltip=["Nama", "Overall (1-10)"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)
    
    with tab2:
        # Detailed aspect comparison
        melted = edited_df.melt(
            id_vars=["Nama"],
            value_vars=aspect_cols,
            var_name="Aspek",
            value_name="Score"
        )
        
        # Clean aspect names
        melted["Aspek"] = melted["Aspek"].str.replace(" (1-10)", "")
        
        chart = alt.Chart(melted).mark_boxplot().encode(
            x=alt.X("Aspek:N", title="Aspek Penilaian"),
            y=alt.Y("Score:Q", title="Score (1-10)", scale=alt.Scale(domain=[0, 10])),
            color="Aspek:N"
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
    
    # Top performers
    st.markdown("---")
    st.subheader("🏆 Top Performers")
    
    top_3 = edited_df.nlargest(3, "Overall (1-10)")
    
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (idx, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            st.markdown(f"### {medals[i]} {row['Nama']}")
            st.metric("Overall Score", f"{row['Overall (1-10)']}/10")
            st.caption(row['Catatan'] if row['Catatan'] else "No notes")


# ============================================================================
# EXPORT & UTILITY FUNCTIONS
# ============================================================================

def export_all_data():
    """Export all session data to JSON."""
    data = {
        "metadata": {
            "exported_at": datetime.now().isoformat(),
            "divisi": "INTEL Fasilkom UNSRI",
            "program": "Pengajaran Newscasting",
        },
        "progress_pengajaran": st.session_state.progress_pengajaran.to_dict(orient="records"),
        "keaktifan_staf": st.session_state.keaktifan_staf.to_dict(orient="records"),
        "live_practice": st.session_state.live_practice.to_dict(orient="records"),
        "evaluasi_divisi": st.session_state.evaluasi_divisi.to_dict(orient="records"),
        "penilaian_staf": st.session_state.penilaian_staf.to_dict(orient="records"),
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_to_csv():
    """Export all data to CSV format (multiple sheets simulation)."""
    output = []
    
    sections = [
        ("Progress Pengajaran", st.session_state.progress_pengajaran),
        ("Keaktifan Staf", st.session_state.keaktifan_staf),
        ("Live Practice", st.session_state.live_practice),
        ("Evaluasi Divisi", st.session_state.evaluasi_divisi),
        ("Penilaian Staf", st.session_state.penilaian_staf),
    ]
    
    for section_name, df in sections:
        output.append(f"\n=== {section_name} ===\n")
        output.append(df.to_csv(index=False))
    
    return "\n".join(output)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="Dashboard Progress Report - Divisi INTEL",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Initialize session state
    init_session_state()
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stMetric {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("📰 Dashboard Progress Report")
    st.markdown("**Divisi INTEL Fasilkom UNSRI** - Program Pengajaran Newscasting")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        # Use relative path for logo
        try:
            st.image("Logo intel.jpg", use_container_width=True)
        except:
            st.markdown("### 📰 INTEL Dashboard")
        st.markdown("### Navigation")
        
        section = st.radio(
            "Pilih Section:",
            [
                "📊 Overview Dashboard",
                "📚 Progress Pengajaran",
                "👥 Keaktifan Staf",
                "🎬 Live Practice",
                "📝 Evaluasi Divisi",
                "⭐ Penilaian Staf",
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            json_data = export_all_data()
            st.download_button(
                label="JSON",
                data=json_data,
                file_name=f"progress_report_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
            )
        
        with col2:
            csv_data = export_to_csv()
            st.download_button(
                label="CSV",
                data=csv_data,
                file_name=f"progress_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        
        st.markdown("---")
        st.info(f"**Total Staf**: {len(STAF_NEWSCASTING)}\n\n**Total Weeks**: 12")
        
        st.markdown("---")
        st.caption("Dashboard v2.0 - Divisi INTEL Fasilkom UNSRI")
    
    # Render selected section
    if section == "📊 Overview Dashboard":
        render_overview()
    elif section == "📚 Progress Pengajaran":
        render_progress_pengajaran()
    elif section == "👥 Keaktifan Staf":
        render_keaktifan_staf()
    elif section == "🎬 Live Practice":
        render_live_practice()
    elif section == "📝 Evaluasi Divisi":
        render_evaluasi_divisi()
    elif section == "⭐ Penilaian Staf":
        render_penilaian_staf()


if __name__ == "__main__":
    main()
