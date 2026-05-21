# dpdp-law-to-code

**بھارت کا ڈیجیٹل ذاتی ڈیٹا تحفظ ایکٹ، 2023 — قابلِ اجراء Python کوڈ کے طور پر۔ MIT · ₹0 · مقامی-اول۔**

بھارت سرکار نے جس فریم ورک کی عوامی تحقیق کا آغاز کیا ہے، یہ اس کا ایک شہری-تعمیر کردہ حوالہ نفاذ ہے۔

**پڑھیں:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *کمیونٹی ترجمہ۔ انگریزی [README](../README.md) مستند نسخہ ہے۔ ایکٹ کی متعین تکنیکی اصطلاحات (Data Fiduciary, Data Principal، وغیرہ) DPDP Act 2023 کے اصل متن سے تصدیق کے لیے انگریزی ہی میں رکھی گئی ہیں۔*

---

## یہ کیوں موجود ہے — MeitY کا اشارہ

20 مئی 2026 کو، *Economic Times* نے رپورٹ کیا کہ **وزارتِ الیکٹرانکس و انفارمیشن ٹیکنالوجی (Ministry of Electronics and IT — MeitY)** ایک تصور — **"Law-to-Code"** — یعنی DPDP Act 2023 کے قواعد کو مشین-قابل اجراء الگوردمز میں ترجمہ کرنا — پر صنعت کے فریقین سے وسیع مشاورت کر رہی ہے۔

ہیمانشی لوہچب اور سبھایان چکروَرتی کا مضمون *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times، 20 مئی 2026) بتاتا ہے کہ یہ مشاورت تقریباً ایک ماہ سے جاری ہے اور جدید AI ماڈلز کی تیز پیش رفت کے سامنے MeitY کے وسیع جواب کا حصہ ہے۔

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**یہ ریپوزٹری حکومت نے عوام کے سامنے رکھے گئے سوال کا ایک شہری کا جواب ہے۔** یہ کوئی مقابلہ پسند تجویز نہیں، تنقید بھی نہیں — ایک کام کرنے والا، اوپن-سورس حوالہ نفاذ۔ اگر MeitY رسمی فریم ورک شائع کرتا ہے، تو یہ ریپوزٹری اسی کے مطابق اپ ڈیٹ کی جائے گی۔

---

## یہ کیا ہے

DPDP Act 2023 (دفعات 5–16) — `pip install` کے قابل Python لائبریری۔ ہر check شرعی حوالے کے ساتھ `ComplianceResult` واپس کرتا ہے۔

---

## انسٹال

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10۔ کوئی runtime dependencies نہیں۔

---

## استعمال کیسے کریں — تین راستے

### راستہ A — اپنے Python codebase میں (ڈویلپرز)
`from dpdp.consent import check_consent` — request handler یا CI pipeline میں۔

### راستہ B — ٹرمینل سے (تعمیلی افسران)
```bash
dpdp-check --section 6 --input consent.json
```

### راستہ C — AI معاون کے ذریعے (وکلاء، بانیان)

Claude / Cursor / ChatGPT / Gemini کو کہیں — وہ خود لائبریری install کر کے check کر دے گا۔

**⚠ ضروری ڈیٹا-ہینڈلنگ نوٹس:**

DPDP Act 2023، **دفعہ 8(5)** کے مطابق ہر Data Fiduciary پر "معقول حفاظتی اقدامات" لازم ہیں۔ مفت AI chatbot میں اصل ذاتی ڈیٹا paste کرنا خود ایک خلاف ورزی ہو سکتی ہے۔

**اصل پیداواری ڈیٹا AI کو دینے سے پہلے دو شرائط:**

1. **صرف ادا شدہ / تجارتی API tier — Data Processing Agreement (DPA) کے ساتھ:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (سب ادا شدہ)۔
2. **"Training-on-input" بند ہے، یقینی بنائیں۔** مفت ChatGPT / Gemini / Claude.ai صارف-سطح اصل Data Principal معلومات کے لیے غیر موزوں۔

سیکھنے / تجربے / فرضی مثالوں کے لیے — کوئی بھی tier ٹھیک ہے۔ **اصل ڈیٹا** — ادا شدہ API + DPA، کوئی استثنا نہیں۔

---

## v0.1 میں شامل دفعات

| دفعہ | ماڈیول | موضوع |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal کو نوٹس |
| Sec 6 | `dpdp.consent` | F-S-I-U-U رضامندی |
| Sec 7 | `dpdp.legitimate` | 9 جائز استعمال |
| Sec 8 | `dpdp.fiduciary` | Fiduciary فرض · خلاف ورزی · حذف |
| Sec 9 | `dpdp.children` | تصدیق پذیر والدین کی رضامندی |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal کے حقوق |
| Sec 15 | `dpdp.duties` | Data Principal کے فرائض |
| Sec 16 | `dpdp.cross_border` | سرحد-پار منتقلی |

407 ٹیسٹ پاس۔

---

## قانونی دستبرداری

یہ سافٹ ویئر **قانونی مشورہ نہیں ہے۔** اہل وکیل کا متبادل نہیں۔ Bar Council of India Rule 36 کے تحت — یہ مفت، اوپن-سورس، MIT-لائسنس یافتہ شراکت ہے۔ گاہک جمع کرنا نہیں، قانونی خدمات کی تشہیر نہیں، وکیل-گاہک تعلق قائم نہیں کرتا۔

## لائسنس

MIT۔ مکمل تفصیل کے لیے [English README](../README.md) دیکھیں۔

## شراکت

اس ترجمے کو بہتر کرنے کے لیے PR کا خیر مقدم ہے۔
