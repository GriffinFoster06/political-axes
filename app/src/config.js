// Pilot settings. Edit this file (app/src/config.js), then rebuild: python3 scripts/build_app.py
window.QUIZ_CONFIG = {
  // Where finished responses are sent (POST, text/plain JSON). Leave empty to keep
  // answers on the device only (people can still copy or download them).
  // See server/README.md for a free Google Sheets endpoint.
  submitUrl: "",
  // "pilot": link block + 3 of 9 blocks (about 45 min). "full": every question.
  defaultMode: "pilot",
  allowFullMode: true,
};
