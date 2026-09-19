# -*- coding: utf-8 -*-
"""
HydroCarrier AI — LOHC Discovery & Predictor Platform
منصة هايدروكارير الذكي لاستكشاف وتقييم نواقل الهيدروجين العضوية السائلة (LOHC)
Energy Hackathon 2026 — Innovative Vision Track
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    RDKIT_AVAILABLE = True
except Exception:
    RDKIT_AVAILABLE = False

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except Exception:
    FPDF_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

PRIMARY = "#3a566e"
PRIMARY_DARK = "#22374a"
ACCENT = "#71aeca"
ACCENT_LIGHT = "#eaf3f8"
AMBER = "#e0a03c"
DANGER = "#c0392b"
OK = "#2e7d32"
WARN = "#b8860b"

st.set_page_config(
    page_title="HydroCarrier AI | هايدروكارير الذكي",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Language toggle (top of page, before any CSS so direction can adapt)
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

_, lang_box = st.columns([6, 1])
with lang_box:
    choice = st.selectbox(
        "🌐", ["العربية", "English"],
        index=0 if st.session_state.lang == "ar" else 1,
        label_visibility="collapsed", key="lang_picker",
    )
    st.session_state.lang = "ar" if choice == "العربية" else "en"

L = st.session_state.lang
IS_AR = L == "ar"


def tt(ar, en):
    return ar if IS_AR else en


# ---------------------------------------------------------------------------
# Global CSS — modernized: gradient header, soft shadows, richer cards
# ---------------------------------------------------------------------------
direction = "rtl" if IS_AR else "ltr"
border_side = "right" if IS_AR else "left"

st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        direction: {direction};
        font-family: 'Segoe UI', 'Tahoma', sans-serif;
    }}
    .block-container {{ padding-top: 1rem; max-width: 1200px; }}
    h1, h2, h3, h4 {{ color: {PRIMARY}; font-weight: 800; }}

    .hc-hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 55%, #1a2c3a 100%);
        border-radius: 18px;
        padding: 22px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(34,55,74,0.25);
    }}
    .hc-hero h1 {{ color: white !important; margin: 0 0 4px 0; font-size: 26px; }}
    .hc-hero p {{ color: {ACCENT_LIGHT}; margin: 0; font-size: 14px; }}

    .hc-card {{
        background: white;
        border: 1px solid #e6edf2;
        border-{border_side}: 5px solid {ACCENT};
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(58,86,110,0.06);
    }}
    .hc-decision {{
        border-radius: 16px;
        padding: 18px 22px;
        margin: 10px 0 18px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .hc-decision.high {{ background: linear-gradient(135deg, #e8f5e9 0%, #d3ede4 100%); border: 1.5px solid {OK}; }}
    .hc-decision.mid  {{ background: linear-gradient(135deg, #fff8e1 0%, #ffedc2 100%); border: 1.5px solid {WARN}; }}
    .hc-decision.low  {{ background: linear-gradient(135deg, #fdecea 0%, #fbd9d5 100%); border: 1.5px solid {DANGER}; }}
    .hc-decision .tag {{ font-weight: 800; font-size: 15px; margin-bottom: 4px; display:block; }}
    .hc-decision.high .tag {{ color: {OK}; }}
    .hc-decision.mid .tag {{ color: {WARN}; }}
    .hc-decision.low .tag {{ color: {DANGER}; }}
    .hc-decision .txt {{ font-size: 13.5px; color: #2c3e40; }}

    .hc-src-badge {{
        background: {ACCENT_LIGHT}; color: {PRIMARY};
        padding: 2px 10px; border-radius: 20px;
        font-size: 10.5px; font-weight: 700; display: inline-block; margin-top: 6px;
    }}
    .hc-badge-warn {{
        background: linear-gradient(135deg, #fff8e1, #ffedc2); color: #7a5c00; padding: 10px 14px; border-radius: 12px;
        font-size: 12.5px; font-weight: 600; border: 1px solid {WARN};
    }}
    .hc-badge-ok {{
        background: linear-gradient(135deg, #e8f5e9, #d3ede4); color: {OK}; padding: 10px 14px; border-radius: 12px;
        font-size: 12.5px; font-weight: 700; border: 1px solid {OK}; display: inline-block;
    }}
    div[data-testid="stMetric"] {{
        background: linear-gradient(160deg, {ACCENT_LIGHT} 0%, #ffffff 100%);
        border-radius: 14px; padding: 12px 8px; border: 1px solid #d7e7ef;
        box-shadow: 0 2px 6px rgba(58,86,110,0.05);
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {ACCENT_LIGHT}; border-radius: 10px 10px 0 0;
        padding: 9px 18px; font-weight: 700; color: {PRIMARY};
    }}
    .stTabs [aria-selected="true"] {{ background-color: {PRIMARY} !important; color: white !important; }}
    .hc-arrow-box {{
        display: flex; align-items: center; justify-content: center; gap: 14px;
        background: {ACCENT_LIGHT}; border-radius: 14px; padding: 14px; margin: 8px 0 16px 0;
    }}
    .hc-arrow-box .lbl {{ font-weight: 700; color: {PRIMARY}; font-size: 12.5px; text-align: center; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
logo_h_path = os.path.join(ASSETS_DIR, "hydrocarrier_logo_horizontal.png")
if os.path.exists(logo_h_path):
    st.image(logo_h_path, width=380)

st.markdown(f"""
<div class="hc-hero">
  <h1>⚡ {tt("مستكشف ناقلات الهيدروجين", "Hydrogen Carrier Explorer")}</h1>
  <p>{tt("رتّب المرشحين وفق السعة، متطلبات إزالة الهدرجة، وقابلية التشغيل.", "Rank candidates by capacity, dehydrogenation requirements, and operability.")}</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def smiles_to_image(smiles_str, size=(220, 220)):
    if not RDKIT_AVAILABLE or not isinstance(smiles_str, str):
        return None
    try:
        mol = Chem.MolFromSmiles(smiles_str)
        if mol:
            return Draw.MolToImage(mol, size=size)
    except Exception:
        return None
    return None


