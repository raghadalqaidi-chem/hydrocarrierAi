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
import plotly.graph_objects as go

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    RDKIT_AVAILABLE = True
except Exception:
    RDKIT_AVAILABLE = False

# ---------------------------------------------------------------------------
# Page config & brand identity
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

PRIMARY = "#3a566e"      # dark navy (from the HydroCarrier AI logo)
ACCENT = "#71aeca"       # light blue (from the logo's water motif)
ACCENT_LIGHT = "#eaf3f8"
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
# Global CSS — brand colors + RTL Arabic layout
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        direction: rtl;
        font-family: 'Tahoma', 'Segoe UI', sans-serif;
    }}
    .block-container {{
        padding-top: 1.2rem;
    }}
    h1, h2, h3, h4 {{
        color: {PRIMARY};
        font-weight: 800;
    }}
    .hc-header {{
        background: linear-gradient(90deg, {PRIMARY} 0%, {ACCENT} 100%);
        padding: 18px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .hc-header h1 {{
        color: white !important;
        margin: 0;
        font-size: 26px;
    }}
    .hc-header p {{
        color: #eaf3f8;
        margin: 2px 0 0 0;
        font-size: 14px;
    }}
    .hc-card {{
        background: white;
        border: 1px solid #e2e8ee;
        border-left: 5px solid {ACCENT};
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .hc-badge-ok {{
        background: #e8f5e9; color: {OK}; padding: 3px 10px; border-radius: 20px;
        font-size: 12px; font-weight: 700; display: inline-block;
    }}
    .hc-badge-warn {{
        background: #fff8e1; color: {WARN}; padding: 3px 10px; border-radius: 20px;
        font-size: 12px; font-weight: 700; display: inline-block;
    }}
    .hc-badge-source {{
        background: {ACCENT_LIGHT}; color: {PRIMARY}; padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600; display: inline-block; margin-left: 6px;
    }}
    div[data-testid="stMetric"] {{
        background: {ACCENT_LIGHT};
        border-radius: 12px;
        padding: 10px 6px;
        border: 1px solid #d7e7ef;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {ACCENT_LIGHT};
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 700;
        color: {PRIMARY};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PRIMARY} !important;
        color: white !important;
    }}
    .hc-logo-slot {{
        background: white;
        border-radius: 10px;
        padding: 6px 10px;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header — HydroCarrier logo only (transparent background)
# ---------------------------------------------------------------------------
logo_h_path = os.path.join(ASSETS_DIR, "hydrocarrier_logo_horizontal.png")
logo_sq_path = os.path.join(ASSETS_DIR, "hydrocarrier_logo.jpeg")
if os.path.exists(logo_h_path):
    st.image(logo_h_path, width=420)
elif os.path.exists(logo_sq_path):
    st.image(logo_sq_path, width=110)
st.markdown(f"""
<p style="color:{PRIMARY}; font-size:14px; margin-top:-6px;">
    منصة التنبؤ بحركية الإطلاق الحفزية واستقرار الدورات لناقلات الهيدروجين العضوية السائلة (LOHC)
</p>
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
    path = os.path.join(DATA_DIR, "LOHC_Dataset_Verified.xlsx")
    return pd.read_excel(path, sheet_name="LOHC_Dataset_Verified")


@st.cache_data
def load_experimental_dataset():
    path = os.path.join(DATA_DIR, "LOHC_Complete_Dataset_With_Cycles.xlsx")
    return pd.read_excel(path)


@st.cache_data
def load_qm9_known():
    path = os.path.join(DATA_DIR, "QM9_G4MP2_all.csv")
    return pd.read_csv(path)


@st.cache_data
def load_qm9_candidates():
    path = os.path.join(DATA_DIR, "QM9-LOHC_new_molecules.csv")
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_exp, tab_screen, tab_qm9, tab_about = st.tabs([
    "🏠 نظرة عامة",
    "🧪 القاعدة التجريبية الموثقة",
    "📊 مسح المرشحين (48 نظام)",
    "🔬 الاستكشاف الكمي (QM9)",
    "ℹ️ عن المنصة",
])

# ============================= TAB: OVERVIEW ===============================
with tab_overview:
    try:
        df_exp_preview = load_experimental_dataset()
        df_screen_preview = load_verified_dataset()
        df_qm9_preview = load_qm9_known()
        df_cand_preview = load_qm9_candidates()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("أنظمة تجريبية موثّقة بمصادر منشورة", f"{df_exp_preview['LOHC_Pair'].nunique()}")
        c2.metric("مرشحون مُفحوصون (فرز أولي)", f"{len(df_screen_preview)}")
        c3.metric("جزيئات محسوبة كمياً (QM9)", f"{len(df_qm9_preview):,}")
        c4.metric("مرشحون جدد مكتشفون", f"{len(df_cand_preview):,}")
    except Exception as e:
        st.warning(f"تعذر تحميل بعض ملفات البيانات للمعاينة السريعة: {e}")

    st.markdown("### 💡 فكرة المشروع")
    st.markdown(f"""
    <div class="hc-card">
    تعتمد طرق تخزين الهيدروجين الحالية إما على <b>الضغط العالي (700 بار)</b> بتكلفة ومخاطر أمان كبيرة،
    أو <b>التسييل المبرّد (-253°م)</b> عالي استهلاك الطاقة ومع فقدان مستمر بالتبخر. تقدّم
    <b>ناقلات الهيدروجين العضوية السائلة (LOHC)</b> حلاً كيميائياً مباشراً: تخزين الهيدروجين في سائل
    يبقى عند درجة حرارة وضغط الغرفة، يُنقل كالوقود التقليدي، ويُطلق الهيدروجين عند الحاجة عبر حفاز.
    <br><br>
    <b>هايدروكارير الذكي</b> يتنبأ بثلاثة أشياء لا تغطيها أدوات الفرز الأكاديمية الحالية بشكل كافٍ:
    <b>السعة الوزنية</b>، و<b>حركية الإطلاق الحفزية العملية</b> تحت حفاز حقيقي، و<b>الاستقرار عبر دورات الشحن والتفريغ</b>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🗂️ مصادر البيانات في هذه المنصة")
    st.markdown(f"""
    <div class="hc-card">
    <b>1. القاعدة التجريبية الموثقة</b> — أنظمة حقيقية موثقة من أدبيات منشورة فعلياً (PubMed، MDPI Energies 2025،
    Springer 2025، RSC 2025/2026)، تشمل نوع الحفاز، الحرارة، الضغط، معدل التفاعل، والاستقرار عبر الدورات.<br>
    <b>2. مسح المرشحين الأولي</b> — 48 نظام ناقل مرشح مع سعة وزنية محسوبة كيميائياً ومُتحقق منها.<br>
    <b>3. الاستكشاف الكمي QM9</b> — أكثر من 10,000 تفاعل نزع هيدروجين محسوب كمياً (G4MP2) من قاعدة بيانات QM9-LOHC المنشورة،
    بالإضافة لمرشحين جدد مكتشفين عبر الفرز الحاسوبي.
    </div>
    """, unsafe_allow_html=True)

# ===================== TAB: EXPERIMENTAL (REAL, CITED) =====================
with tab_exp:
    st.subheader("🧪 الأنظمة التجريبية الموثقة بمصادر أدبية منشورة")
    st.caption("كل صف في هذا الجدول مرتبط بمصدر علمي منشور فعلياً — انظري عمودي المصدر أسفل كل بطاقة.")

    try:
        df_exp = load_experimental_dataset()
        pairs = sorted(df_exp["LOHC_Pair"].unique())
        selected_pair = st.selectbox("اختر نظام الناقل (LOHC Pair):", pairs)
        subset = df_exp[df_exp["LOHC_Pair"] == selected_pair].reset_index(drop=True)

        st.markdown(f"#### النتائج التجريبية المسجلة لـ **{selected_pair}** ({len(subset)} تجربة/شرط تشغيلي)")

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
                    k1.metric("السعة الوزنية", f"{row['H2_Capacity_wt%']:.2f}%")
                    k2.metric("درجة حرارة الإطلاق", f"{row['Temperature_C']:.0f}°م")
                    k3.metric("نسبة التحول", f"{row['Conversion_%']:.1f}%")
                    k4.metric("الاحتفاظ بالسعة", f"{row['Capacity_Retention_%']:.1f}%", f"عبر {int(row['Cycles'])} دورة")

                    st.markdown(
                        f"**الحفاز:** {row['Catalyst']} (تحميل {row['Catalyst_Loading_wt%']}٪) &nbsp;|&nbsp; "
                        f"**الضغط:** {row['Pressure_bar']} بار &nbsp;|&nbsp; "
                        f"**إنثالبي النزع:** {row['Enthalpy_kJmol_H2']} kJ/mol H2 &nbsp;|&nbsp; "
                        f"**الحالة الفيزيائية:** {row['State']}"
                    )
                    st.markdown(
                        f'<span class="hc-badge-source">📚 بيانات الحفاز: {row["Data_Source_Catalyst"]}</span>'
                        f'<span class="hc-badge-source">📚 بيانات الخواص: {row["Data_Source_Properties"]}</span>',
                        unsafe_allow_html=True,
                    )
            st.markdown("---")

        st.markdown("#### 📈 مقارنة الحفازات لهذا النظام: السعة مقابل حرارة الإطلاق")
        fig = px.scatter(
            subset, x="Temperature_C", y="H2_Capacity_wt%",
            color="Catalyst", size="Capacity_Retention_%",
            hover_data=["Pressure_bar", "Cycles", "Conversion_%"],
            labels={"Temperature_C": "درجة حرارة الإطلاق (°م)", "H2_Capacity_wt%": "السعة الوزنية (wt%)"},
            color_discrete_sequence=[PRIMARY, ACCENT, "#a8c9da", "#5a7d94"],
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"تأكدي من وجود ملف 'LOHC_Complete_Dataset_With_Cycles.xlsx' داخل مجلد data/. الخطأ: {e}")

# ========================= TAB: 48-SYSTEM SCREENING =========================
with tab_screen:
    st.subheader("📊 مسح المرشحين الأولي (48 نظام ناقل)")
    st.caption("سعة وزنية محسوبة ومُتحقق منها كيميائياً من الصيغة الجزيئية؛ راجعي عمود الملاحظات للتنبيهات الهندسية.")

    try:
        df_screen = load_verified_dataset()
        carrier_list = df_screen["LOHC_Name"].tolist()
        selected_carrier = st.selectbox("اختر الناقل العضوي للهيدروجين:", carrier_list)
        carrier_data = df_screen[df_screen["LOHC_Name"] == selected_carrier].iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        cap_col = "H2_Capacity_wt_VERIFIED" if "H2_Capacity_wt_VERIFIED" in df_screen.columns else "H2_Capacity_wt_GIVEN"
        col1.metric("السعة الوزنية (مُتحقق منها)", f"{carrier_data[cap_col]:.2f}%")
        col2.metric("حرارة التحرير المطلوبة", f"{carrier_data['Release_Temp_C']}°م")
        col3.metric("معدل الاستقرار (50 دورة)", f"{carrier_data['Retention_50_Cycles']}%")
        col4.metric("نظام الحفاز", f"{carrier_data['Catalyst_Metal']} / {carrier_data['Support_Material']}")

        note = carrier_data.get("Notes", "")
        if isinstance(note, str) and note.strip():
            st.markdown(f'<div class="hc-badge-warn">⚠️ تنبيه هندسي: {note}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hc-badge-ok">✅ ضمن النطاق التشغيلي الآمن المتوقع</div>', unsafe_allow_html=True)

        st.markdown("#### التركيب الجزيئي")
        mol_img = smiles_to_image(carrier_data["SMILES"])
        if mol_img:
            st.image(mol_img, caption=f"SMILES: {carrier_data['SMILES']}", width=240)
        else:
            st.code(carrier_data["SMILES"], language=None)

        st.markdown("#### مقارنة جميع المرشحين: السعة الوزنية مقابل حرارة التحرير")
        fig2 = px.scatter(
            df_screen, x="Release_Temp_C", y=cap_col,
            color="Catalyst_Metal", hover_name="LOHC_Name",
            size="Retention_50_Cycles",
            labels={"Release_Temp_C": "حرارة التحرير (°م)", cap_col: "السعة الوزنية (wt%)"},
            color_discrete_sequence=[PRIMARY, ACCENT, "#a8c9da", "#5a7d94", "#2e4a5e"],
        )
        fig2.add_hline(y=5.5, line_dash="dash", line_color=DANGER,
                        annotation_text="هدف وزارة الطاقة الأمريكية (DOE): 5.5 wt%")
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"تأكدي من وجود ملف 'LOHC_Dataset_Verified.xlsx' داخل مجلد data/. الخطأ: {e}")

# ============================ TAB: QM9 EXPLORER =============================
with tab_qm9:
    st.subheader("🔬 محرك الاستكشاف الجزيئي الكمي (QM9 High-Throughput Screening)")
    st.markdown("فرز آلاف الجزيئات استناداً إلى إنثالبي التفاعل (ΔH) وضغط التحرير (pH2).")

    try:
        source_choice = st.radio(
            "مصدر الجزيئات:",
            ["الجزيئات المعروفة (QM9-LOHC، +10,000 تفاعل)", "المرشحون الجدد المكتشفون حديثاً"],
            horizontal=True,
        )
        df_qm9 = load_qm9_known() if source_choice.startswith("الجزيئات المعروفة") else load_qm9_candidates()

        st.sidebar.markdown("---")
        st.sidebar.subheader("🔎 معايير الترشيح")
        delta_h_min, delta_h_max = float(df_qm9["delta_H"].min()), float(df_qm9["delta_H"].max())
        sel_delta_h = st.sidebar.slider("نطاق طاقة التفاعل ΔH (kJ/mol H₂):", delta_h_min, delta_h_max, (40.0, 75.0))

        ph2_min, ph2_max = float(df_qm9["pH2"].min()), float(df_qm9["pH2"].max())
        sel_ph2 = st.sidebar.slider("نطاق ضغط الهيدروجين pH2 (bar):", ph2_min, ph2_max, (ph2_min, ph2_max))

        num_display = st.sidebar.number_input("العدد الأقصى للجزيئات المعروضة:", min_value=1, max_value=20, value=6)

        filtered = df_qm9[
            df_qm9["delta_H"].between(sel_delta_h[0], sel_delta_h[1]) &
            df_qm9["pH2"].between(sel_ph2[0], sel_ph2[1])
        ]

        st.info(f"تم العثور على **{len(filtered):,}** جزيء يطابق معايير الطاقة المدخلة "
                f"(من أصل {len(df_qm9):,}).")

        st.markdown("#### توزيع إنثالبي التفاعل مقابل ضغط الهيدروجين")
        fig3 = px.scatter(
            filtered.sample(min(2000, len(filtered))) if len(filtered) > 0 else filtered,
            x="delta_H", y="pH2", opacity=0.5,
            color_discrete_sequence=[ACCENT],
            labels={"delta_H": "ΔH (kJ/mol H₂)", "pH2": "pH2 (bar)"},
        )
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=350)
        st.plotly_chart(fig3, use_container_width=True)

        if len(filtered) > 0:
            sample_df = filtered.head(int(num_display))
            st.markdown("#### عيّنة من الجزيئات المطابقة")
            for idx, row in sample_df.iterrows():
                with st.container():
                    col_data, col_img1, col_img2 = st.columns([2, 1, 1])
                    with col_data:
                        st.markdown(f"**مركب #{idx}**")
                        st.write(f"**طاقة التفاعل (ΔH):** {row['delta_H']:.2f} kJ/mol H₂")
                        st.write(f"**ضغط الهيدروجين (pH2):** {row['pH2']:.2f} bar")
                        if "molar_mass" in row and pd.notnull(row["molar_mass"]):
                            st.write(f"**الوزن الجزيئي:** {row['molar_mass']:.2f} g/mol")
                        st.write(f"**عدد جزيئات H₂:** {row['nH2']}")
                    with col_img1:
                        img_unsat = smiles_to_image(row["unsat_SMILE"])
                        if img_unsat:
                            st.image(img_unsat, caption="الطور المفرّغ", width=170)
                        else:
                            st.code(row["unsat_SMILE"], language=None)
                    with col_img2:
                        img_sat = smiles_to_image(row["sat_SMILE"])
                        if img_sat:
                            st.image(img_sat, caption="الطور المشبع", width=170)
                        else:
                            st.code(row["sat_SMILE"], language=None)
                st.markdown("---")

    except Exception as e:
        st.error(f"تأكدي من وجود ملفات QM9 داخل مجلد data/. الخطأ: {e}")

# ============================== TAB: ABOUT ==================================
with tab_about:
    st.subheader("ℹ️ عن المنصة والمنهجية")
    st.markdown(f"""
    <div class="hc-card">
    <b>المعمارية:</b> طبقتان منفصلتان عمداً —
    <br>1) <b>محرك علمي حتمي</b>: جميع الأرقام (السعة، الإنثالبي، الحركية، الاستقرار) تُحسب من بيانات
    QM9-LOHC/G4MP2 الحقيقية وخصائف RDKit الجزيئية، دون أي تدخل من نموذج لغوي.
    <br>2) <b>طبقة تقرير تشغيلي</b> باللغة العربية مبنية على ALLAM (من هيومين HUMAIN)، تقرأ فقط مخرجات الطبقة
    الأولى وتترجمها لتقرير ميداني للمهندس.
    </div>
    <div class="hc-card">
    <b>لماذا هذا التمايز:</b> الفرز الحاسوبي النظري للسعة والإنثالبي مجال مُشبع أكاديمياً (قاعدة QM9-LOHC
    ونماذجها المرتبطة). تركّز هذه المنصة على الفجوة غير المطروقة: حركية النزع الحفزية العملية، والاستقرار
    الدوري الحقيقي — كما يظهر في تبويب "القاعدة التجريبية الموثقة".
    </div>
    <div class="hc-card">
    <b>هاكاثون الطاقة 2026</b> — مسار الرؤية الابتكارية — تحدي تخزين الهيدروجين بكفاءة أعلى ومرونة أكبر.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("HydroCarrier AI © 2026 — Energy Hackathon Submission")
