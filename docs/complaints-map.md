# Complaints map — why holistic care feels broken, and the Heliotrope feature that fixes each one

*Phase 1 research, healthcare-complaints team. Each complaint is grounded in real survey/statistical sources, then mapped to a specific Heliotrope tab. The point of this doc: if a feature can't trace back to a real frustration people actually report, it doesn't belong in the build.*

Feature tabs referenced: **Today, Body, Meds, Labs, Care team, To-dos, Nourish, Cycle/Stress/Skin/Weight, Mind, Orders, Reports**.

---

## 1. Records scattered across five portals and three phone apps

**The complaint.** Federal data: in 2024, 59% of US patients had medical records spread across multiple portals, up from 50% in 2022 — yet only 7% used any app that pulls them together in one place ([healthcarebusinesstoday.com](https://www.healthcarebusinesstoday.com/patient-portals-digital-health-fragmentation/)). The GAO found patients' #1 frustration with accessing records is wasted time: setting up portal after portal, each with its own password, just to prepare for one appointment ([fiercehealthcare.com](https://www.fiercehealthcare.com/ehr/gao-patients-often-frustrated-when-seeking-health-records)). Only 59% of consumers say they've *always* been successful getting their requested records at all ([fortherecordmag.com](https://www.fortherecordmag.com/news/012320_news.shtml)).

**The Heliotrope fix → Labs + Reports + Care team.** Labs becomes the one library where every result lands, regardless of which portal it came from, with trend views across providers. Reports turns that library into a one-tap doctor-ready packet — the patient stops being the human fax machine. Care team records *which* portal belongs to *which* doctor so there's no archaeology next time.

## 2. Referrals that vanish into the void

**The complaint.** Up to 20% of referred patients never show up for their specialty appointment — no cancellation, no decline, they just fall through the handoff cracks ([medium.com](https://medium.com/@healthcare_operations/the-referral-leakage-problem-why-specialty-practices-lose-20-of-referred-patients-ca94a9c1c75b)). 76% of health organizations estimate more than 10% of referrals never become completed appointments ([Documo/bizwire](https://business.theantlersamerican.com/theantlersamerican/article/bizwire-2026-9-9-nearly-half-of-healthcare-organizations-say-document-delays-frequently-affect-patient-care-new-survey-finds)). Patients 18–44 are 40% less likely to follow through, largely for logistical reasons. A referral without follow-up tracking is a piece of paper thrown into a storm.

**The Heliotrope fix → To-dos + Care team.** A referral becomes a tracked to-do the moment it's issued: who referred, to whom, referral number, "call to schedule by X date" — with reminders. Care team holds the specialist's actual booking info (not "call this hospital and figure it out yourself"). Status visible at a glance: sent → scheduled → seen.

## 3. The prior-authorization maze

**The complaint.** KFF's Feb 2026 tracking poll: prior authorization is the single biggest burden insured Americans face beyond costs — 34% name it the #1 burden, and 47% had a service or medication denied or delayed by their insurer in two years ([beckershospitalreview.com](https://www.beckershospitalreview.com/finance/one-third-of-insured-adults-say-prior-auth-major-burden-in-accessing-care-kff/)). Among those who experienced a denial/delay, a third say it harmed their mental health or finances and a quarter say it harmed their physical health. 95% of physicians say prior auth delays necessary care; 79% say patients abandon treatment over it ([financialcontent.com](https://markets.financialcontent.com/1discountbrokerage/article/gnwcq-2026-5-13-ama-survey-prior-authorization-reform-pledge-falls-short-with-physicians)). KFF's claims analysis: insurers denied at least 1 in 8 standard requests in 2025 ([beckerspayer.com](https://www.beckerspayer.com/policy-updates/unitedhealthcare-to-drop-prior-authorization-requirements-for-1700-services/)).

**The Heliotrope fix → To-dos + Care team.** Every prior-auth becomes a to-do with the denial letter, the appeal deadline, and the phone tree that actually works — plus a template for what to say ("my doctor prescribed X on [date], here's the denial reason"). Care team renders the insurance card beautifully so the member ID and prior-auth phone number are one tap away at the pharmacy counter or on a call with the insurer. Nothing about an appeal lives only in someone's memory anymore.

## 4. Surprise billing — the bill you didn't know was coming

**The complaint.** 1 in 10 insured adults got a surprise out-of-network bill in a 12-month period, with an average estimated balance bill of $623 ([arnoldventures.org](https://assets.arnoldventures.org/uploads/AV-Surprise-Biling-Fact-Sheet.pdf)). Roughly 1 in 5 Americans still receives surprise bills despite the No Surprises Act — some providers keep sending now-illegal bills ([pirg.org](https://pirg.org/michigan/updates/update-americans-are-still-getting-surprise-medical-bills-despite-new-protections/?pg=4)). Before the NSA, ~20% of privately insured elective surgeries at in-network hospitals produced surprise bills from out-of-network providers ([californiahealthline.org](https://californiahealthline.org/news/article/surprise-medical-bills-federal-no-surprises-act-california-law/view/republish/)). Understanding medical bills is itself a top burden (60% of insured adults, KFF).

**The Heliotrope fix → Care team + To-dos + Orders.** Care team holds the insurance card (in-network vs out, deductible status, the number to call when a bill looks wrong). Orders can catch EOBs and bills auto-detected from the inbox. To-dos tracks bill disputes the same way as referrals — what was billed, what the plan says, the dispute deadline. And the *unknown-unknowns* teaching surface (see `unknown-unknowns.md`) proactively teaches: what an EOB is, what balance billing is, and that you can contest it.

## 5. No shared medication list — every doctor starts from zero

**The complaint.** Medication discrepancies occur in up to 70% of patients at hospital admission or discharge ([leapfroggroup.org](https://ratings.leapfroggroup.org/sites/default/files/inline-files/2021%20Medication%20Reconciliation%20Fact%20Sheet.pdf)). ~15% of adverse medication events trace back to reconciliation failures at care handoffs ([todayshospitalist.com](https://todayshospitalist.com/To-prevent-drug-errors-try-medication-reconciliation/)). The #1 barrier hospitals cite: *patients don't know their own medications* (87% of respondents) ([todayshospitalist.com](https://todayshospitalist.com/Medication-reconciliation-hurdles-one-hospitals-experience/)). Every new doctor visit starts with the same interrogation — "so what are you taking?" — and the answer is always incomplete.

**The Heliotrope fix → Meds + Reports.** Meds is the one canonical list: every med, dose, schedule, with a photo of the bottle. Reports puts that list on every doctor visit summary automatically. The interaction scanner flags conflicts across the *whole* list — not just what one prescriber knows about. She never has to reconstruct her med list from memory in a waiting room again.

## 6. Lab results patients receive but can't read

**The complaint.** A JAMA Network Open study (Aug 2026, ~175M US adults weighted): 68.6% of patients view test results in a portal *before* hearing from any clinician — and a meaningful slice don't understand what they're reading ([medicaleconomics.com](https://www.medicaleconomics.com/view/most-patients-view-test-results-before-hearing-from-a-physician)). In a JMIR study, 67% of patients were confused by some aspect of their lab results; of the confused, 61% said technical jargon and abbreviations were the worst part ([jmir.org](https://www.jmir.org/2020/12/e18725/PDF)). "Health systems give you your data, but that does not mean that they put a lot of effort into making the information easy to understand on your own" — coauthor José Pagán, NYU.

**The Heliotrope fix → Labs + Body.** Labs translates: plain-language summaries of each panel, trend lines instead of single numbers, reference ranges in context ("here's what the number means, and what to ask your doctor"). Body links symptoms to systems so a low iron-saturation value stops being a floating number and can be tracked alongside fatigue — logged together for her to bring to a doctor, never explained by the app. The teaching surface explains what reference ranges are and why one abnormal value isn't a verdict.

## 7. Appointment logistics — the phone gauntlet

**The complaint.** The AMN Healthcare 2025 survey: average new-patient wait time across six major specialties hit **31 days**, the highest since the survey began in 2004 ([healthleadersmedia.com](https://www.healthleadersmedia.com/cmo/survey-physician-wait-times-surge-19-2022)). 34% of patients report difficulty scheduling within a reasonable timeframe; 23% of calls to medical practices go unanswered; average hold time 4:22, long enough that 28% hang up ([MGMA/Accenture via quickvoice](https://github.com/sohampawar1866/quickvoice/blob/HEAD/apps/web/content/blog/ai-medical-scheduling-voice-agents.md)). 41% of patients would switch providers for easier scheduling ([Accenture](https://github.com/sohampawar1866/quickvoice/blob/HEAD/apps/web/content/blog/ai-medical-scheduling-voice-agents.md)). Meanwhile 44% of patients delay care partly because of costs and time away from work ([techtarget.com](https://www.techtarget.com/patientengagement/news/366584422/Patients-Overburdened-with-Care-Coordination-Hurts-Patient-Experience?vgnextfmt=print)).

**The Heliotrope fix → To-dos + Care team + Today.** Finding a doctor is the to-do list: the search, the call, the callback, the first appointment — tracked with notes ("called Monday, they said call back Thursday, ask for Dr. X"). Care team stores the working phone numbers and portal links per doctor so rebooking doesn't restart from zero. Today surfaces what's coming up so nothing gets missed in the 31-day gap between booking and sitting in the chair.

## 8. "Nobody told me how to store my pills" — the counseling gap

**The complaint.** ~50% of patients don't take medications as prescribed ([drugtopics.com](https://www.drugtopics.com/view/rethinking-medication-adherence-patient-centered-solutions-for-better-outcomes)). 30% don't even fill the first prescription. The NCPA's national report card gave Americans a C+ on adherence; one in seven earned an F ([ncpa.co](https://www.ncpa.co/adherence/AdherenceReportCard_Full.pdf?ref=chaindrugreview.com)). 93% of pharmacists believe patients don't grasp the impact of non-adherence ([pharmacymagazine.co.uk](https://www.pharmacymagazine.co.uk/news/patients-failing-to-grasp-impact-of-non-adherence)). And nobody teaches the practical stuff: storage, expiry, food interactions. The bathroom "medicine cabinet" is the classic mistake — heat and humidity degrade pills fast ([NPR/mtpr.org](https://www.mtpr.org/2017-02-06/when-old-medicine-goes-bad)).

**The Heliotrope fix → Meds + Today.** Every med gets a plain-language wisdom card (see `docs/med-wisdom/`): what it's for, how/when to take it, spacing rules, storage (temperature, moisture, light, original container, travel), what to avoid, missed-dose guidance. Today shows what's due *now* so the schedule survives a chaotic day. The unknown-unknowns surface teaches the general principles once, so each new med's card is review, not discovery.

## 9. Doctors who don't talk to each other — and the patient is the messenger

**The complaint.** A national survey of adults 65+: 38% reported gaps in care coordination in the past year; those gaps carried 55% greater adjusted odds of a preventable bad outcome ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7728843/)). 64% of patients wish their providers took more time to understand them; 49% don't always feel listened to; 54% say their health would improve if providers helped them understand the healthcare system ([techtarget.com](https://www.techtarget.com/patientengagement/news/366584422/Patients-Overburdened-with-Care-Coordination-Hurts-Patient-Experience?vgnextfmt=print)). 61% of patients only access care when they're sick — preventive care quietly dies ([techtarget.com](https://www.techtarget.com/patientengagement/news/366584422/Patients-Overburdened-with-Care-Coordination-Hurts-Patient-Experience?vgnextfmt=print)).

**The Heliotrope fix → Reports + Body + Mind.** Reports generates the visit packet: meds, labs, symptoms, questions — the 10-minute visit becomes productive instead of a reconstruction exercise. Body keeps per-system notes so "the dizziness, the jaw tension, the brain fog" arrive at the appointment as a coherent story, not three forgotten mentions. Mind tracks patterns she can show a clinician ("here's what the last month looked like"), framed as her data, not a diagnosis.

## 10. Preventive care and the stuff nobody schedules for you

**The complaint.** 61% only access care when sick; 44% are actively delaying care ([techtarget.com](https://www.techtarget.com/patientengagement/news/366584422/Patients-Overburdened-with-Care-Coordination-Hurts-Patient-Experience?vgnextfmt=print)). Nobody's office calls *you* to say you're due for the thing you didn't know existed. Patients don't know what they don't know — and the system has no incentive to tell them.

**The Heliotrope fix → To-dos + Cycle/Stress/Skin/Weight + Nourish.** To-dos holds the find-a-doctor list and preventive checklist (the to-find list: endocrinologist, cardiologist, new PCP, optometrist, dentist…), prioritized, with notes. The body-upkeep tabs make maintenance a habit surface rather than a crisis response. The unknown-unknowns surface proactively teaches what to ask for at what age — the stuff she said she doesn't know to ask.

## 11. Cost opacity — bills in a foreign language

**The complaint.** Understanding medical bills burdens 60% of insured adults (KFF). Bills arrive coded, itemized in jargon, and disconnected from what insurance actually paid. (Folded into complaint #4's stats; the pain point is comprehension, not just surprise.)

**The Heliotrope fix → Orders + To-dos + the teaching surface.** Orders can ingest EOBs from the inbox; To-dos tracks each bill's dispute/payment; the teaching surface decodes EOB anatomy (billed amount vs. allowed amount vs. your responsibility) and the "call and ask for an itemized bill" move.

---

## What this means for the build

- **Every tab in the feature map earns its place from a complaint above.** Nothing here is speculative — it's the inverse of documented, measured patient frustration.
- The *wisdom cards* (`docs/med-wisdom/`) and the *unknown-unknowns surface* (`docs/unknown-unknowns.md`) are not nice-to-haves: they answer complaint #8 directly, which is the one she asked for by name ("I'm not a doctor, I don't know all the things I even need to know").
- The interaction scanner + alcohol check (architecture team's scope) extend complaint #5: the med list is only as good as the conflict detection across it.
- Sources are linked inline; where stats carry a date, it's noted. Numbers are 2024–2026.
