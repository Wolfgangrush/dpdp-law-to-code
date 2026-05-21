# dpdp-law-to-code

**ಭಾರತದ ಡಿಜಿಟಲ್ ವೈಯಕ್ತಿಕ ಡೇಟಾ ಸಂರಕ್ಷಣಾ ಕಾಯಿದೆ, 2023 — ಚಲಾಯಿಸಬಹುದಾದ Python ಕೋಡ್ ಆಗಿ. MIT · ₹0 · ಸ್ಥಳೀಯ-ಮೊದಲು.**

ಭಾರತ ಸರ್ಕಾರವು ಸಾರ್ವಜನಿಕವಾಗಿ ಅನ್ವೇಷಿಸಲು ಆರಂಭಿಸಿರುವ ಚೌಕಟ್ಟಿನ ಒಬ್ಬ ನಾಗರಿಕ-ನಿರ್ಮಿತ ಉಲ್ಲೇಖ ಅನುಷ್ಠಾನ.

**ಓದಿ:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *ಸಮುದಾಯ ಅನುವಾದ. ಆಂಗ್ಲ [README](../README.md) ಅಧಿಕೃತ ಆವೃತ್ತಿ. ಕಾಯಿದೆಯ ವ್ಯಾಖ್ಯಾನಿತ ಪದಗಳು (Data Fiduciary, Data Principal, ಇತ್ಯಾದಿ) DPDP Act 2023 ಮೂಲಪಾಠದೊಂದಿಗೆ ತಾಳೆಮಾಡಲು ಆಂಗ್ಲದಲ್ಲಿಯೇ ಉಳಿಸಲಾಗಿದೆ.*

---

## ಇದು ಏಕೆ ಇದೆ — MeitY ಸಂಕೇತ

20 ಮೇ 2026 ರಂದು *Economic Times* ವರದಿಯ ಪ್ರಕಾರ, **ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್ ಮತ್ತು ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ ಸಚಿವಾಲಯ (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** ಎಂಬ ಪರಿಕಲ್ಪನೆ — DPDP Act 2023 ನಿಬಂಧನೆಗಳನ್ನು ಯಂತ್ರ-ಕಾರ್ಯಗತ ಅಲ್ಗಾರಿದಮ್‌ಗಳಾಗಿ ಪರಿವರ್ತಿಸುವುದು — ಬಗ್ಗೆ ಉದ್ಯಮ ಪಾಲುದಾರರೊಂದಿಗೆ ವ್ಯಾಪಕ ಸಮಾಲೋಚನೆಗಳನ್ನು ನಡೆಸುತ್ತಿದೆ.

ಹಿಮಾಂಶಿ ಲೋಹ್ಚಾಬ್ ಮತ್ತು ಸುಭಾಯನ್ ಚಕ್ರವರ್ತಿ ಬರೆದ *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 ಮೇ 2026) ಲೇಖನದ ಪ್ರಕಾರ, ಈ ಸಮಾಲೋಚನೆಗಳು ಸುಮಾರು ಒಂದು ತಿಂಗಳಿನಿಂದ ನಡೆಯುತ್ತಿವೆ ಮತ್ತು ಫ್ರಾಂಟಿಯರ್ AI ಮಾದರಿಗಳ ತ್ವರಿತ ಪ್ರಗತಿಗೆ MeitY ವಿಶಾಲ ಪ್ರತಿಕ್ರಿಯೆಯ ಭಾಗ.

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**ಈ ರೆಪೋಸಿಟರಿ ಸರ್ಕಾರ ಸಾರ್ವಜನಿಕರ ಮುಂದೆ ಇಟ್ಟ ಪ್ರಶ್ನೆಗೆ ಒಬ್ಬ ನಾಗರಿಕನ ಉತ್ತರ.** ಇದು ಸ್ಪರ್ಧಾತ್ಮಕ ಪ್ರಸ್ತಾಪವಲ್ಲ, ಟೀಕೆಯೂ ಅಲ್ಲ — ಒಂದು ಕಾರ್ಯನಿರ್ವಹಿಸುವ, ತೆರೆದ-ಮೂಲ ಉಲ್ಲೇಖ ಅನುಷ್ಠಾನ. MeitY ಔಪಚಾರಿಕ ಚೌಕಟ್ಟನ್ನು ಪ್ರಕಟಿಸಿದರೆ, ಈ ರೆಪೋಸಿಟರಿ ಅದಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಪರಿಷ್ಕರಿಸಲಾಗುತ್ತದೆ.

---

## ಇದು ಏನು

DPDP Act 2023 (ವಿಭಾಗಗಳು 5–16) — `pip install` ಮಾಡಬಹುದಾದ Python ಗ್ರಂಥಾಲಯ. ಪ್ರತಿ check ಶಾಸನೋಲ್ಲೇಖದೊಂದಿಗೆ `ComplianceResult` ಹಿಂದಿರುಗಿಸುತ್ತದೆ.

---

## ಸ್ಥಾಪನೆ

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. runtime dependencies ಇಲ್ಲ.

---

## ಬಳಸುವುದು ಹೇಗೆ — ಮೂರು ದಾರಿಗಳು

### ದಾರಿ A — ನಿಮ್ಮ Python codebase ನಲ್ಲಿ (ಡೆವಲಪರ್‌ಗಳು)
`from dpdp.consent import check_consent` — request handler ಅಥವಾ CI pipeline ನಲ್ಲಿ.

