# dpdp-law-to-code

**ഇന്ത്യയുടെ ഡിജിറ്റൽ വ്യക്തിഗത ഡാറ്റ സംരക്ഷണ നിയമം, 2023 — പ്രവർത്തിപ്പിക്കാവുന്ന Python കോഡായി. MIT · ₹0 · പ്രാദേശിക-ആദ്യം.**

ഇന്ത്യൻ സർക്കാർ പരസ്യമായി പര്യവേക്ഷണം ആരംഭിച്ച ചട്ടക്കൂടിന്റെ ഒരു പൗരൻ-നിർമിത റഫറൻസ് നടപ്പാക്കൽ.

**വായിക്കുക:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *കമ്മ്യൂണിറ്റി വിവർത്തനം. ഇംഗ്ലീഷ് [README](../README.md) ആധികാരിക പതിപ്പ്. നിയമത്തിലെ നിർവചിച്ച പദങ്ങൾ (Data Fiduciary, Data Principal, മുതലായവ) DPDP Act 2023 മൂലപാഠവുമായി ഒത്തുനോക്കാൻ ഇംഗ്ലീഷിൽത്തന്നെ നിലനിർത്തിയിരിക്കുന്നു.*

---

## ഇത് എന്തിന് — MeitY-യുടെ സൂചന

2026 മേയ് 20-ന് *Economic Times* റിപ്പോർട്ട് ചെയ്തു: **ഇലക്ട്രോണിക്സ് ആൻഡ് ഇൻഫർമേഷൻ ടെക്നോളജി മന്ത്രാലയം (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** എന്ന ആശയം — DPDP Act 2023 വ്യവസ്ഥകളെ യന്ത്ര-നിർവഹണയോഗ്യമായ അൽഗോരിതങ്ങളിലേക്ക് വിവർത്തനം ചെയ്യൽ — സംബന്ധിച്ച് വ്യാപകമായ വ്യവസായ കൂടിയാലോചനകൾ നടത്തുന്നു.

ഹിമാംശി ലോഹ്ചാബ്, സുഭായൻ ചക്രവർത്തി എഴുതിയ *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 മേയ് 2026) റിപ്പോർട്ട് അനുസരിച്ച്, ഈ കൂടിയാലോചനകൾ ഏതാണ്ട് ഒരു മാസമായി തുടരുന്നു, ഫ്രണ്ടിയർ AI മാതൃകകളുടെ ദ്രുതഗതിയിലുള്ള പുരോഗതിക്ക് MeitY-യുടെ വിശാല പ്രതികരണത്തിന്റെ ഭാഗമാണ്.

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**ഈ റിപ്പോസിറ്ററി, സർക്കാർ പൊതുമുമ്പിൽ വെച്ച ചോദ്യത്തിന് ഒരു പൗരന്റെ ഉത്തരം.** ഇത് മത്സര നിർദേശമല്ല, വിമർശനവുമല്ല — പ്രവർത്തിക്കുന്ന, ഓപ്പൺ-സോഴ്സ് റഫറൻസ് നടപ്പാക്കൽ. MeitY ഔദ്യോഗിക ചട്ടക്കൂട് പ്രസിദ്ധീകരിക്കുകയാണെങ്കിൽ, ഈ റിപ്പോസിറ്ററി അതിനനുസരിച്ച് അപ്ഡേറ്റ് ചെയ്യും.

---

## ഇത് എന്താണ്

DPDP Act 2023 (വകുപ്പുകൾ 5–16) — `pip install` ചെയ്യാവുന്ന Python ലൈബ്രറി. ഓരോ check-ഉം `ComplianceResult` തിരികെ നൽകുന്നു, നിയമ ഉദ്ധരണി സഹിതം.

---

## ഇൻസ്റ്റാൾ

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. runtime dependencies ഇല്ല.

---

## എങ്ങനെ ഉപയോഗിക്കാം — മൂന്ന് വഴികൾ

### വഴി A — സ്വന്തം Python codebase-ൽ (ഡെവലപ്പർമാർ)
`from dpdp.consent import check_consent` — request handler അല്ലെങ്കിൽ CI pipeline-ൽ.