@st.cache_data
def load_verified_dataset():
    return pd.read_excel(os.path.join(DATA_DIR, "LOHC_Dataset_Verified.xlsx"), sheet_name="LOHC_Dataset_Verified")


@st.cache_data
def load_experimental_dataset():
    return pd.read_excel(os.path.join(DATA_DIR, "LOHC_Complete_Dataset_With_Cycles.xlsx"))


@st.cache_data
def load_qm9_known():
    return pd.read_csv(os.path.join(DATA_DIR, "QM9_G4MP2_all.csv"))


@st.cache_data
def load_qm9_candidates():
    return pd.read_csv(os.path.join(DATA_DIR, "QM9-LOHC_new_molecules.csv"))


# Structured, bilingual phase-viability alerts for the 3 known flagged systems
# (replaces the raw English Notes text with a proper problem/consequence structure)
PHASE_ALERTS = {
    "Furan": {
        "boiling": "66°C", "release": "180°C",
        "ar_problem": "نقطة غليان الحامل 66°م أقل بكثير من درجة حرارة الإطلاق المطلوبة 180°م.",
        "ar_result": "قد لا يبقى الحامل سائلاً عند الضغط الجوي؛ يحتاج مراجعة ضغط التشغيل أو استبعاده من تطبيقات الطور السائل.",
        "en_problem": "Carrier boiling point (66°C) is far below the required release temperature (180°C).",
        "en_result": "The carrier may not remain liquid at atmospheric pressure; operating pressure needs review or the system should be excluded from liquid-phase applications.",
    },
    "2-Methyltetrahydrofuran": {
        "boiling": "78-80°C", "release": "190°C",
        "ar_problem": "نقطة غليان الحامل 78-80°م أقل بكثير من درجة حرارة الإطلاق المطلوبة 190°م.",
        "ar_result": "نفس مشكلة التطاير؛ يحتاج مراجعة ضغط التشغيل قبل الاعتماد.",
        "en_problem": "Carrier boiling point (78-80°C) is far below the required release temperature (190°C).",
        "en_result": "Same volatility concern; operating pressure needs review before adoption.",
    },
    "Dibenzothiophene": {
        "boiling": None, "release": None,
        "ar_problem": "الحامل يحتوي كبريتاً، وهو عنصر معروف بتسميمه لحفازات البلاتين.",
        "ar_result": "خطر تسمم الحفاز غير منعكس في قيمة الاستقرار المعروضة؛ يستحق تقييماً إضافياً قبل الاعتماد الصناعي.",
        "en_problem": "The carrier contains sulfur, a well-documented poison for platinum-group catalysts.",
        "en_result": "This catalyst-poisoning risk is not reflected in the displayed retention value; it warrants further evaluation before industrial adoption.",
    },
}


def get_phase_alert(name):
    for key, alert in PHASE_ALERTS.items():
        if key.lower() in name.lower():
            return alert
    return None


