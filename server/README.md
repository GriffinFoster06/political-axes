# Collecting pilot responses (free, about 10 minutes to set up)

The app is static files, so it needs somewhere to send finished responses.
The simplest free option is a Google Sheet with a small Apps Script.

## Set up

1. Create a new Google Sheet (use an account you control; consider a
   separate one for the project). Name it e.g. "Where You Stand pilot".
2. In the sheet: **Extensions → Apps Script**. Delete the sample code and
   paste in `google-apps-script.gs` from this folder. Save.
3. **Deploy → New deployment → Web app.**
   - Execute as: **Me**
   - Who has access: **Anyone**
   Copy the web app URL it gives you (ends in `/exec`).
4. Put that URL in `app/src/config.js` as `submitUrl` and rebuild
   (`python3 scripts/build_app.py`), or run the Pages workflow again.
5. Test: take the quiz once in full or pilot mode; a row should appear in a
   `responses` tab within a few seconds.

Each response is one row: date, random id, bank version, mode and the JSON
split over several cells. Results-page feedback ("How well does your result
describe your views?") arrives later as a row in a `feedback` tab with the
same id.

## Getting the data out

**File → Download → Comma-separated values** for the `responses` tab (and
`feedback`), save into `data/pilot/` (git-ignored, never committed), then:

```bash
python3 scripts/pilot_responses.py data/pilot/responses.csv
```

This writes `data/pilot/answers_long.csv` (one row per answer) and
`data/pilot/respondents.csv` (one row per person, with the quality flags and
the exclusion decision from `docs/preregistration.md` §3).

## Privacy

- The sheet never receives names, emails or IP addresses. Apps Script does
  not expose the sender's IP, and the app sends none.
- People under 18 are never submitted (the app checks the age answer).
- Keep the sheet private. Share it only with people analyzing the data.
- Don't commit raw responses to the public repo.

## Other hosts

Any endpoint that accepts a `POST` with a JSON body (sent as `text/plain`
to avoid CORS preflight) works: a Vercel/Netlify function writing to a
database, a Cloudflare Worker with D1, etc. The app doesn't read the
response, so the endpoint only has to store the body.
