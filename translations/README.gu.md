# dpdp-law-to-code

**ભારતનો ડિજિટલ વ્યક્તિગત ડેટા સંરક્ષણ અધિનિયમ, 2023 — ચલાવી શકાય તેવી Python કોડ તરીકે. MIT · ₹0 · સ્થાનિક-પ્રથમ.**

ભારત સરકારે જે માળખું જાહેરમાં શોધવાનું શરૂ કર્યું છે, તેનું એક નાગરિક-નિર્મિત સંદર્ભ અમલીકરણ.

**વાંચો:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *કમ્યુનિટી અનુવાદ. અંગ્રેજી [README](../README.md) અધિકૃત આવૃત્તિ. અધિનિયમની વ્યાખ્યાયિત તકનીકી શબ્દાવલી (Data Fiduciary, Data Principal, વગેરે) DPDP Act 2023 ના મૂળ પાઠ સાથે ચકાસણી માટે અંગ્રેજીમાં જ રાખવામાં આવી છે.*

---

## આ શા માટે છે — MeitY નો સંકેત

20 મે 2026 ના રોજ *Economic Times* એ અહેવાલ આપ્યો કે **ઇલેક્ટ્રોનિક્સ અને માહિતી ટેકનોલોજી મંત્રાલય (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** તરીકે ઓળખાતી વિભાવના — DPDP Act 2023 ની જોગવાઈઓને મશીન-અમલીકરણ યોગ્ય અલ્ગોરિધમ્સમાં અનુવાદિત કરવાની — પર ઉદ્યોગના હિતધારકો સાથે વ્યાપક પરામર્શ યોજી રહ્યું છે.

હિમાંશી લોહચબ અને સુભાયન ચક્રવર્તીનો લેખ *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 મે 2026) મુજબ, આ પરામર્શ લગભગ એક મહિનાથી ચાલી રહ્યો છે અને અદ્યતન AI મોડેલ્સની ઝડપી પ્રગતિ માટે MeitY ના વ્યાપક પ્રતિસાદનો ભાગ છે.

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**આ રિપોઝિટરી સરકારે જનતા સમક્ષ મૂકેલા પ્રશ્નનો એક નાગરિકનો જવાબ છે.** તે સ્પર્ધાત્મક પ્રસ્તાવ નથી, ટીકા પણ નથી — એક કાર્યરત, ઓપન-સોર્સ સંદર્ભ અમલીકરણ છે. જો MeitY ઔપચારિક માળખું પ્રકાશિત કરે, તો આ રિપોઝિટરી તદનુસાર અપડેટ કરવામાં આવશે.

---

## આ શું છે

DPDP Act 2023 (કલમો 5–16) — `pip install` કરી શકાય તેવી Python લાઇબ્રેરી. દરેક check `ComplianceResult` પરત કરે છે, કાનૂની ઉદ્ધરણ સાથે.

---

## ઇન્સ્ટોલ

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. કોઈ runtime dependencies નથી.

---

## કેવી રીતે ઉપયોગ કરવો — ત્રણ માર્ગો

### માર્ગ A — તમારી Python codebase માં (ડેવલપર્સ)
`from dpdp.consent import check_consent` — request handler અથવા CI pipeline માં.

### માર્ગ B — ટર્મિનલમાંથી (કમ્પ્લાયન્સ ઓફિસર્સ)
```bash
dpdp-check --section 6 --input consent.json
```

### માર્ગ C — AI સહાયક દ્વારા (વકીલો, સ્થાપકો)

Claude / Cursor / ChatGPT / Gemini-ને કહો — તે પોતે જ લાઇબ્રેરી install કરીને check કરશે.

**⚠ આવશ્યક ડેટા-હેન્ડલિંગ સૂચના:**

DPDP Act 2023, **કલમ 8(5)** મુજબ દરેક Data Fiduciary "વાજબી સુરક્ષા પગલાં" લેવા જરૂરી છે. મફત AI chatbot માં વાસ્તવિક વ્યક્તિગત ડેટા pastes કરવો એ પોતે ઉલ્લંઘન બની શકે છે.

**વાસ્તવિક ઉત્પાદન ડેટા AI ને આપતા પહેલા બે શરતો:**

1. **માત્ર પેઇડ / કમર્શિયલ API tier — Data Processing Agreement (DPA) સાથે:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (બધા પેઇડ).
2. **"Training-on-input" બંધ છે તેની ખાતરી કરો.** મફત ChatGPT / Gemini / Claude.ai consumer સ્તર વાસ્તવિક Data Principal માહિતી માટે યોગ્ય નથી.

શીખવા / પ્રયોગ / કાલ્પનિક ઉદાહરણો માટે — કોઈપણ tier ઠીક છે. **વાસ્તવિક ડેટા** — પેઇડ API + DPA, કોઈ અપવાદ નહીં.

---

## v0.1 માં સમાવિષ્ટ કલમો

| કલમ | મોડ્યુલ | વિષય |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal ને નોટિસ |
| Sec 6 | `dpdp.consent` | F-S-I-U-U સંમતિ |
| Sec 7 | `dpdp.legitimate` | 9 કાનૂની ઉપયોગો |
| Sec 8 | `dpdp.fiduciary` | Fiduciary જવાબદારી · ઉલ્લંઘન · ભૂંસવું |
| Sec 9 | `dpdp.children` | ચકાસી શકાય તેવી માતા-પિતાની સંમતિ |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal ના અધિકારો |
| Sec 15 | `dpdp.duties` | Data Principal ની ફરજો |
| Sec 16 | `dpdp.cross_border` | સરહદ-પાર સ્થાનાંતરણ |

407 પરીક્ષણો પાસ.

---

## કાનૂની અસ્વીકાર

આ સોફ્ટવેર **કાનૂની સલાહ નથી.** લાયક વકીલનો વિકલ્પ નથી. Bar Council of India Rule 36 મુજબ — આ મફત, ઓપન-સોર્સ, MIT-લાઇસન્સ યુક્ત યોગદાન છે. ગ્રાહક સંગ્રહ નથી, કાનૂની સેવાઓની જાહેરાત નથી, વકીલ-ગ્રાહક સંબંધ બનાવતું નથી.

## લાઇસન્સ

MIT. સંપૂર્ણ વિગતો માટે [English README](../README.md) જુઓ.

## યોગદાન

આ અનુવાદને સુધારવા માટે PR આવકાર્ય.