def compute_priority(capacity, retention, has_note):
    """Simple, transparent rule-based scoring — not a trained model."""
    score = 0
    if capacity >= 5.5:
        score += 1
    if retention >= 90:
        score += 1
    if not has_note:
        score += 1
    if score >= 3:
        return "high"
    elif score == 2:
        return "mid"
    return "low"


PRIORITY_LABEL = {
    "high": {"ar": "مرتفعة", "en": "High"},
    "mid": {"ar": "متوسطة", "en": "Medium"},
    "low": {"ar": "منخفضة", "en": "Low"},
}
DECISION_TEXT = {
    "high": {
        "ar": "مرشح واعد حوسبياً ويستحق الانتقال إلى مرحلة المراجعة أو الاختبار.",
        "en": "A computationally promising candidate that warrants moving to the review or testing stage.",
    },
    "mid": {
        "ar": "مرشح واعد من ناحية السعة، لكنه يحتاج إلى مراجعة ظروف الطور والضغط قبل اعتماده للتطوير.",
        "en": "Promising in terms of capacity, but needs a review of phase and pressure conditions before development adoption.",
    },
    "low": {
        "ar": "لا يُوصى به في ظروف التشغيل الحالية بسبب عدم توافق خواصه الفيزيائية مع درجة إزالة الهدرجة.",
        "en": "Not recommended under current operating conditions due to a mismatch between its physical properties and the dehydrogenation temperature.",
    },
}

def build_candidate_csv(carrier_data, cap_col, priority, alert_text=""):
    """Returns CSV bytes for the selected candidate, in the active UI language."""
    rows = [
        (tt("اسم المرشح", "Candidate Name"), carrier_data["LOHC_Name"]),
        ("SMILES", carrier_data["SMILES"]),
        (tt("السعة الوزنية (wt%)", "Gravimetric Capacity (wt%)"), f"{carrier_data[cap_col]:.2f}"),
        (tt("حرارة الإطلاق (°م)", "Release Temperature (°C)"), carrier_data["Release_Temp_C"]),
        (tt("الاستقرار (50 دورة، %)", "Stability (50 cycles, %)"), carrier_data["Retention_50_Cycles"]),
        (tt("نظام الحفاز", "Catalyst System"), f"{carrier_data['Catalyst_Metal']} / {carrier_data['Support_Material']}"),
        (tt("أولوية التطوير", "Development Priority"), PRIORITY_LABEL[priority][L]),
        (tt("التوصية النهائية", "Final Recommendation"), DECISION_TEXT[priority][L]),
        (tt("تنبيه هندسي", "Engineering Alert"), alert_text or tt("لا يوجد", "None")),
    ]
    df_out = pd.DataFrame(rows, columns=[tt("الحقل", "Field"), tt("القيمة", "Value")])
    return df_out.to_csv(index=False).encode("utf-8-sig")  # BOM so Excel shows Arabic correctly


def build_candidate_pdf(carrier_data, cap_col, priority, alert_problem="", alert_result=""):
    """Returns PDF bytes for the selected candidate. Always in English for reliable rendering."""
    if not FPDF_AVAILABLE:
        return None
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(58, 86, 110)
    pdf.cell(0, 12, "HydroCarrier AI - Candidate Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 8, "Energy Hackathon 2026 - Innovative Vision Track", ln=True)
    pdf.ln(4)

    pdf.set_draw_color(113, 174, 202)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    def field(label, value):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(58, 86, 110)
        pdf.cell(60, 8, label, ln=False)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 8, str(value))

    field("Candidate Name:", carrier_data["LOHC_Name"])
    field("SMILES:", carrier_data["SMILES"])
    field("Gravimetric Capacity:", f"{carrier_data[cap_col]:.2f} wt%  (source: computed & chemically verified)")
    field("Release Temperature:", f"{carrier_data['Release_Temp_C']} deg C  (source: reference data)")
    field("Stability (50 cycles):", f"{carrier_data['Retention_50_Cycles']}%  (source: reference data)")
    field("Catalyst System:", f"{carrier_data['Catalyst_Metal']} / {carrier_data['Support_Material']}")
    field("Development Priority:", PRIORITY_LABEL[priority]["en"])

    pdf.ln(2)
    pdf.set_fill_color(234, 243, 248)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(58, 86, 110)
    pdf.multi_cell(0, 8, "Initial Screening Decision:", fill=True)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 7, DECISION_TEXT[priority]["en"])

    if alert_problem:
        pdf.ln(2)
        pdf.set_fill_color(255, 248, 225)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(122, 92, 0)
        pdf.multi_cell(0, 8, "Liquid-Phase Viability Alert:", fill=True)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.multi_cell(0, 7, f"{alert_problem} {alert_result}")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(140, 140, 140)
    pdf.multi_cell(0, 6, "Generated by HydroCarrier AI. Values are computational screening estimates, not a substitute for laboratory validation.")

    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_exp, tab_screen, tab_qm9, tab_about = st.tabs([
    tt("🏠 نظرة عامة", "🏠 Overview"),
    tt("🧪 القاعدة التجريبية الموثقة", "🧪 Documented Experimental Data"),
    tt("📊 مسح المرشحين (48 نظام)", "📊 Candidate Screening (48 systems)"),
    tt("🔬 الاستكشاف الكمي (QM9)", "🔬 Quantum Exploration (QM9)"),
    tt("ℹ️ عن المنصة", "ℹ️ About"),
])

