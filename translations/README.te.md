# dpdp-law-to-code

**భారతదేశ డిజిటల్ వ్యక్తిగత డేటా రక్షణ చట్టం, 2023 — అమలు చేయగల Python కోడ్‌గా. MIT · ₹0 · స్థానిక-ప్రథమ.**

భారత ప్రభుత్వం బహిరంగంగా అన్వేషించడం ప్రారంభించిన ఫ్రేమ్‌వర్క్‌కు పౌరుడిచే నిర్మించబడిన ఒక సూచిక అమలు.

**చదవండి:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *కమ్యూనిటీ అనువాదం. ఆంగ్ల [README](../README.md) అధికారిక సంస్కరణ. చట్టంలో నిర్వచించబడిన పదాలు (Data Fiduciary, Data Principal, మొదలైనవి) DPDP Act 2023 మూల పాఠంతో సరిపోల్చడానికి ఆంగ్లంలోనే ఉంచబడ్డాయి.*

---

## ఇది ఎందుకు ఉంది — MeitY సంకేతం

20 మే 2026న *Economic Times* నివేదిక ప్రకారం, **ఎలక్ట్రానిక్స్ మరియు ఇన్ఫర్మేషన్ టెక్నాలజీ మంత్రిత్వ శాఖ (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** అని పిలవబడే భావనపై — DPDP Act 2023 నిబంధనలను యంత్ర-అమలు చేయగల అల్గోరిథమ్‌లుగా అనువదించడం — పరిశ్రమ భాగస్వాములతో విస్తృత సంప్రదింపులు జరుపుతోంది.

హిమాంశీ లోహ్‌చబ్ మరియు సుభాయన్ చక్రవర్తి రాసిన *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 మే 2026) వ్యాసం ప్రకారం, ఈ సంప్రదింపులు దాదాపు ఒక నెల పాటు సాగుతున్నాయి మరియు అత్యాధునిక AI మోడల్స్ వేగవంతమైన అభివృద్ధికి MeitY విస్తృత ప్రతిస్పందనలో భాగం.

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**ఈ రిపాజిటరీ ప్రభుత్వం ప్రజల ముందు ఉంచిన ప్రశ్నకు ఒక పౌరుడి సమాధానం.** ఇది పోటీ ప్రతిపాదన కాదు, విమర్శ కాదు — ఒక పనిచేసే, ఓపెన్-సోర్స్ సూచిక అమలు. MeitY అధికారిక ఫ్రేమ్‌వర్క్‌ను ప్రచురిస్తే, ఈ రిపాజిటరీ తదనుగుణంగా నవీకరించబడుతుంది.

---

## ఇది ఏమిటి

DPDP Act 2023 (సెక్షన్లు 5–16) — `pip install` చేయగల Python లైబ్రరీ. ప్రతి check `ComplianceResult` తిరిగి ఇస్తుంది, చట్ట ఉల్లేఖనంతో.

---

## ఇన్‌స్టాల్

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. ఎలాంటి runtime dependencies లేవు.

---

## ఎలా ఉపయోగించాలి — మూడు మార్గాలు

### మార్గం A — మీ Python codebase లో (డెవలపర్లు)
`from dpdp.consent import check_consent` — request handler లేదా CI pipeline లో వాడండి.

### మార్గం B — టెర్మినల్ నుండి (కంప్లయన్స్ ఆఫీసర్లు)
```bash
dpdp-check --section 6 --input consent.json
```

### మార్గం C — AI సహాయకుడి ద్వారా (న్యాయవాదులు, వ్యవస్థాపకులు)

Claude / Cursor / ChatGPT / Gemini-కి చెప్పండి — అది లైబ్రరీని install చేసి check చేస్తుంది.

**⚠ తప్పనిసరి డేటా-నిర్వహణ నోటీసు:**

DPDP Act 2023, **సెక్షన్ 8(5)** ప్రకారం ప్రతి Data Fiduciary "సహేతుకమైన భద్రతా చర్యలు" తీసుకోవాలి. ఉచిత AI chatbot లో అసలు వ్యక్తిగత డేటా పేస్ట్ చేయడం స్వయంగా ఉల్లంఘన కావచ్చు.

**అసలు ఉత్పత్తి డేటాను AI కి ఇచ్చే ముందు రెండు షరతులు:**

1. **చెల్లింపు / వాణిజ్య API tier మాత్రమే — Data Processing Agreement (DPA) తో:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (అన్నీ చెల్లింపు).
2. **"Training-on-input" ఆఫ్ ఉందని నిర్ధారించుకోండి.** ఉచిత ChatGPT / Gemini / Claude.ai consumer స్థాయి అసలు Data Principal సమాచారానికి తగదు.

అభ్యాసం / ప్రయోగం / కల్పిత ఉదాహరణలకు — ఏ tier అయినా సరే. **అసలు డేటా** — చెల్లింపు API + DPA, మినహాయింపులు లేవు.

---

## v0.1 లో చేర్చబడిన సెక్షన్లు

| సెక్షన్ | మాడ్యూల్ | అంశం |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal కి నోటీసు |
| Sec 6 | `dpdp.consent` | F-S-I-U-U సమ్మతి |
| Sec 7 | `dpdp.legitimate` | 9 చట్టబద్ధ ఉపయోగాలు |
| Sec 8 | `dpdp.fiduciary` | Fiduciary బాధ్యత · ఉల్లంఘన · తొలగింపు |
| Sec 9 | `dpdp.children` | ధృవీకరించదగిన తల్లిదండ్రుల సమ్మతి |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal హక్కులు |
| Sec 15 | `dpdp.duties` | Data Principal విధులు |
| Sec 16 | `dpdp.cross_border` | సరిహద్దు-దాటిన బదిలీ |

407 పరీక్షలు పాస్.

---

## చట్టపరమైన నిరాకరణ

ఈ సాఫ్ట్‌వేర్ **చట్టపరమైన సలహా కాదు.** అర్హత గల న్యాయవాదికి ప్రత్యామ్నాయం కాదు. Bar Council of India Rule 36 ప్రకారం — ఇది ఉచిత, ఓపెన్-సోర్స్, MIT-లైసెన్స్ సహకారం. క్లయింట్ సేకరణ లేదు, చట్ట సేవల ప్రకటన లేదు, న్యాయవాది-క్లయింట్ సంబంధం ఏర్పడదు.

## లైసెన్స్

MIT. పూర్తి వివరాల కోసం [English README](../README.md) చూడండి.

## సహకారం

ఈ అనువాదాన్ని మెరుగుపరచడానికి PR స్వాగతం.
