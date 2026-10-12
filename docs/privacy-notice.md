# Privacy notice and consent (shown before the quiz starts)

**About this quiz.** This is a personal, non-commercial project by Griffin
Foster. It isn't affiliated with any university, company, party or campaign.

**What's collected.** Your answers, optional broad demographics (age range,
region, education), and how long each question took. No name, email or IP
address is collected. Political opinions are sensitive, so the quiz is built
to be anonymous.

**How it's used.** To show your results and, in aggregate, to improve the
quiz. Anonymized aggregate data may be published.

**Your choices.** You can skip any question and stop at any time. At the end
you get a deletion code; send it to [contact] to have your answers removed.

**Risks.** Minimal. Your results are statistical estimates with uncertainty,
not judgments about you.

**Who can take it.** Adults 18 and older in the United States.

☐ I'm 18 or older, in the US, and I agree.

---

## Engineering checklist behind this notice

- [ ] No accounts; no email unless someone opts into a retest, stored in a
      separate table and deleted after the retest.
- [ ] No IP addresses stored. Rate limiting uses a salted hash with a
      rotating salt, kept in memory only.
- [ ] Cookieless analytics, or none.
- [ ] Coarse demographics only; party questions optional and asked last.
- [ ] Postgres row-level security, TLS, a content security policy,
      dependency alerts.
- [ ] Raw responses kept 24 months; published extracts must have at least
      10 people in every combination of reported demographics.
- [ ] Deletion code shown at the end of the quiz and honored.