### വഴി B — ടെർമിനലിൽ നിന്ന് (കംപ്ലയൻസ് ഓഫീസർമാർ)
```bash
dpdp-check --section 6 --input consent.json
```

### വഴി C — AI സഹായിയിലൂടെ (അഭിഭാഷകർ, സ്ഥാപകർ)

Claude / Cursor / ChatGPT / Gemini-യോട് പറയുക — അത് സ്വയം ലൈബ്രറി install ചെയ്ത് check ചെയ്യും.

**⚠ അനിവാര്യമായ ഡാറ്റ-കൈകാര്യ അറിയിപ്പ്:**

DPDP Act 2023, **വകുപ്പ് 8(5)** പ്രകാരം ഓരോ Data Fiduciary-യും "ന്യായമായ സുരക്ഷാ നടപടികൾ" സ്വീകരിക്കണം. സൗജന്യ AI chatbot-ൽ യഥാർത്ഥ വ്യക്തിഗത ഡാറ്റ pastes ചെയ്യുന്നത് സ്വയം ഒരു ലംഘനമാകാം.

**യഥാർത്ഥ ഉൽപാദന ഡാറ്റ AI-യിലേക്ക് നൽകുന്നതിന് മുമ്പ് രണ്ട് നിബന്ധനകൾ:**

1. **പണമടച്ച / വാണിജ്യ API tier മാത്രം — Data Processing Agreement (DPA) സഹിതം:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (എല്ലാം പണമടച്ച).
2. **"Training-on-input" ഓഫ് ആണെന്ന് ഉറപ്പാക്കുക.** സൗജന്യ ChatGPT / Gemini / Claude.ai consumer നില യഥാർത്ഥ Data Principal വിവരത്തിന് അനുയോജ്യമല്ല.

പഠനം / പരീക്ഷണം / സാങ്കൽപിക ഉദാഹരണങ്ങൾക്ക് — ഏത് tier-ഉം ശരി. **യഥാർത്ഥ ഡാറ്റ** — പണമടച്ച API + DPA, അപവാദങ്ങളില്ല.

---

## v0.1-ൽ ഉൾപ്പെടുത്തിയ വകുപ്പുകൾ

| വകുപ്പ് | മൊഡ്യൂൾ | വിഷയം |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal-ന് അറിയിപ്പ് |
| Sec 6 | `dpdp.consent` | F-S-I-U-U സമ്മതം |
| Sec 7 | `dpdp.legitimate` | 9 നിയമപരമായ ഉപയോഗങ്ങൾ |
| Sec 8 | `dpdp.fiduciary` | Fiduciary കടമ · ലംഘനം · നീക്കം ചെയ്യൽ |
| Sec 9 | `dpdp.children` | സ്ഥിരീകരിക്കാവുന്ന രക്ഷാകർതൃ സമ്മതം |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal അവകാശങ്ങൾ |
| Sec 15 | `dpdp.duties` | Data Principal കടമകൾ |
| Sec 16 | `dpdp.cross_border` | അതിർത്തി-കടന്നുള്ള കൈമാറ്റം |

407 ടെസ്റ്റുകൾ വിജയം.

---

## നിയമപരമായ നിരാകരണം

ഈ സോഫ്റ്റ്‌വെയർ **നിയമോപദേശമല്ല.** യോഗ്യനായ അഭിഭാഷകന്റെ പകരക്കാരനല്ല. Bar Council of India Rule 36 പ്രകാരം — ഇത് സൗജന്യ, ഓപ്പൺ-സോഴ്സ്, MIT-ലൈസൻസ്ഡ് സംഭാവന. ക്ലയന്റ് സമാഹരണം ഇല്ല, നിയമ സേവന പരസ്യം ഇല്ല, അഭിഭാഷകൻ-ക്ലയന്റ് ബന്ധം രൂപപ്പെടുത്തുന്നില്ല.

## ലൈസൻസ്

MIT. പൂർണ വിശദാംശത്തിന് [English README](../README.md) കാണുക.

## സംഭാവന

ഈ വിവർത്തനം മെച്ചപ്പെടുത്താൻ PR സ്വാഗതം.