# ============================= TAB: OVERVIEW ===============================
with tab_overview:
    try:
        df_exp_p = load_experimental_dataset()
        df_screen_p = load_verified_dataset()
        df_qm9_p = load_qm9_known()
        df_cand_p = load_qm9_candidates()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(tt("أنظمة تجريبية موثّقة", "Documented experimental systems"), f"{df_exp_p['LOHC_Pair'].nunique()}")
        c2.metric(tt("مرشحون مُفحوصون", "Screened candidates"), f"{len(df_screen_p)}")
        c3.metric(tt("جزيئات QM9", "QM9 molecules"), f"{len(df_qm9_p):,}")
        c4.metric(tt("مرشحون جدد", "New candidates"), f"{len(df_cand_p):,}")
    except Exception as e:
        st.warning(f"{tt('تعذر تحميل بعض الملفات:', 'Could not load some files:')} {e}")

    st.markdown(f"### 💡 {tt('فكرة المشروع', 'Project Idea')}")
    st.markdown(f'''<div class="hc-card">{tt(
        "HydroCarrier AI لا تعرض أعلى سعة فقط؛ بل تحدد أي المرشحين يستحق الانتقال إلى مرحلة التطوير التالية ولماذا. من مساحة كيميائية واسعة إلى قرار تطوير قابل للتفسير — اكتشاف أسرع، مقارنة أذكى، وتطوير أكثر كفاءة لناقلات الهيدروجين.",
        "HydroCarrier AI doesn't just show the highest capacity — it identifies which candidates deserve to move to the next development stage, and why. From a wide chemical space to an explainable development decision — faster discovery, smarter comparison, and more efficient hydrogen carrier development."
    )}</div>''', unsafe_allow_html=True)

