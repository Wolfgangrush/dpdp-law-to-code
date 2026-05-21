# dpdp-law-to-code

**இந்தியாவின் டிஜிட்டல் தனிநபர் தரவுப் பாதுகாப்புச் சட்டம், 2023 — இயக்கக்கூடிய Python குறியீடாக. MIT · ₹0 · உள்ளூர்-முதலாவது.**

இந்திய அரசு பொதுவில் ஆராயத் தொடங்கியுள்ள கட்டமைப்பின் ஒரு குடிமக்கள் கட்டிய குறிப்பு செயலாக்கம்.

**படிக்கவும்:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *சமூக மொழிபெயர்ப்பு. ஆங்கில [README](../README.md) அதிகாரப்பூர்வப் பதிப்பு. சட்டத்தில் வரையறுக்கப்பட்ட தொழில்நுட்பச் சொற்கள் (Data Fiduciary, Data Principal, முதலியன) DPDP Act 2023 மூலப் பாடத்துடன் சரிபார்க்க ஆங்கிலத்திலேயே வைக்கப்பட்டுள்ளன.*

---

## ஏன் இது உள்ளது — MeitY-யின் சமிக்ஞை

20 மே 2026 அன்று, *Economic Times* அறிக்கையின்படி, **மின்னணு மற்றும் தகவல் தொழில்நுட்ப அமைச்சகம் (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** என்று அழைக்கப்படும் ஒரு கருத்தாக்கம் — DPDP Act 2023-ன் விதிமுறைகளை இயந்திர-செயல்படுத்தத்தக்க அல்காரிதங்களாக மொழிபெயர்ப்பது — பற்றி தொழில்துறை பங்குதாரர்களுடன் விரிவான ஆலோசனைகளை நடத்தி வருகிறது.

ஹிமாஞ்சி லோஹ்சாப் மற்றும் சுபாயன் சக்ரவர்த்தி எழுதிய *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 மே 2026) கட்டுரையின்படி, இந்த ஆலோசனைகள் கடந்த ஒரு மாதமாக நடந்து வருகின்றன மற்றும் அதிநவீன AI மாதிரிகளின் வேகமான முன்னேற்றத்திற்கு MeitY-யின் பரந்த பதிலின் ஒரு பகுதியாகும்.

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**இந்த ரெபோசிட்டரி அரசு பொதுவில் வைத்த கேள்விக்கு ஒரு குடிமகனின் பதில்.** இது போட்டி முன்மொழிவு அல்ல, விமர்சனமும் அல்ல — ஒரு செயல்படும், திறந்த-மூல குறிப்பு செயலாக்கம். MeitY முறையான கட்டமைப்பை வெளியிட்டால், இந்த ரெபோசிட்டரி அதற்கேற்ப புதுப்பிக்கப்படும்.

---

## இது என்ன

DPDP Act 2023 (பிரிவுகள் 5–16) — `pip install` செய்யக்கூடிய Python நூலகம். ஒவ்வொரு சரிபார்ப்பும் `ComplianceResult` திருப்பித் தருகிறது, சட்டத்தின் மேற்கோளுடன்.

---

## நிறுவல்

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. runtime சார்புகள் இல்லை.

---

## எப்படிப் பயன்படுத்துவது — மூன்று வழிகள்

### வழி A — உங்கள் Python codebase-இல் (டெவலப்பர்கள்)
`from dpdp.consent import check_consent` — உங்கள் request handler அல்லது CI pipeline-இல் பயன்படுத்தவும்.

### வழி B — டெர்மினலில் இருந்து (இணக்க அதிகாரிகள்)
```bash
dpdp-check --section 6 --input consent.json
```

### வழி C — AI உதவியாளர் வழியாக (வழக்கறிஞர்கள், நிறுவனர்கள்)

Claude / Cursor / ChatGPT / Gemini-யிடம் கேளுங்கள் — அது தானே நூலகத்தை நிறுவி சரிபார்க்கும்.

**⚠ அவசிய தரவு-கையாள்தல் அறிவிப்பு:**

DPDP Act 2023, **பிரிவு 8(5)** ஒவ்வொரு Data Fiduciary-க்கும் "நியாயமான பாதுகாப்பு நடவடிக்கைகள்" தேவை. இலவச AI chatbot-இல் உண்மையான தனிப்பட்ட தரவு ஒட்டுவது தானே ஒரு மீறலாக இருக்கலாம்.

**உண்மையான தயாரிப்புத் தரவை AI-க்கு வழங்கும் முன் இரண்டு நிபந்தனைகள்:**

1. **பணம் செலுத்தும் / வணிக API tier மட்டுமே — Data Processing Agreement (DPA) கொண்டது:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (அனைத்தும் கட்டண பதிப்பு).
2. **"Training-on-input" அணைக்கப்பட்டிருப்பதை உறுதிசெய்யவும்.** இலவச ChatGPT / Gemini / Claude.ai நுகர்வோர் நிலை உண்மையான Data Principal தகவலுக்கு பொருத்தமற்றது.

கற்றல் / ஆய்வு / கற்பனை உதாரணங்களுக்கு — எந்த tier-ஐயும் பயன்படுத்தலாம். **உண்மையான தரவு** — கட்டண API + DPA, விதிவிலக்குகள் இல்லை.

---

## v0.1-இல் சேர்க்கப்பட்ட பிரிவுகள்

| பிரிவு | தொகுதி | தலைப்பு |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal-க்கு அறிவிப்பு |
| Sec 6 | `dpdp.consent` | F-S-I-U-U சம்மதம் |
| Sec 7 | `dpdp.legitimate` | 9 முறையான பயன்கள் |
| Sec 8 | `dpdp.fiduciary` | Fiduciary கடமை · மீறல் · அழித்தல் |
| Sec 9 | `dpdp.children` | சரிபார்க்கத்தக்க பெற்றோர் சம்மதம் |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal உரிமைகள் |
| Sec 15 | `dpdp.duties` | Data Principal கடமைகள் |
| Sec 16 | `dpdp.cross_border` | எல்லை-தாண்டிய இடமாற்றம் |

407 சோதனைகள் வெற்றி.

---

## சட்ட மறுப்பு

இந்த மென்பொருள் **சட்ட ஆலோசனை அல்ல.** தகுதியான வழக்கறிஞருக்கு மாற்றாக இல்லை. Bar Council of India Rule 36 அடிப்படையில் — இது இலவச, திறந்த-மூல, MIT-உரிமம் கொண்ட பங்களிப்பு. வாடிக்கையாளர் சேகரிப்பு இல்லை, சட்ட சேவை விளம்பரம் இல்லை, வழக்கறிஞர்-வாடிக்கையாளர் உறவை உருவாக்கவில்லை.

## உரிமம்

MIT. முழு விவரத்திற்கு [English README](../README.md) பார்க்கவும்.

## பங்களிப்பு

இந்த மொழிபெயர்ப்பை சுத்திகரிக்க PR வரவேற்கப்படுகிறது.
