# Physician Review — Phase 1 Gate: Med-Wisdom Cards

**Reviewer:** Physician, Heliotrope review board
**Date:** 2026-09-29
**Scope:** 9 med-wisdom cards (modafinil, iron, opill, vitamin-d, magnesium, l-theanine, multivitamin, hydroxyzine, propranolol)
**Standard:** informational-only framing (hard requirement); clinical accuracy; plain-language digestibility; cited sources.

## Overall verdict

**6 cards: CHANGES REQUIRED (all minor — wording precision, one citation, status-note consistency). 3 cards: APPROVED.**
**No hard-line violations found.** No card gives direct medical advice, no card green-lights alcohol or any behavior, every card carries the informational-only banner and an "ask your pharmacist or doctor" closing. Nothing in this batch would block the Phase 1 gate once the listed fixes land — all are quotable, surgical edits, no rewrites.

Cross-card checks:
- **Alcohol:** modafinil ("label advises avoiding"), hydroxyzine ("— no," label-consistent), propranolol (additive effects) — all informational, all safe, none a green light. ✓
- **Intra-list interactions:** modafinil↔Opill flagged on both cards; modafinil↔propranolol flagged on both cards; iron↔magnesium spacing on both cards; iron/multivitamin overlap addressed. ✓
- **Banners/closings:** present on all 9. ✓
- **Prozac:** correctly omitted (status unconfirmed). ✓
- **Hydroxyzine/propranolol:** correctly carry "on hand but NOT currently taking" status notes with "don't restart an old prescription on your own" counseling. ✓

---

## 1. modafinil.md — CHANGES REQUIRED (minor)

Accurate overall. Contraceptive interaction is label-faithful ("during treatment and for 1 month after stopping," routes to prescriber/pharmacist, no invented failure rates). Alcohol, driving, rash-watch, missed-dose guidance all sound.

**Fix — CYP2C19/propranolol wording overstates certainty.** The label's CYP2C19 data is in-vitro; propranolol is mainly cleared by other enzymes (CYP2D6/CYP1A2), so "examples include propranolol" implies more than the label supports.

> OLD: "Modafinil can *slow the clearance* of drugs cleared by CYP2C19 — examples include **propranolol**, omeprazole, diazepam, and some antidepressants. Propranolol on hand but not currently taken: worth a pharmacist conversation before it ever gets used."
>
> NEW: "Lab studies show modafinil reversibly inhibits the liver enzyme CYP2C19; in volunteers it raised exposure to omeprazole (a CYP2C19-cleared drug). Standard interaction references list **propranolol** as potentially affected — it is partly cleared by CYP2C19, though mainly by other enzymes — so the real-world significance is uncertain. Propranolol on hand but not currently taken: worth a pharmacist conversation before it ever gets used."

---

## 2. opill.md — APPROVED

Drafting-team flag #1 (Opill + modafinil wording) resolved: the wording is label-accurate, invents no norgestrel-specific failure rates, and routes to her prescriber (her prescriber) + pharmacist. The 3-hour rule verified word-by-word against the Drug Facts label: same-time-daily within 3-hour window ✓; <3h late = take now, no backup ✓; >3h late or missed = take ASAP (may mean 2 in one day) + 48h barrier backup ✓; start-day-1-of-period vs any-other-day backup rules ✓; no break week between packs ✓; vomiting/diarrhea-within-4-hours treated as missed ✓. The context note correctly states the FDA-labeled indication is pregnancy prevention while acknowledging her stated purpose, without endorsing off-label use. ✓

*Optional (not required):* the vomiting guidance could track the Drug Facts verbatim ("take another pill as soon as possible"); the card's simplified version is safe as written.

---

## 3. iron.md — APPROVED

Drafting-team flag #2 (alternate-day dosing) resolved: "ask your prescriber about alternatives like alternate-day dosing or a different formulation" is correctly framed as a prescriber conversation, not a directive — and it's an evidence-based adherence strategy, which matters because side effects are the #1 reason people abandon iron. Child-poisoning warning present and emphatic ✓. Empty-stomach/spacing rules, vitamin C note, "swallow whole," dark-stool normalization all standard. ✓

---

## 4. vitamin-d.md — CHANGES REQUIRED (minor)

Drafting-team flag #4 ("higher is not better" claim) resolved on accuracy: the 3-year trial summary (4,000–10,000 IU/day → lower wrist bone density than 400 IU) faithfully describes Burt et al., JAMA 2019. **But the trial is not in the sources list** — the banner cites only NIH ODS.

**Fix — cite the trial:**

> ADD to Sources: "Burt LA et al., JAMA 2019 — 3-year randomized trial of 400 vs 4,000 vs 10,000 IU/day vitamin D3 (n=311); higher doses associated with greater decline in radial volumetric bone mineral density."

Upper limit (4,000 IU/day, NIH), fat-with-food absorption, warfarin/vitamin K and thiazide cautions all accurate. ✓

---

## 5. magnesium.md — CHANGES REQUIRED (minor)

Content accurate: elemental-vs-compound dose, GI effects by form, 2-hour spacing from iron/thyroid meds/antibiotics, kidney-disease caution, "don't chase the dose upward." ✓

**Fix — status-note consistency.** Hydroxyzine/propranolol carry "not currently taking" notes; magnesium is *incoming* (not yet started) and should say so:

