# ⚡ HydroCarrier AI | هايدروكارير الذكي

**Energy Hackathon 2026 — Innovative Vision Track**
منصة استكشاف وتقييم نواقل الهيدروجين العضوية السائلة (LOHC)

---

## 🇸🇦 نظرة عامة

منصة تفاعلية (Streamlit) لاستكشاف وتقييم أنظمة **ناقلات الهيدروجين العضوية السائلة (LOHC)**،
تجمع بين:

1. **قاعدة بيانات تجريبية موثقة** — 16 تجربة حقيقية من أدبيات منشورة (PubMed، MDPI Energies 2025،
   Springer 2025، RSC 2025/2026) تشمل نوع الحفاز، الحرارة، الضغط، معدل التفاعل، والاستقرار عبر الدورات.
2. **مسح أولي لـ 48 نظام ناقل مرشح** — سعة وزنية محسوبة ومُتحقق منها كيميائياً من الصيغة الجزيئية.
3. **محرك استكشاف كمي (QM9-LOHC)** — أكثر من 10,000 تفاعل نزع هيدروجين محسوب كمياً (G4MP2)، بالإضافة
   إلى ما يقارب 9,800 مرشح جديد مكتشف عبر الفرز الحاسوبي.

### 🚀 التشغيل محلياً

```bash
# 1. إنشاء بيئة افتراضية (اختياري لكن يُنصح به)
python3 -m venv venv
source venv/bin/activate      # على ويندوز: venv\Scripts\activate

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تشغيل التطبيق
streamlit run app.py
```

سيفتح المتصفح تلقائياً على `http://localhost:8501`.

### 📁 هيكل المشروع

```
hydrocarrier-ai/
├── app.py                          # التطبيق الرئيسي
├── requirements.txt
├── .streamlit/config.toml          # ألوان الهوية البصرية
├── assets/
│   ├── hydrocarrier_logo_horizontal.png   # الشعار الأفقي (خلفية شفافة، يُستخدم في رأس التطبيق)
│   └── hydrocarrier_logo.jpeg             # الشعار المربع (احتياطي)
└── data/
    ├── LOHC_Complete_Dataset_With_Cycles.xlsx   # القاعدة التجريبية الموثقة
    ├── LOHC_Dataset_Verified.xlsx               # مسح 48 نظام
    ├── QM9_G4MP2_all.csv                        # قاعدة QM9-LOHC (10,373 تفاعل)
    └── QM9-LOHC_new_molecules.csv                # مرشحون جدد
```

### 📤 رفع المشروع إلى GitHub

```bash
cd hydrocarrier-ai
git init
git add .
git commit -m "Initial commit: HydroCarrier AI platform"
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

> إذا كانت ملفات `data/QM9_G4MP2_all.csv` أو `QM9-LOHC_new_molecules.csv` كبيرة نسبياً (حوالي 0.5-0.9
> ميجابايت لكل منهما)، فهي ضمن الحد المسموح لرفع الملفات العادي في GitHub (الحد 100 ميجابايت للملف)
> ولا تحتاجين Git LFS.

### 🏗️ المعمارية العلمية

طبقتان منفصلتان عمداً لتفادي أي مخاطرة "هلوسة" في الأرقام العلمية:

1. **محرك علمي حتمي** — كل الأرقام (السعة، الإنثالبي، الحركية، الاستقرار) تُحسب من بيانات
   QM9-LOHC/G4MP2 الحقيقية وخصائف RDKit، بلا أي تدخل من نموذج لغوي توليدي.
2. **طبقة تقرير تشغيلي عربي** (مخطط لها) مبنية على ALLAM من هيومين (HUMAIN) — تقرأ فقط مخرجات
   الطبقة الأولى وتترجمها لتقرير ميداني، دون التأثير على الحسابات نفسها.

---

## 🇬🇧 Overview (English)

An interactive Streamlit platform for screening and evaluating **Liquid Organic Hydrogen Carrier
(LOHC)** systems, combining a literature-cited experimental dataset (16 real, sourced experiments),
a 48-system verified screening set, and a QM9-LOHC-based high-throughput exploration engine
(10,373 known reactions + ~9,800 newly discovered candidates).

Run locally with `pip install -r requirements.txt && streamlit run app.py`. See the Arabic section
above for the full project structure and GitHub push instructions (identical steps apply in English).

The header displays the HydroCarrier AI logo (transparent background) only.

**Data sources:** PubMed, MDPI Energies (2025), Springer (2025), RSC (2025/2026), and the QM9-LOHC
dataset (Nature Scientific Data, 2025).

---

**Energy Hackathon 2026 — Innovative Vision Track**
