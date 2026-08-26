/**
 * Ribble Outliers microsite tracking collector.
 * Logs every event to a Google Sheet: open, heartbeats (read time), scroll depth, CTA clicks.
 *
 * Setup (10 minutes):
 * 1. Create a new Google Sheet. Name the first tab "log".
 * 2. Extensions -> Apps Script. Delete the sample code, paste this file.
 * 3. Deploy -> New deployment -> Web app.
 *      Execute as: Me. Who has access: Anyone.
 * 4. Copy the web app URL.
 * 5. In index.html set TRACK.beacon to that URL and push the change.
 *
 * Read time per visit = highest "hb" count x 10 seconds.
 * The prospect code is the ?p= value from the minted link.
 */
function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('log');
    ss.appendRow([new Date(), d.p || '', d.ev || '', d.n || '', d.sid || '', d.ref || '']);
  } catch (err) {}
  return ContentService.createTextOutput('ok');
}
