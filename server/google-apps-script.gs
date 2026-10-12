/**
 * Free response collector for the pilot: a Google Apps Script web app that
 * appends each finished quiz to a Google Sheet. See server/README.md.
 *
 * Stores: the date (not the time), the random response id, the bank version,
 * the mode, and the JSON payload split into 45,000-character cells (Sheets
 * allows 50,000 per cell). Apps Script never sees the sender's IP address.
 */
var CHUNK = 45000;
var MAX_BODY = 400000;

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var body = (e && e.postData && e.postData.contents) || "";
    if (!body || body.length > MAX_BODY) return out({ ok: false, error: "empty or too large" });
    var data;
    try { data = JSON.parse(body); } catch (err) { return out({ ok: false, error: "not JSON" }); }
    if (!data.rid || typeof data.rid !== "string" || data.rid.length > 32) return out({ ok: false, error: "no id" });
    var name = data.feedback ? "feedback" : "responses";
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(name) || ss.insertSheet(name);
    if (sh.getLastRow() === 0) sh.appendRow(["date", "rid", "bank", "mode", "chunks", "payload_1", "payload_2", "payload_3", "payload_4", "payload_5", "payload_6", "payload_7", "payload_8", "payload_9"]);
    var chunks = [];
    for (var i = 0; i < body.length; i += CHUNK) chunks.push(body.slice(i, i + CHUNK));
    var row = [new Date().toISOString().slice(0, 10), data.rid, data.bank || "", data.mode || "", chunks.length].concat(chunks);
    sh.appendRow(row);
    return out({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return out({ ok: true, note: "Send finished quiz responses here with POST." });
}

function out(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
