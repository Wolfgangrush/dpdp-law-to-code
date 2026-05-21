# dpdp-law-to-code

**भारताचा डिजिटल पर्सनल डेटा प्रोटेक्शन कायदा, 2023 — चालवण्यायोग्य Python कोड म्हणून. MIT · ₹0 · स्थानिक-प्रथम.**

भारत सरकारने ज्या चौकटीचा सार्वजनिक शोध सुरू केला आहे, त्याची नागरिकाने तयार केलेली एक संदर्भ अंमलबजावणी.

**हे वाचा:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *सामुदायिक भाषांतर. इंग्रजी [README](../README.md) हीच अधिकृत आवृत्ती आहे. कायद्यातील परिभाषित तांत्रिक शब्द (Data Fiduciary, Data Principal, Significant Data Fiduciary, Consent वगैरे) DPDP Act 2023 च्या मूळ मजकुराशी ताळमेळ साधण्यासाठी इंग्रजीतच ठेवले आहेत.*

---

## हे का अस्तित्वात आहे — MeitY चा संकेत

20 मे 2026 रोजी *Economic Times* ने वृत्त दिले की **इलेक्ट्रॉनिक्स आणि माहिती तंत्रज्ञान मंत्रालय (Ministry of Electronics and IT — MeitY)** ज्याला **"Law-to-Code"** म्हटले जाते — म्हणजेच डिजिटल पर्सनल डेटा प्रोटेक्शन कायदा 2023 च्या तरतुदींचे मशीन-निष्पादन योग्य अल्गोरिदममध्ये रूपांतर — या संकल्पनेवर उद्योगातील भागधारकांशी विस्तृत सल्लामसलत करत आहे.

हिमांशी लोहचब आणि सुभायन चक्रवर्ती यांचा लेख *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 मे 2026) सांगतो की ही सल्लामसलत साधारण एक महिन्यापासून चालू आहे आणि अत्याधुनिक AI मॉडेल्सच्या वेगवान प्रगतीला MeitY च्या व्यापक प्रतिसादाचा भाग आहे.

लेखातील थेट उद्धरण:

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

MeitY च्या सल्लामसलतीतून सुचवलेले व्यावहारिक उपयोग — संमतीशिवाय वैयक्तिक डेटाला प्रवेश थांबवणे, अनुमत कालावधीपलीकडे डेटा साठवल्यास इशारा, स्वयंचलित विलोपन कार्यप्रवाह, आणि उत्पादन प्रणालींमध्ये अंतर्निहित डिझाइन-दर-अनुपालन.

**ही रिपॉझिटरी सरकारने जनतेसमोर ठेवलेल्या प्रश्नाला एका नागरिकाचे उत्तर आहे.** हे प्रतिस्पर्धी प्रस्ताव नाही, टीकाही नाही. हे एक खुले-स्रोत, चालणारे संदर्भ-अंमलबजावणी आहे — या आशेने प्रकाशित की भारत सरकारने सुरू केलेला संवाद यामुळे जलद आणि अधिक ठोस होईल. MeitY ने औपचारिक चौकट प्रकाशित केल्यास, ही रिपॉझिटरी त्यानुसार अद्ययावत केली जाईल.

---

## हे काय आहे

DPDP कायदा 2023 (कलम 5–16) मधील कार्यान्वित तरतुदी एक `pip install` करण्यायोग्य Python ग्रंथालय म्हणून. प्रत्येक check `ComplianceResult` परत करते — ज्यात निकाल + कायद्याचा संदर्भ.

- एकल विकसक आज दुपारी आपल्या codebase मध्ये याचा वापर सुरू करू शकतो.
- स्टार्टअप अनुपालन संघ enterprise-sales call न करता ऑडिट करू शकते.
- संसाधनसंपन्न मोठ्या विधिसंस्था त्यांच्या व्यावसायिक चौकटी काळानुसार आणतील. ही चौकट खुली, मोफत, आणि आज उपलब्ध आहे.

