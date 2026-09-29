# "Things you might not know" — proactive teaching surface spec

*Healthcare-complaints team, Phase 1. This spec defines Heliotrope's answer to the complaint she stated herself: "I'm not a doctor, I don't know all the things I even need to know."*

## The problem it solves

Nobody teaches patients the practical layer of healthcare. Doctors prescribe; pharmacists dispense; neither has time to explain what "take with food" actually means, why the bathroom is the worst place for pills, or what an EOB is. The result: ~50% of patients don't take meds as prescribed ([drugtopics.com](https://www.drugtopics.com/view/rethinking-medication-adherence-patient-centered-solutions-for-better-outcomes)), 30% never fill the first prescription, and 93% of pharmacists say patients don't grasp what non-adherence costs them ([pharmacymagazine.co.uk](https://www.pharmacymagazine.co.uk/news/patients-failing-to-grasp-impact-of-non-adherence)). This surface closes that gap *before* she's standing at a pharmacy counter confused.

## Design principles

1. **Proactive, not searchable.** She shouldn't have to know the question to get the answer. The surface pushes the right card at the right moment.
2. **One idea per card.** A card teaches exactly one thing in plain language, in under 30 seconds of reading. No walls of text.
3. **Contextual first, browsable second.** Cards appear where they're relevant (photographing a new bottle → storage card) AND live in a browsable library.
4. **Physician-reviewed.** Every card passes the Heliotrope physician reviewer before it ships. Cards carry a review stamp and date. Informational only — every card ends with "ask your pharmacist or doctor."
5. **Never preachy, never scary.** Tone: the knowledgeable friend who already made this mistake so you don't have to. No shame about what she doesn't know.
6. **Dismissible and resumable.** She can dismiss a card; dismissed cards don't nag. A "show me again" library keeps them available.

## Where the surface lives in the app

| Placement | Behavior |
|---|---|
| **Meds tab → new med added** | When she adds a med (or photographs a bottle), the matching wisdom card (`docs/med-wisdom/`) appears inline — storage, spacing, missed-dose rules for *that* med. The general-principles cards stay out of the way until relevant. |
| **Today → "tip" slot** | One small, rotating tip under the day's summary — e.g., "Your iron works best 2 hours away from coffee." Tappable to the full card. Max one per day; never above her meds/tasks. |
| **Teach-me library (Meds tab section)** | The full browsable catalog below, grouped by topic. Searchable. Each card shows its review stamp. |
| **Contextual triggers** | Examples: she logs a missed dose → the missed-dose general card surfaces once. She adds a second supplement → the "check for overlap" card surfaces. She gets a lab with an unfamiliar marker → the "reading your labs" card surfaces. |

## The catalog — knowledge gaps, grouped

### A. Storing meds (the thing nobody tells you)

1. **The bathroom is the worst place for pills.** Heat and humidity from showers degrade medications fast — even before the expiry date. Pharmacists' rule: "medicines like the kind of environment people like — a little dry, not too hot or cold" ([NPR](https://www.mtpr.org/2017-02-06/when-old-medicine-goes-bad)). Best spots: bedroom cabinet, pantry shelf, dedicated box — cool, dry, dark, out of reach of kids.
2. **Keep meds in their original containers.** The label has the drug name, strength, expiry, and directions. Decanting into unmarked bottles or baggies loses all of that — and some meds (iron, certain antibiotics) need their original light/moisture protection.
3. **Weekly pill organizers are fine — with one rule.** They're great for adherence, but don't load a month at once; a week at a time, and keep the stock bottles sealed. Moisture-sensitive meds suffer in open compartments.
4. **Travel rules:** carry meds in original labeled containers, in carry-on (never checked luggage), never leave them in a hot car. For controlled substances (like modafinil), the original labeled container isn't optional — it's the proof it's yours.
5. **Fridge or not?** Most meds: room temperature. Only refrigerate if the label says so. Never freeze meds unless the label says to.

### B. Expiry dates and disposal

6. **What an expiry date actually means.** The manufacturer guarantees full potency and safety only up to that date. After it: no guarantee — some drugs just get weaker, a few (like old tetracycline) can become harmful. When in doubt, don't take it — ask the pharmacist.
7. **If it looks/smells/feels wrong, don't take it.** Discoloration, crumbling, odd smell, cream turned runny — red flags. Ask the pharmacist; don't guess.
8. **How to get rid of old meds:** pharmacy take-back programs first. Never flush (water supply) and don't just toss in the trash — the fallback is mixing with something unappealing (coffee grounds, cat litter), sealing in a bag, then trashing. ([FDA/DEA guidance](https://www.mtpr.org/2017-02-06/when-old-medicine-goes-bad))

### C. "Take with food" — decoding label language

9. **"Take with food"** = take it during or right after a meal (or at least a snack). Purpose: protects your stomach, and for fat-soluble things (vitamin D) food *helps* absorption.
10. **"Take on an empty stomach"** = 1 hour before or 2 hours after eating. Purpose: food would block absorption (iron is the classic). A full glass of water, not milk or juice.
11. **"Take with a full glass of water"** = 8 oz / 240 mL, and stay upright a bit after — some pills irritate the esophagus otherwise.
12. **"Take at the same time each day"** vs **"take at bedtime"** vs **"take in the morning"** — these are different instructions with different reasons (steady blood levels vs. drowsiness timing vs. wakefulness). Follow the specific one on the label.

### D. The spacing maze (supplements and meds that fight each other)

13. **Iron's enemies:** tea, coffee, calcium/dairy, eggs, soy, antacids — keep 1–2 hours away. Vitamin C is iron's friend (helps absorption).
14. **Minerals compete:** calcium, magnesium, iron, and zinc all fight for the same absorption pathways. Don't take them in one handful; spread across the day (e.g., iron morning, magnesium evening).
15. **Antibiotics + minerals:** tetracyclines and fluoroquinolones get neutralized by calcium, magnesium, iron, zinc — 2 hours before or 4–6 hours after the mineral.
16. **Don't double-dose from overlap:** a multivitamin + a separate iron pill + a separate vitamin D can mean 2–3x of the same nutrient. Read all labels together once; show them to your pharmacist together.

### E. Missed doses, doubling, and "as needed"

17. **The universal missed-dose rule:** take it when you remember, unless it's close to the next dose — then skip. **Never double up** to make up for a missed dose (unless the specific label says to, e.g., Opill's make-up rule).
18. **One missed dose is rarely an emergency** (iron, vitamin D, multivitamin). The exceptions: drugs where *stopping* is dangerous (propranolol — never stop abruptly) and drugs where *timing* is the whole mechanism (Opill's 3-hour window).
19. **"Take as needed" (PRN) vs scheduled:** PRN means only when the symptom appears, at the stated minimum interval — not on a clock. Don't convert a PRN into a daily habit without asking.

### F. Reading the system (insurance, bills, labs)

20. **EOB anatomy:** the Explanation of Benefits is not a bill. Three numbers matter: what was billed, what your plan allowed, what you owe. If "what you owe" looks wrong, call the number on the EOB before paying.
21. **"In-network" isn't the whole story:** the facility can be in-network while the anesthesiologist/radiologist isn't. For planned procedures, ask "will everyone involved be in-network?" — and get the answer in writing if you can.
22. **You can contest bills.** Ask for an itemized bill, check for duplicates and services you didn't receive, and dispute in writing. Surprise balance bills for emergency or in-network-facility care are illegal under the No Surprises Act — report them at cms.gov/nosurprises or 1-800-985-3059.
23. **Reading a lab result:** the reference range is the "normal" band for the general population — one value slightly outside it is usually not a verdict. Trends over time beat single numbers. "High" or "low" flags describe the number, not a diagnosis. Bring questions to your doctor — that's what the flags are for.
24. **Prior auth in one paragraph:** your insurer can require approval *before* covering certain drugs/procedures. If denied: you can appeal, your doctor can do a "peer-to-peer" review, and denials have deadlines — don't let them sit.

### G. Myths and quiet mistakes

25. **"Natural" doesn't mean safe or dose-free.** Supplements aren't FDA-approved like drugs; "more" can mean liver strain, bleeding risk, or toxicity (vitamin D, iron, vitamin A). Treat supplements with the same respect as prescriptions.
26. **Grapefruit is the famous one, not the only one.** Grapefruit juice blocks the enzyme that clears many drugs (statins, some blood pressure meds) — levels can spike. It's the poster child for "food can be a drug interaction."
27. **Don't split or crush unless the label says you can.** Extended-release, enteric-coated, and capsule formulations are designed to release a certain way — crushing defeats the design. Scored tablets with a line down the middle are usually the splittable ones.
28. **Tell every doctor about everything** — prescriptions, OTCs, supplements, and alcohol use. "It's just a vitamin" has caused real interactions. The Meds tab's one canonical list exists for exactly this.
29. **Side effects vs. "just how the drug is":** new, severe, or scary symptoms after starting something → call your prescriber or pharmacist promptly. Mild, listed, expected effects (iron → dark stools; Opill → spotting) → note them, mention at the next visit, don't panic-stop the drug without asking.

## Card format (for the builders)

Each card in the app is a data object:

- `id` (stable slug), `topic` (A–G grouping), `title`, `body` (plain language, ≤120 words), `why_it_matters` (one line), `source` (reference), `reviewed_by` + `reviewed_date` (physician reviewer stamp), `trigger` (contextual trigger rule, if any), `dismissable: true`.
- Cards render in her visual language (dense but calm, tertiary palette) — art team's domain, not this spec's.
- Cards never contain dosing instructions for *her* specifically — general principles only. Personal dosing lives in the per-med wisdom cards and comes from her prescriber.

## Review and maintenance

- **Physician reviewer** approves every card before it ships; re-review annually or when guidance changes.
- Cards are versioned; the review stamp shows in the library so she can see it's current.
- New cards can be proposed from her actual questions — if she asks "wait, why can't I take iron with coffee?", that becomes (or updates) a card.

## Success looks like

She never has to Google "can I take X with Y" at midnight again — because the answer was already in the app, surfaced before she needed it, in language she didn't need a medical degree to read.