# ===================== TAB: EXPERIMENTAL (REAL, CITED) =====================
with tab_exp:
    st.subheader(tt("🧪 الأنظمة التجريبية الموثقة بمصادر أدبية منشورة", "🧪 Experimental Systems Documented in Published Literature"))
    st.caption(tt("كل صف مرتبط بمصدر علمي منشور فعلياً.", "Every row is linked to an actually published scientific source."))
    try:
        df_exp = load_experimental_dataset()
        pairs = sorted(df_exp["LOHC_Pair"].unique())
        selected_pair = st.selectbox(tt("اختر نظام الناقل:", "Select carrier system:"), pairs)
        subset = df_exp[df_exp["LOHC_Pair"] == selected_pair].reset_index(drop=True)
        st.markdown(f"#### {tt('النتائج المسجلة لـ', 'Recorded results for')} **{selected_pair}** ({len(subset)} {tt('تجربة', 'trial(s)')})")

        for i, row in subset.iterrows():
            with st.container():
                cimg, cdata = st.columns([1, 3])
                with cimg:
                    img = smiles_to_image(row.get("SMILES"))
                    if img:
                        st.image(img, width=160)
                    else:
                        st.code(row.get("SMILES", ""), language=None)
                with cdata:
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric(tt("السعة الوزنية", "Gravimetric Capacity"), f"{row['H2_Capacity_wt%']:.2f}%")
                    k2.metric(tt("حرارة الإطلاق", "Release Temp"), f"{row['Temperature_C']:.0f}°C")
                    k3.metric(tt("نسبة التحول", "Conversion"), f"{row['Conversion_%']:.1f}%")
                    k4.metric(tt("الاحتفاظ بالسعة", "Capacity Retention"), f"{row['Capacity_Retention_%']:.1f}%",
                               f"{tt('عبر', 'over')} {int(row['Cycles'])} {tt('دورة', 'cycles')}")
                    st.markdown(
                        f"{tt('**الحفاز:**', '**Catalyst:**')} {row['Catalyst']} ({tt('تحميل', 'loading')} {row['Catalyst_Loading_wt%']}%) &nbsp;|&nbsp; "
                        f"{tt('**الضغط:**', '**Pressure:**')} {row['Pressure_bar']} bar &nbsp;|&nbsp; "
                        f"{tt('**إنثالبي النزع:**', '**Release Enthalpy:**')} {row['Enthalpy_kJmol_H2']} kJ/mol H2 &nbsp;|&nbsp; "
                        f"{tt('**الحالة:**', '**State:**')} {row['State']}"
                    )
                    st.markdown(
                        f'<span class="hc-src-badge">📚 {tt("مصدر الحفاز", "Catalyst source")}: {row["Data_Source_Catalyst"]}</span> '
                        f'<span class="hc-src-badge">📚 {tt("مصدر الخواص", "Property source")}: {row["Data_Source_Properties"]}</span>',
                        unsafe_allow_html=True,
                    )
            st.markdown("---")

        st.markdown(f"#### 📈 {tt('السعة مقابل حرارة الإطلاق', 'Capacity vs. Release Temperature')}")
        fig = px.scatter(
            subset, x="Temperature_C", y="H2_Capacity_wt%", color="Catalyst", size="Capacity_Retention_%",
            hover_data=["Pressure_bar", "Cycles", "Conversion_%"],
            labels={"Temperature_C": tt("حرارة الإطلاق (°م)", "Release Temp (°C)"), "H2_Capacity_wt%": tt("السعة الوزنية (wt%)", "Capacity (wt%)")},
            color_discrete_sequence=[PRIMARY, ACCENT, "#a8c9da", "#5a7d94"],
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"{tt('تأكدي من ملف LOHC_Complete_Dataset_With_Cycles.xlsx. الخطأ:', 'Check LOHC_Complete_Dataset_With_Cycles.xlsx exists. Error:')} {e}")