### ದಾರಿ B — ಟರ್ಮಿನಲ್ ನಿಂದ (ಅನುಸರಣಾ ಅಧಿಕಾರಿಗಳು)
```bash
dpdp-check --section 6 --input consent.json
```

### ದಾರಿ C — AI ಸಹಾಯಕರ ಮೂಲಕ (ವಕೀಲರು, ಸ್ಥಾಪಕರು)

Claude / Cursor / ChatGPT / Gemini ಗೆ ಹೇಳಿ — ಅದು ತಾನೇ ಗ್ರಂಥಾಲಯವನ್ನು install ಮಾಡಿ check ಮಾಡುತ್ತದೆ.

**⚠ ಅಗತ್ಯ ಡೇಟಾ-ನಿರ್ವಹಣಾ ಸೂಚನೆ:**

DPDP Act 2023, **ವಿಭಾಗ 8(5)** ಪ್ರಕಾರ ಪ್ರತಿ Data Fiduciary "ಸಮಂಜಸ ಭದ್ರತಾ ಕ್ರಮಗಳನ್ನು" ತೆಗೆದುಕೊಳ್ಳಬೇಕು. ಉಚಿತ AI chatbot ಗೆ ನಿಜವಾದ ವೈಯಕ್ತಿಕ ಡೇಟಾ ಅಂಟಿಸುವುದು ಸ್ವತಃ ಉಲ್ಲಂಘನೆಯಾಗಬಹುದು.

**ನಿಜವಾದ ಡೇಟಾವನ್ನು AI ಗೆ ನೀಡುವ ಮೊದಲು ಎರಡು ಷರತ್ತುಗಳು:**

1. **ಪಾವತಿಸಿದ / ವಾಣಿಜ್ಯ API tier ಮಾತ್ರ — Data Processing Agreement (DPA) ಸಹಿತ:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (ಎಲ್ಲವೂ ಪಾವತಿಸಿದ).
2. **"Training-on-input" ಆಫ್ ಆಗಿದೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.** ಉಚಿತ ChatGPT / Gemini / Claude.ai consumer ಮಟ್ಟ ನಿಜವಾದ Data Principal ಮಾಹಿತಿಗೆ ಯೋಗ್ಯವಲ್ಲ.

ಕಲಿಕೆ / ಪ್ರಯೋಗ / ಕಾಲ್ಪನಿಕ ಉದಾಹರಣೆಗಳಿಗೆ — ಯಾವುದೇ tier ಸರಿ. **ನಿಜವಾದ ಡೇಟಾ** — ಪಾವತಿಸಿದ API + DPA, ವಿನಾಯಿತಿಗಳಿಲ್ಲ.

---

## v0.1 ರಲ್ಲಿ ಸೇರಿಸಲಾದ ವಿಭಾಗಗಳು

| ವಿಭಾಗ | ಮಾಡ್ಯೂಲ್ | ವಿಷಯ |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal ಗೆ ಸೂಚನೆ |
| Sec 6 | `dpdp.consent` | F-S-I-U-U ಸಮ್ಮತಿ |
| Sec 7 | `dpdp.legitimate` | 9 ಕಾನೂನುಬದ್ಧ ಬಳಕೆ |
| Sec 8 | `dpdp.fiduciary` | Fiduciary ಕರ್ತವ್ಯ · ಉಲ್ಲಂಘನೆ · ಅಳಿಸುವಿಕೆ |
| Sec 9 | `dpdp.children` | ಪರಿಶೀಲಿಸಬಹುದಾದ ಪೋಷಕ ಸಮ್ಮತಿ |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal ಹಕ್ಕುಗಳು |
| Sec 15 | `dpdp.duties` | Data Principal ಕರ್ತವ್ಯಗಳು |
| Sec 16 | `dpdp.cross_border` | ಗಡಿ-ಪಾರ ವರ್ಗಾವಣೆ |

407 ಪರೀಕ್ಷೆಗಳು ಉತ್ತೀರ್ಣ.

---

## ಕಾನೂನು ನಿರಾಕರಣೆ

ಈ ಸಾಫ್ಟ್‌ವೇರ್ **ಕಾನೂನು ಸಲಹೆ ಅಲ್ಲ.** ಅರ್ಹ ವಕೀಲರಿಗೆ ಬದಲಿ ಅಲ್ಲ. Bar Council of India Rule 36 ಪ್ರಕಾರ — ಇದು ಉಚಿತ, ತೆರೆದ-ಮೂಲ, MIT-ಪರವಾನಗಿಯ ಕೊಡುಗೆ. ಗ್ರಾಹಕ ಸಂಗ್ರಹಣೆ ಇಲ್ಲ, ಕಾನೂನು ಸೇವೆಗಳ ಜಾಹೀರಾತು ಇಲ್ಲ, ವಕೀಲ-ಗ್ರಾಹಕ ಸಂಬಂಧ ರೂಪಿಸುವುದಿಲ್ಲ.

## ಪರವಾನಗಿ

MIT. ಪೂರ್ಣ ವಿವರಕ್ಕೆ [English README](../README.md) ನೋಡಿ.

## ಕೊಡುಗೆ

ಈ ಅನುವಾದವನ್ನು ಪರಿಷ್ಕರಿಸಲು PR ಸ್ವಾಗತ.
