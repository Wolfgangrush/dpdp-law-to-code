<div align="center">
  <img src="docs/banner.png" width="820"/>
  
  **DPDP Act 2023, Sections 5–16 — as runnable Python.**

  Visit the live site: [wolfgangrush.github.io](https://wolfgangrush.github.io)
</div>

<div align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"/></a>
  <img src="https://img.shields.io/badge/tests-407-brightgreen" alt="407 tests"/>
  <img src="https://img.shields.io/badge/CLI%20|%20Library%20|%20AI--assistant%20ready-blue" alt="CLI | Library | AI-assistant ready"/>
</div>


<div align="center">
  <img src="docs/banner.png" width="820"/>
  
  **DPDP Act 2023, Sections 5–16 — as runnable Python.**

  Visit the live site: [wolfgangrush.github.io](https://wolfgangrush.github.io)
</div>

<div align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"/></a>
  <img src="https://img.shields.io/badge/tests-407-brightgreen" alt="407 tests"/>
  <img src="https://img.shields.io/badge/CLI%20|%20Library%20|%20AI--assistant%20ready-blue" alt="CLI | Library | AI-assistant ready"/>
</div>


# dpdp-law-to-code

**India's Digital Personal Data Protection Act 2023 — as runnable Python. MIT · ₹0 · local-first.**

A citizen-built reference implementation of the framework the Government of India has begun publicly exploring.

**Read this in:** [English](README.md) · [हिन्दी](translations/README.hi.md) · [मराठी](translations/README.mr.md) · [বাংলা](translations/README.bn.md) · [தமிழ்](translations/README.ta.md) · [తెలుగు](translations/README.te.md) · [ಕನ್ನಡ](translations/README.kn.md) · [മലയാളം](translations/README.ml.md) · [ગુજરાતી](translations/README.gu.md) · [ਪੰਜਾਬੀ](translations/README.pa.md) · [اردو](translations/README.ur.md)

---

## Why this exists — the MeitY signal

On 20 May 2026, the *Economic Times* reported that the **Ministry of Electronics and IT (MeitY)** has been holding extensive industry consultations on a concept it calls **"Law-to-Code"** — translating Digital Personal Data Protection Act 2023 provisions into machine-executable algorithms.

The article, *"Coded Compliance: Centre is Eyeing 'Law-to-code' to AI-proof Data Law"* by Himanshi Lohchab and Subhayan Chakraborty (*Economic Times*, 20 May 2026 — [link](https://economictimes.indiatimes.com/tech/technology/coded-compliance-centre-is-eyeing-law-to-code-to-ai-proof-data-law/articleshow/131209144.cms)), reports that these consultations have been ongoing for approximately a month and form part of MeitY's broader response to the rapid advance of frontier AI systems. A government official quoted in the piece characterises the proposal as *"a relatively new concept that's been suggested, and we are looking into it"* — placing the initiative at the consultation stage, not at any formal commitment stage.

Quoting the article directly:

> *"Law-to-code is the practice of translating legal rules into machine-executable algorithms such as a Python code that software can automatically process and enforce without human intervention."*

> *"A 'base code' for legal provisions can ensure that systems are compliant by design without needing an army of lawyers to interpret every technical step."*

The applications MeitY's consultations have publicly identified include:

- Blocking attempts to access personal data without valid consent
- Raising alerts on illegal retention of customer data beyond permissible duration
- Auto-deletion workflows when retention windows lapse
- Compliance-by-design enforcement embedded directly in production systems

No formal MeitY framework on Law-to-Code has been committed to in the public record yet — the article reports consultations and ministerial interest, but the named official describes the concept itself as *"relatively new"* and *"being looked into."* Based on typical Indian government consultation-to-publication timelines for a technical framework of this scope, a published framework is plausibly **6 to 18 months away or longer**.

**This repository is one citizen's response to the question MeitY has placed before the public.** It is not a competing proposal. It is not a critique. It is a working, runnable, openly-licensed reference implementation — published in the hope that it accelerates and grounds the conversation that the Government of India has begun.

If MeitY publishes a formal framework, this repository will be updated to align with it.

---

## What this framework is

A `pip install`-able Python library that encodes the operative provisions of the DPDP Act 2023 (Sections 5–16) as testable, type-hinted Python functions. Every check returns a structured `ComplianceResult` with the statute citation.

- A solo developer can drop it into a codebase this afternoon.
- A startup compliance team can audit it without an enterprise-sales call.
- A regulator or researcher can read and run every rule in one repository.
- Big law firms with resources will, in time, produce their own commercial frameworks. This one is open, free, and available today.

---

## Install

```bash
pip install dpdp-law-to-code
```

Python ≥ 3.10. No runtime dependencies.

---

## How to use this — three paths

This library serves three different audiences. Pick the path that fits you.

### Path A — Inside your own Python codebase (developers)

If your team already uses Python, treat this as any other library:

```python
from dpdp.consent import check_consent
from dpdp.types import ConsentRecord

result = check_consent(ConsentRecord(...))
if not result.compliant:
    raise PermissionError(f"{result.section}: {result.reason}")
```

Wire it into your request handler to block non-compliant flows in real time. Wire it into your CI pipeline to fail builds on regression.

### Path B — From the terminal (compliance officers, auditors)

You do not need to know Python. You only need to open a terminal and run one command.

**Step 1.** Install once:

```bash
pip install dpdp-law-to-code
```

**Step 2.** Save your facts as a JSON file (`consent.json`):

```json
{
  "is_free": true,
  "is_specific": true,
  "is_informed": true,
  "is_unconditional": true,
  "is_unambiguous": true,
  "has_clear_affirmative_action": true,
  "is_limited_to_specified_purpose": true,
  "is_withdrawable_easily": true,
  "is_pre_checked": false,
  "is_bundled_with_unrelated_terms": false
}
```

**Step 3.** Run the check:

```bash
dpdp-check --section 6 --input consent.json
```

You get a plain-English verdict with the statute citation.

### Path C — Through an AI assistant (lawyers, founders, anyone)

If you use an AI assistant (Claude, Cursor, ChatGPT, Gemini, or similar code-aware tool), you do not need to install anything yourself. The assistant can install and call this library for you. But before you paste anything that could identify a real Data Principal, please read the data-handling notice below.

#### ⚠ Data-handling notice — required reading before Path C

The DPDP Act 2023, Sec 8(5), requires every Data Fiduciary to protect personal data "by taking reasonable security safeguards to prevent personal data breach." Pasting real personal data into an AI assistant without the right contractual safeguards is itself a breach in the making.

**Two non-negotiable conditions before feeding any production fact-pattern to an AI assistant:**

1. **Use a paid / commercial API tier governed by a Data Processing Agreement (DPA) or equivalent contract.** Free consumer chatbots may use your inputs to train their models — incompatible with Sec 8(5). Recommended commercial endpoints:
   - **Anthropic Claude API** (paid tier · Commercial Terms include data-processing provisions)
   - **OpenAI API / Codex** (paid tier · Enterprise terms or API DPA)
   - **Google Gemini API** (paid tier · Workspace / enterprise terms)
2. **Confirm training-on-input is OFF.** Free ChatGPT, free Gemini, free Claude.ai consumer tier and similar free chat tools may use inputs to improve models by default. They are inappropriate for any data that could identify a real person.

For **learning, exploration, or synthetic examples** — any tier is fine. For **anything that could identify a real Data Principal** — paid API tier with a DPA, no exceptions.

#### How to use Path C

Once you have confirmed both conditions above, open your assistant and paste a prompt like:

> *"Please install `dpdp-law-to-code` (https://github.com/Wolfgangrush/dpdp-law-to-code) and use it to check whether the following consent banner is compliant with the DPDP Act 2023:*
>
> *Our cookie banner shows two buttons: 'Accept All' (pre-checked) and 'Reject Non-Essential' (smaller, greyed out). The banner does not explain what data is collected. Users can withdraw consent only by writing to support@example.com.*
>
> *Tell me the section, the reason, and the statute citation. Quote the source code from the library so I can verify."*

The assistant will:

1. Install the library in its sandboxed environment
2. Construct the appropriate `ConsentRecord` from your description
3. Call `check_consent` and return the `ComplianceResult`
4. Quote the statutory provision the result is grounded in

This path is the most common one for non-developers. You get a citation-grounded verdict in seconds, without writing or installing anything yourself. **The AI is doing the work; this library is what gives the AI its rulebook.**

> *The verdict an AI assistant returns is only as reliable as the library it is calling. This library encodes a developer-friendly reading of the Act and is not a substitute for qualified legal counsel. Always verify against the statute and consult a lawyer for contentious matters.*

---

## Three runnable examples

### Sec 6 — consent banner check

```python
from dpdp.consent import check_consent
from dpdp.types import ConsentRecord

result = check_consent(ConsentRecord(
    is_free=True,
    is_specific=True,
    is_informed=True,
    is_unconditional=True,
    is_unambiguous=True,
    has_clear_affirmative_action=True,
    is_limited_to_specified_purpose=True,
    is_withdrawable_easily=True,
    is_pre_checked=False,
    is_bundled_with_unrelated_terms=False,
))

print(result.compliant, result.section, result.citation)
# True Sec 6 DPDP Act 2023, Sec 6
```

### Sec 16 — cross-border transfer

```python
from dpdp.cross_border import check_cross_border_transfer
from dpdp.types import CrossBorderTransfer

result = check_cross_border_transfer(CrossBorderTransfer(
    destination_country_iso="DE",
    sectoral_law_restriction_applies=False,
    central_govt_has_notified_restriction=False,
))

print(result.compliant, result.reason)
# True  "transfer to DE permissible — no Central Govt restriction notified
#        + no higher sectoral law restriction asserted"
```

### Sec 8 — breach-notification window

```python
from dpdp.fiduciary import check_breach_notification
from dpdp.types import BreachRecord

result = check_breach_notification(BreachRecord(
    detected_at_unix=1_716_000_000,
    notified_board_at_unix=1_716_000_000 + 60 * 60 * 12,
    notified_affected_principals_at_unix=1_716_000_000 + 60 * 60 * 24,
    affected_principal_count=4200,
    breach_description="unauthorized access to user table",
))

print(result.compliant, result.section)
```

Three polished, copy-pasteable variants live in `examples/`.

---

## Sections shipped in v0.1

| Section | Module | Subject |
|---|---|---|
| Sec 5 | `dpdp.notice` | Notice requirement to Data Principal |
| Sec 6 | `dpdp.consent` | Free / Specific / Informed / Unconditional / Unambiguous + withdrawal |
| Sec 7 | `dpdp.legitimate` | The 9 enumerated legitimate-use cases |
| Sec 8 | `dpdp.fiduciary` | Fiduciary obligations · breach notification · erasure |
| Sec 9 | `dpdp.children` | Verifiable parental consent · no tracking · no targeted ads |
| Sec 10 | `dpdp.sdf` | Significant Data Fiduciary threshold + obligations |
| Sec 11–14 | `dpdp.rights` | Access · correction · grievance · nomination |
| Sec 15 | `dpdp.duties` | Data Principal duties |
| Sec 16 | `dpdp.cross_border` | Negative list (16(1)) + sectoral-law preservation (16(2)) |

407 tests pass across all sections.

Each check returns a `ComplianceResult(compliant, section, reason, citation, sub_results)`. The `sub_results` list carries per-sub-clause findings where the section has internal structure (e.g. Sec 10(2)(a)(i)–(iv) DPO requirements).

---

## CLI

```bash
dpdp-check --list-sections
dpdp-check --section 6 --input consent.json
dpdp-check --section 16 --input transfer.json --json
```

Exit codes: `0` compliant · `1` non-compliant · `2` input error · `3` validation error.

---

## Language support — Eighth Schedule readiness

The DPDP Act 2023, **Sec 5(3)**, requires that notice be available in English or any of the **22 languages listed in the Eighth Schedule** of the Constitution of India. The `NoticeRecord` schema in this library carries a dedicated field — `available_in_english_or_eighth_schedule_language` — and the `check_notice` function enforces it.

The compliance logic itself is language-agnostic: a statute citation in Hindi, Marathi, Tamil, Bengali, Telugu, or any other Eighth Schedule language is treated identically by every checker.

Translations of this README are already shipped under `translations/`:

हिन्दी (Hindi) · मराठी (Marathi) · বাংলা (Bengali) · தமிழ் (Tamil) · తెలుగు (Telugu) · ಕನ್ನಡ (Kannada) · മലയാളം (Malayalam) · ગુજરાતી (Gujarati) · ਪੰਜਾਬੀ (Punjabi) · اردو (Urdu)

Translations into additional Eighth Schedule languages are welcome — submit as `README.<lang>.md` (e.g. `README.or.md` for Odia, `README.as.md` for Assamese).

---

## What v0.1 is not

- Not a web UI / dashboard
- Not a database integration
- Not cloud-hosted
- Not a live regulatory-update feed (planned v0.2+)
- Not a replacement for qualified legal counsel
- Not Sec 17/18+ (Data Protection Board structure + penalties — deferred to v0.2)

---

## Legal disclaimer

This software is **not legal advice**. It encodes a developer-friendly reading of the DPDP Act 2023 and Draft Rules 2025 (G.S.R. 846(E), MeitY Notification dated 13 November 2025) as a compliance harness. It is not a substitute for qualified legal counsel.

Bar Council of India Rule 36 considerations: this is a free, open-source, MIT-licensed contribution. It does not solicit clients, does not advertise legal services, and does not constitute a lawyer–client engagement.

---

## License

MIT. See `LICENSE`.

---

## Contributing

PRs welcome — especially for:

- Sec 16 cross-border list updates (when MeitY notifies countries under Sec 16(1))
- Sec 17+ Data Protection Board structure (out of scope for v0.1)
- Additional test scenarios and edge cases
- README translations into any of the 22 Eighth Schedule languages
- Worked examples for specific sectors (fintech · healthtech · e-commerce · employment)

---

## Acknowledgements

The framing of this library was sharpened by Lohchab & Chakraborty's reporting in the *Economic Times* on MeitY's Law-to-Code consultations (20 May 2026). The Act text and Rules text are sourced from MeitY publications at meity.gov.in.