# ========================= TAB: 48-SYSTEM SCREENING =========================
with tab_screen:
    st.subheader(tt("📊 مسح المرشحين الأولي (48 نظام ناقل)", "📊 Initial Candidate Screening (48 systems)"))
    st.caption(tt("سعة وزنية محسوبة ومُتحقق منها كيميائياً من الصيغة الجزيئية.", "Gravimetric capacity chemically computed and verified from molecular formula."))

    try:
        df_screen = load_verified_dataset()
        cap_col = "H2_Capacity_wt_VERIFIED" if "H2_Capacity_wt_VERIFIED" in df_screen.columns else "H2_Capacity_wt_GIVEN"

        # Precompute priority for every row (for ranking + comparison table)
        def _row_priority(r):
            note = r.get("Notes", "")
            has_note = isinstance(note, str) and note.strip() != ""
            return compute_priority(r[cap_col], r["Retention_50_Cycles"], has_note)

        df_screen = df_screen.copy()
        df_screen["_priority"] = df_screen.apply(_row_priority, axis=1)
        _rank_order = {"high": 0, "mid": 1, "low": 2}
        df_screen["_rank"] = df_screen["_priority"].map(_rank_order)

        carrier_list = df_screen["LOHC_Name"].tolist()
        selected_carrier = st.selectbox(tt("اختر ناقل الهيدروجين العضوي:", "Select the organic hydrogen carrier:"), carrier_list)
        carrier_data = df_screen[df_screen["LOHC_Name"] == selected_carrier].iloc[0]

        note = carrier_data.get("Notes", "")
        has_note = isinstance(note, str) and note.strip() != ""
        priority = carrier_data["_priority"]

        # --- KPI cards with source-of-value badges (fix #2) ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(tt("السعة الوزنية", "Gravimetric Capacity"), f"{carrier_data[cap_col]:.2f}%")
        col1.markdown(f'<span class="hc-src-badge">{tt("محسوبة ومُتحقق منها كيميائياً", "Computed & chemically verified")}</span>', unsafe_allow_html=True)
        col2.metric(tt("حرارة الإطلاق", "Release Temp"), f"{carrier_data['Release_Temp_C']}°C")
        col2.markdown(f'<span class="hc-src-badge">{tt("بيانات مرجعية", "Reference data")}</span>', unsafe_allow_html=True)
        col3.metric(tt("الاستقرار (50 دورة)", "Stability (50 cycles)"), f"{carrier_data['Retention_50_Cycles']}%")
        col3.markdown(f'<span class="hc-src-badge">{tt("بيانات مرجعية", "Reference data")}</span>', unsafe_allow_html=True)
        col4.metric(tt("أولوية التطوير", "Development Priority"), PRIORITY_LABEL[priority][L])
        col4.markdown(f'<span class="hc-src-badge">{tt("مُشتقة من 3 معايير", "Derived from 3 criteria")}</span>', unsafe_allow_html=True)

        # --- Clear decision box (fix #1) ---
        st.markdown(f'''
        <div class="hc-decision {priority}">
          <span class="tag">🧭 {tt("قرار الفرز الأولي", "Initial Screening Decision")}</span>
          <span class="txt">{DECISION_TEXT[priority][L]}</span>
        </div>
        ''', unsafe_allow_html=True)

        # --- Structured bilingual phase-viability alert (fix #3) ---
        alert = get_phase_alert(selected_carrier)
        if alert:
            problem = alert["ar_problem"] if IS_AR else alert["en_problem"]
            result = alert["ar_result"] if IS_AR else alert["en_result"]
            st.markdown(f'''
            <div class="hc-badge-warn">
              ⚠️ <b>{tt("تنبيه: قابلية الطور السائل", "Alert: Liquid-Phase Viability")}</b><br>
              {problem}<br>{result}
            </div>
            ''', unsafe_allow_html=True)
        elif has_note:
            st.markdown(f'<div class="hc-badge-warn">⚠️ {tt("تنبيه هندسي", "Engineering note")}: {note}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="hc-badge-ok">✅ {tt("ضمن النطاق التشغيلي الآمن المتوقع", "Within expected safe operating range")}</div>', unsafe_allow_html=True)

        # --- Why this ranking (reasons breakdown) ---
        with st.expander(f"🔎 {tt('لماذا حصل هذا المرشح على هذه الأولوية؟', 'Why did this candidate get this priority?')}"):
            cap_ok = carrier_data[cap_col] >= 5.5
            ret_ok = carrier_data["Retention_50_Cycles"] >= 90
            st.write(f"- {tt('السعة الوزنية', 'Gravimetric capacity')}: "
                     f"{'✅ ' + tt('جيدة (فوق هدف DOE 5.5%)', 'Good (above DOE 5.5% target)') if cap_ok else '⚠️ ' + tt('أقل من هدف DOE', 'Below DOE target')}")
            st.write(f"- {tt('الاستقرار عبر الدورات', 'Cyclic stability')}: "
                     f"{'✅ ' + tt('مرتفع (≥90%)', 'High (≥90%)') if ret_ok else '⚠️ ' + tt('يحتاج بيانات إضافية', 'Needs more data')}")
            st.write(f"- {tt('الحالة الفيزيائية', 'Physical state')}: "
                     f"{'⚠️ ' + tt('تحتاج تحقق (انظري التنبيه أعلاه)', 'Needs verification (see alert above)') if (alert or has_note) else '✅ ' + tt('لا تنبيهات', 'No flags')}")
            st.write(f"- {tt('التوصية النهائية', 'Final recommendation')}: {DECISION_TEXT[priority][L]}")

        # --- Download buttons (candidate report) ---
        st.markdown(f"#### 📥 {tt('تحميل تقرير المرشح', 'Download Candidate Report')}")
        alert_problem_txt = (alert["ar_problem"] if IS_AR else alert["en_problem"]) if alert else ""
        alert_result_txt = (alert["ar_result"] if IS_AR else alert["en_result"]) if alert else ""
        alert_flat = f"{alert_problem_txt} {alert_result_txt}".strip() if alert else (note if has_note else "")

        dl1, dl2 = st.columns(2)
        with dl1:
            csv_bytes = build_candidate_csv(carrier_data, cap_col, priority, alert_flat)
            st.download_button(
                label=f"⬇️ {tt('تحميل CSV', 'Download CSV')}",
                data=csv_bytes,
                file_name=f"{carrier_data['LOHC_Name'].replace(' ', '_').replace('/', '-')}_report.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with dl2:
            if FPDF_AVAILABLE:
                pdf_bytes = build_candidate_pdf(carrier_data, cap_col, priority, alert_problem_txt, alert_result_txt)
                st.download_button(
                    label=f"⬇️ {tt('تحميل PDF (إنجليزي)', 'Download PDF')}",
                    data=pdf_bytes,
                    file_name=f"{carrier_data['LOHC_Name'].replace(' ', '_').replace('/', '-')}_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.caption(tt("مكتبة PDF غير مثبتة على الخادم.", "PDF library not installed on server."))

        # --- Molecular structure with hydrogenation arrow ---
        st.markdown(f"#### 🧬 {tt('التركيب الجزيئي', 'Molecular Structure')}")
        mol_img = smiles_to_image(carrier_data["SMILES"])
        if mol_img:
            st.image(mol_img, caption=f"SMILES: {carrier_data['SMILES']}", width=240)
        else:
            st.code(carrier_data["SMILES"], language=None)

        # --- Comparison table: this candidate vs average of top candidates ---
        st.markdown(f"#### 📋 {tt('مقارنة المرشح مع أفضل المرشحين', 'Candidate vs. Top Candidates Comparison')}")
        top5 = df_screen.sort_values(["_rank", cap_col], ascending=[True, False]).head(5)
        avg_cap = top5[cap_col].mean()
        avg_ret = top5["Retention_50_Cycles"].mean()
        comp_df = pd.DataFrame({
            tt("المؤشر", "Metric"): [tt("السعة الوزنية", "Capacity"), tt("الاستقرار", "Stability"), tt("أولوية التطوير", "Priority")],
            tt("المرشح الحالي", "Current Candidate"): [f"{carrier_data[cap_col]:.2f}%", f"{carrier_data['Retention_50_Cycles']}%", PRIORITY_LABEL[priority][L]],
            tt("متوسط أفضل 5 مرشحين", "Top-5 Average"): [f"{avg_cap:.2f}%", f"{avg_ret:.1f}%", "—"],
        })
        st.dataframe(comp_df, hide_index=True, use_container_width=True)
        st.caption(tt("القيم المعروضة للمقارنة تعتمد على البيانات المتاحة لكل مرشح، وقد تختلف حسب مصدر البيانات أو ظروف القياس.",
                       "Comparison values depend on available data for each candidate and may vary by data source or measurement conditions."))

        # --- Overview chart of all candidates ---
        st.markdown(f"#### {tt('مقارنة جميع المرشحين', 'All Candidates Compared')}")
        fig2 = px.scatter(
            df_screen, x="Release_Temp_C", y=cap_col, color="_priority", hover_name="LOHC_Name",
            size="Retention_50_Cycles",
            labels={"Release_Temp_C": tt("حرارة التحرير (°م)", "Release Temp (°C)"), cap_col: tt("السعة الوزنية (wt%)", "Capacity (wt%)"), "_priority": tt("الأولوية", "Priority")},
            color_discrete_map={"high": OK, "mid": WARN, "low": DANGER},
        )
        fig2.add_hline(y=5.5, line_dash="dash", line_color=DANGER, annotation_text=tt("هدف DOE: 5.5 wt%", "DOE target: 5.5 wt%"))
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"{tt('تأكدي من ملف LOHC_Dataset_Verified.xlsx. الخطأ:', 'Check LOHC_Dataset_Verified.xlsx exists. Error:')} {e}")

# ============================ TAB: QM9 EXPLORER =============================
with tab_qm9:
    st.subheader(tt("🔬 محرك الاستكشاف الجزيئي الكمي", "🔬 Quantum Molecular Exploration Engine"))
    st.markdown(tt("فرز آلاف الجزيئات استناداً إلى إنثالبي التفاعل (ΔH) وضغط التحرير (pH2).",
                    "Screening thousands of molecules by reaction enthalpy (ΔH) and release pressure (pH2)."))
    try:
        known_label = tt("الجزيئات المعروفة (QM9-LOHC)", "Known molecules (QM9-LOHC)")
        new_label = tt("المرشحون الجدد المكتشفون", "Newly discovered candidates")
        source_choice = st.radio(tt("مصدر الجزيئات:", "Molecule source:"), [known_label, new_label], horizontal=True)
        df_qm9 = load_qm9_known() if source_choice == known_label else load_qm9_candidates()

        st.sidebar.markdown("---")
        st.sidebar.subheader(tt("🔎 معايير الترشيح", "🔎 Filter Criteria"))
        dh_min, dh_max = float(df_qm9["delta_H"].min()), float(df_qm9["delta_H"].max())
        sel_dh = st.sidebar.slider(tt("نطاق ΔH (kJ/mol H₂):", "ΔH range (kJ/mol H₂):"), dh_min, dh_max, (40.0, 75.0))
        ph2_min, ph2_max = float(df_qm9["pH2"].min()), float(df_qm9["pH2"].max())
        sel_ph2 = st.sidebar.slider(tt("نطاق pH2 (bar):", "pH2 range (bar):"), ph2_min, ph2_max, (ph2_min, ph2_max))
        num_display = st.sidebar.number_input(tt("العدد الأقصى للعرض:", "Max to display:"), min_value=1, max_value=20, value=6)

        filtered = df_qm9[df_qm9["delta_H"].between(sel_dh[0], sel_dh[1]) & df_qm9["pH2"].between(sel_ph2[0], sel_ph2[1])]
        st.info(f"{tt('تم العثور على', 'Found')} **{len(filtered):,}** {tt('جزيء (من أصل', 'molecule(s) (out of')} {len(df_qm9):,}).")

        fig3 = px.scatter(
            filtered.sample(min(2000, len(filtered))) if len(filtered) > 0 else filtered,
            x="delta_H", y="pH2", opacity=0.5, color_discrete_sequence=[ACCENT],
            labels={"delta_H": "ΔH (kJ/mol H₂)", "pH2": "pH2 (bar)"},
        )
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=350)
        st.plotly_chart(fig3, use_container_width=True)

        if len(filtered) > 0:
            for idx, row in filtered.head(int(num_display)).iterrows():
                with st.container():
                    col_data, col_img1, col_img2 = st.columns([2, 1, 1])
                    with col_data:
                        st.markdown(f"**{tt('مركب', 'Compound')} #{idx}**")
                        st.write(f"ΔH: {row['delta_H']:.2f} kJ/mol H₂")
                        st.write(f"pH2: {row['pH2']:.2f} bar")
                        if "molar_mass" in row and pd.notnull(row["molar_mass"]):
                            st.write(f"{tt('الوزن الجزيئي', 'Molecular weight')}: {row['molar_mass']:.2f} g/mol")
                        st.write(f"nH₂: {row['nH2']}")
                    with col_img1:
                        img_u = smiles_to_image(row["unsat_SMILE"])
                        st.image(img_u, caption=tt("غير مهدرج", "Unsaturated"), width=170) if img_u else st.code(row["unsat_SMILE"], language=None)
                    with col_img2:
                        img_s = smiles_to_image(row["sat_SMILE"])
                        st.image(img_s, caption=tt("مهدرج", "Hydrogenated"), width=170) if img_s else st.code(row["sat_SMILE"], language=None)
                st.markdown("---")
    except Exception as e:
        st.error(f"{tt('تأكدي من وجود ملفات QM9. الخطأ:', 'Check QM9 files exist. Error:')} {e}")

