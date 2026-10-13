// Pilot settings. Edit this file (app/src/config.js), then rebuild: python3 scripts/build_app.py
window.QUIZ_CONFIG = {
  // Where finished responses are sent (POST, text/plain JSON). Leave empty to keep
  // answers on the device only (people can still copy or download them).
  // See server/README.md for a free Google Sheets endpoint.
  // "auto" = save to this site's own /api/submit endpoint (Netlify function) when hosted,
  // and keep answers on the device when opened as a local file.
  submitUrl: "auto",
  // "pilot": link block + 3 of 9 blocks (about 45 min). "full": every question.
  defaultMode: "quick",
  allowFullMode: true,
  // Pilot A experiments (preregistration section 12): background lines shown or hidden at
  // random, a "Torn" option on tradeoffs for half of people, top-tax question order.
  // Set to false for Pilot B and for the public version.
  experiments: true,
};
