# dpdp-law-to-code

**ভারতের ডিজিটাল পার্সোনাল ডেটা প্রোটেকশন আইন, 2023 — চালানোর উপযোগী Python কোড হিসেবে। MIT · ₹0 · স্থানীয়-প্রথম।**

ভারত সরকার যে কাঠামোর সর্বজনীন অনুসন্ধান শুরু করেছে, এটি তার একজন নাগরিকের তৈরি একটি রেফারেন্স বাস্তবায়ন।

**পড়ুন:** [English](../README.md) · [हिन्दी](README.hi.md) · [मराठी](README.mr.md) · [বাংলা](README.bn.md) · [தமிழ்](README.ta.md) · [తెలుగు](README.te.md) · [ಕನ್ನಡ](README.kn.md) · [മലയാളം](README.ml.md) · [ગુજરાતી](README.gu.md) · [ਪੰਜਾਬੀ](README.pa.md) · [اردو](README.ur.md)

> *কমিউনিটি অনুবাদ। ইংরেজি [README](../README.md) প্রামাণিক সংস্করণ। আইনের সংজ্ঞায়িত পরিভাষা (Data Fiduciary, Data Principal, ইত্যাদি) DPDP Act 2023-এর মূল পাঠের সাথে যাচাইযোগ্যতার জন্য ইংরেজিতেই রাখা হয়েছে।*

---

## কেন এই প্রকল্প — MeitY-এর সংকেত

20 মে 2026 তারিখে *Economic Times* জানায় যে **ইলেকট্রনিক্স ও তথ্যপ্রযুক্তি মন্ত্রণালয় (Ministry of Electronics and IT — MeitY)** **"Law-to-Code"** নামক একটি ধারণা — DPDP Act 2023-এর বিধানগুলিকে মেশিন-নির্বাহযোগ্য অ্যালগরিদমে অনুবাদ — নিয়ে শিল্পের অংশীদারদের সাথে ব্যাপক পরামর্শ চালাচ্ছে।

হিমাংশী লোহচব এবং সুভায়ন চক্রবর্তীর প্রতিবেদন *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* (Economic Times, 20 মে 2026) অনুযায়ী এই পরামর্শ প্রায় এক মাস ধরে চলছে এবং সীমান্ত-অগ্রগামী AI মডেলের দ্রুত উত্থানের প্রতিক্রিয়ায় MeitY-এর ব্যাপক পদক্ষেপের অংশ।

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

**এই রিপোজিটরি সরকার যে প্রশ্ন জনসমক্ষে রেখেছে তার একজন নাগরিকের উত্তর।** এটি প্রতিদ্বন্দ্বী প্রস্তাব নয়, সমালোচনাও নয় — একটি কার্যকর, ওপেন-সোর্স রেফারেন্স বাস্তবায়ন। MeitY আনুষ্ঠানিক কাঠামো প্রকাশ করলে, এই রিপোজিটরি তদনুযায়ী আপডেট হবে।

---

## এটি কী

DPDP Act 2023 (ধারা 5–16) এর কার্যকর বিধানগুলো `pip install`-যোগ্য Python লাইব্রেরিতে এনকোড করা — প্রতিটি ফাংশন `ComplianceResult` ফেরত দেয়, ধারার উদ্ধৃতি সহ।

---

## ইনস্টল

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10। কোনো runtime dependency নেই।

---

## ব্যবহার — তিনটি পথ

### পথ A — নিজস্ব Python কোডবেসে (ডেভেলপার)
`from dpdp.consent import check_consent` — request handler বা CI pipeline-এ ব্যবহার করুন।

### পথ B — টার্মিনাল থেকে (কমপ্লায়েন্স অফিসার)
```bash
dpdp-check --section 6 --input consent.json
```

### পথ C — AI সহায়কের মাধ্যমে (আইনজীবী, প্রতিষ্ঠাতা)

Claude / Cursor / ChatGPT / Gemini-কে বলুন — এটি নিজেই লাইব্রেরি ইনস্টল করে চেক করবে।

**⚠ অপরিহার্য ডেটা-হ্যান্ডলিং নোটিশ:**

DPDP Act 2023, **ধারা 8(5)** অনুযায়ী Data Fiduciary-কে "যুক্তিসঙ্গত নিরাপত্তা ব্যবস্থা" নিতে হবে। বিনামূল্যের consumer AI-তে প্রকৃত ব্যক্তিগত ডেটা পেস্ট করা নিজেই একটি লঙ্ঘন হতে পারে।

**প্রকৃত উৎপাদন ডেটা AI-তে দেওয়ার আগে দুটি শর্ত:**

1. **শুধুমাত্র পেইড / কমার্শিয়াল API tier — Data Processing Agreement (DPA) সহ:** Anthropic Claude API · OpenAI API / Codex · Google Gemini API (সকলেই পেইড)।
2. **"Training-on-input" বন্ধ আছে নিশ্চিত করুন।** বিনামূল্যের ChatGPT / Gemini / Claude.ai consumer স্তর প্রকৃত Data Principal তথ্যের জন্য উপযুক্ত নয়।

শেখা / পরীক্ষা / কাল্পনিক উদাহরণের জন্য — যেকোনো tier ঠিক আছে। প্রকৃত ডেটা — পেইড API + DPA, কোনো ব্যতিক্রম নেই।

---

## v0.1-এ অন্তর্ভুক্ত ধারা

| ধারা | মডিউল | বিষয় |
|---|---|---|
| Sec 5 | `dpdp.notice` | Data Principal-কে নোটিশ |
| Sec 6 | `dpdp.consent` | F-S-I-U-U সম্মতি |
| Sec 7 | `dpdp.legitimate` | 9টি বৈধ ব্যবহার |
| Sec 8 | `dpdp.fiduciary` | Fiduciary দায়িত্ব · ব্রিচ · মুছে ফেলা |
| Sec 9 | `dpdp.children` | যাচাইযোগ্য পিতামাতার সম্মতি |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary |
| Sec 11–14 | `dpdp.rights` | Data Principal-এর অধিকার |
| Sec 15 | `dpdp.duties` | Data Principal-এর কর্তব্য |
| Sec 16 | `dpdp.cross_border` | সীমান্ত-পার স্থানান্তর |

407টি টেস্ট পাস।

---

## আইনি দাবিত্যাগ

এই সফটওয়্যার **আইনি পরামর্শ নয়।** যোগ্য আইনজীবীর বিকল্প নয়। Bar Council of India Rule 36 অনুসারে — এটি বিনামূল্যের, ওপেন-সোর্স, MIT-লাইসেন্সকৃত অবদান। গ্রাহক সংগ্রহ বা আইনি পরিষেবা বিজ্ঞাপন নয়, আইনজীবী-গ্রাহক সম্পর্ক গঠন করে না।

## লাইসেন্স

MIT। পূর্ণ বিবরণের জন্য [English README](../README.md) দেখুন।

## অবদান

এই অনুবাদ পরিমার্জনের জন্য PR স্বাগত।