# ============================== TAB: ABOUT ==================================
with tab_about:
    st.subheader(tt("ℹ️ عن المنصة والمنهجية", "ℹ️ About the Platform & Methodology"))
    st.markdown(f'''
    <div class="hc-card"><b>{tt("المعمارية", "Architecture")}:</b> {tt(
        "طبقتان منفصلتان عمداً — محرك علمي حتمي يحسب كل الأرقام من بيانات QM9-LOHC/G4MP2 الحقيقية دون أي تدخل من نموذج لغوي، وطبقة تقرير تشغيلي عربي تقرأ فقط مخرجات الطبقة الأولى.",
        "Two deliberately separated layers — a deterministic scientific engine computing every number from real QM9-LOHC/G4MP2 data with no language-model involvement, and an Arabic reporting layer that only reads Layer 1's outputs."
    )}</div>
    <div class="hc-card"><b>{tt("لماذا هذا التمايز", "Why this differentiation")}:</b> {tt(
        "الفرز الحاسوبي النظري للسعة والإنثالبي مجال مُشبع أكاديمياً. تركّز هذه المنصة على الفجوة غير المطروقة: حركية النزع الحفزية العملية والاستقرار الدوري الحقيقي.",
        "Theoretical computational screening for capacity and enthalpy is an academically saturated field. This platform focuses on the untapped gap: practical catalytic release kinetics and real cyclic stability."
    )}</div>
    <div class="hc-card"><b>{tt("هاكاثون الطاقة 2026", "Energy Hackathon 2026")}</b> — {tt("مسار الرؤية الابتكارية", "Innovative Vision Track")}</div>
    ''', unsafe_allow_html=True)

st.markdown("---")
st.caption(tt("HydroCarrier AI © 2026 — تقديم هاكاثون الطاقة", "HydroCarrier AI © 2026 — Energy Hackathon Submission"))