> ADD after the banner blockquote: "*Status note (set per med in the app): e.g. incoming — not started yet. Keep the card for when it arrives; show the label to your pharmacist alongside your other bottles.*"

---

## 6. l-theanine.md — CHANGES REQUIRED (minor)

Drafting-team flag #3 (no FDA label) handled well in the banner: "dietary supplement, not an FDA-approved medicine; not intended to diagnose, treat, cure, or prevent any disease." GRAS statement accurate. The modafinil-combination line ("a pharmacist conversation, not a DIY stack") is exactly the right framing. ✓

**Fixes:**
1. **Name the sources.** "NIH-adjacent supplement references" is weasel wording — there is no NIH ODS fact sheet for L-theanine.
> OLD: "*Sources: Health.com l-theanine review (safety, blood-pressure interaction, third-party testing); NIH-adjacent supplement references (GRAS status, studied dose ranges); Designs for Health technical sheet (hypotension caution, pregnancy contraindication).*"
>
> NEW: "*Sources: Health.com l-theanine review (safety, blood-pressure interaction, third-party testing); FDA GRAS Notice for L-theanine (GRAS status); published human trials typically using 100–200 mg/day, with safety data up to 900 mg/day (cite the specific trials in the card's reference list). Note: the pregnancy caution reflects limited data, not a studied risk — and the Designs for Health sheet is a manufacturer source, labeled as such.*"
2. **Soften dosing language to purely descriptive:**
> OLD: "Follow your product's label for dose — start low (50–100 mg is the common starting advice) and see how you respond."
>
> NEW: "Product labels commonly list 50–200 mg per serving — follow the product's label; published studies have typically used 100–200 mg."
3. **Add the incoming status note** (same text as magnesium fix above).

---

## 7. multivitamin.md — CHANGES REQUIRED (minor)

"Read the label before adding anything else" + "show the multivitamin label to your pharmacist alongside your other bottles" is excellent counseling for her stack (separate iron + D). Child-poisoning warning present ✓. Fat-soluble accumulation warning ✓.

**Fixes:**
1. **The dairy-spacing line is muddled** — the calcium/iron interplay is baked into the formulation; there is no standard "don't take a multi with dairy" rule, and it risks confusing the iron card's spacing rules.
> OLD: "**Spacing:** don't take it at the same time as dairy (calcium in the multi + iron interplay), and keep it 2–4 hours from tetracycline/fluoroquinolone antibiotics if you're ever prescribed them. Don't take an antacid within 1 hour before or 2 hours after."
>
> NEW: "**Spacing:** take it with food as directed; keep it 2–4 hours from tetracycline/fluoroquinolone antibiotics if you're ever prescribed them, and don't take an antacid within 1 hour before or 2 hours after (minerals and antacids interfere with each other's absorption). No special dairy spacing is needed for a multivitamin — the mineral interplay is already in the formulation."
2. **Add the incoming status note** (same text as magnesium fix above).
3. *Optional:* "High-dose vitamin C in the multi can interfere with B12 absorption" rests on old in-vitro data not confirmed in people — cut it or cite it. No separate B12 in this stack, so stakes are nil.

---

## 8. hydroxyzine.md — APPROVED

"On hand but NOT currently taking" status note ✓; "don't restart an old prescription on your own" ✓. Alcohol "— no" is emphatic but label-consistent and informational. QT-prolongation warning with correct example drugs (azithromycin, erythromycin, citalopram, fluoxetine) ✓; AGEP warning ✓; the documented sedation sensitivity acknowledged without turning the card into dosing advice ✓.

---

## 9. propranolol.md — CHANGES REQUIRED (minor)

"Never stop suddenly" as the emphasized #1 rule with the taper requirement is exactly right and the most important counseling point on this drug ✓. Alcohol, NSAID, hypoglycemia-masking, surgery/dentist cautions all accurate ✓.

**Fix — same CYP2C19 precision issue as the modafinil card.** "Both use the CYP2C19 pathway" is mechanistically imprecise (modafinil *inhibits* CYP2C19; it doesn't use it as a clearance pathway here).

> OLD: "**Interaction note:** modafinil can slow the clearance of propranolol (both use the CYP2C19 pathway), which could raise propranolol levels. She has both on hand. **A pharmacist should review this pair before propranolol is ever taken alongside modafinil.**"
>
> NEW: "**Interaction note:** modafinil inhibits the liver enzyme CYP2C19 in lab studies, and propranolol is partly cleared by CYP2C19 (its main clearance pathways are others), so propranolol levels *could* be affected — the clinical significance is uncertain. She has both on hand. **A pharmacist should review this pair before propranolol is ever taken alongside modafinil.**"

---

## Disposition

Once the six quotable fixes above land, all 9 cards are **APPROVED** from the physician seat. No informational-only violations, no unsafe guidance, no overstepped claims. The five drafting-team uncertainty flags are dispositioned above (#1 approved, #2 approved, #3 fixed via sourcing, #4 fixed via citation, #5 fixed via precision wording on both cards).

*Reviewer note for the gate report: the interaction-scanner and alcohol-check features (not in this batch) remain the highest-risk surfaces — the scanner must present "no interaction found" as absence of evidence, and the alcohol check must never emit a yes/safe output.*