---

## स्थापना

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. कोणत्याही runtime dependency नाहीत.

---

## हे कसे वापरावे — तीन मार्ग

### मार्ग A — आपल्या Python codebase मध्ये (विकसक)

`from dpdp.consent import check_consent` आयात करा आणि आपल्या request handler मध्ये call करा. CI pipeline मध्ये जोडा.

### मार्ग B — टर्मिनलमधून (अनुपालन अधिकारी, लेखापरीक्षक)

Python माहित असण्याची आवश्यकता नाही. फक्त एक आज्ञा चालवा:

```bash
dpdp-check --section 6 --input consent.json
```

सादा-इंग्रजी निकाल + कायद्याचा संदर्भ.

### मार्ग C — AI सहाय्यकाद्वारे (वकील, संस्थापक, कुणीही)

Claude, Cursor, ChatGPT, Gemini अशा AI सहाय्यकाला सांगा — तो स्वतःच library install करून check करेल.

**⚠ आवश्यक डेटा-संरक्षण सूचना — मार्ग C आधी अनिवार्य:**

DPDP कायदा 2023, **कलम 8(5)**, अंतर्गत प्रत्येक Data Fiduciary ला "वाजवी सुरक्षा उपाय" लागू आहेत. मोफत AI chatbot मध्ये खऱ्या वैयक्तिक डेटाची माहिती पेस्ट करणे म्हणजे स्वतःच एक संभाव्य उल्लंघन.

**वास्तविक डेटा देण्यापूर्वी दोन अनिवार्य अटी:**

1. **पेड / व्यावसायिक API tier वापरा — Data Processing Agreement (DPA) सहित:**
   - **Anthropic Claude API** (पेड · Commercial Terms)
   - **OpenAI API / Codex** (पेड · Enterprise terms)
   - **Google Gemini API** (पेड · Workspace / enterprise terms)
2. **"Training-on-input" बंद आहे याची खात्री करा.** मोफत ChatGPT / Gemini / Claude.ai ग्राहक-स्तरावर default ने इनपुट वापरतात — वास्तविक Data Principal माहितीसाठी अयोग्य.

केवळ **शिकण्यासाठी / प्रयोग / काल्पनिक उदाहरणे** — कोणताही tier चालेल. **वास्तविक डेटा** — पेड API + DPA, अपवाद नाहीत.

---

## v0.1 मध्ये समाविष्ट कलमे

| कलम | मॉड्यूल | विषय |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal ला सूचना |
| Sec 6 | `dpdp.consent` | F-S-I-U-U संमती + माघार |
| Sec 7 | `dpdp.legitimate` | 9 वैध वापर |
| Sec 8 | `dpdp.fiduciary` | Fiduciary दायित्व · भंग सूचना · विलोपन |
| Sec 9 | `dpdp.children` | सत्यापनयोग्य पालक-संमती |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal चे अधिकार |
| Sec 15 | `dpdp.duties` | Data Principal ची कर्तव्ये |
| Sec 16 | `dpdp.cross_border` | सीमापार हस्तांतरण |

407 चाचण्या उत्तीर्ण.

---

## कायदेशीर अस्वीकरण

हे सॉफ्टवेअर **कायदेशीर सल्ला नाही.** योग्य वकील-सल्ल्याचा पर्याय नाही. Bar Council of India Rule 36 अंतर्गत — हे मोफत, खुले-स्रोत, MIT-परवानाधारक योगदान आहे. ग्राहकांची याचना करत नाही, विधी-सेवांची जाहिरात करत नाही, वकील-ग्राहक नाते निर्माण करत नाही.

## परवाना

MIT. पूर्ण तपशिलासाठी [English README](../README.md) पाहा.

## योगदान

या भाषांतराला सुधारण्यासाठी PR आमंत्रित. पूर्ण तांत्रिक तपशील [English README](../README.md) मध्ये.
