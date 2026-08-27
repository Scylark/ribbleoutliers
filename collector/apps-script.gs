/**
 * Ribble Outliers microsite tracking collector. DEPLOYED AND LIVE.
 * Bound to the "Outliers site tracking" sheet (vicivelo@gmail.com).
 * Deployed as a web app: execute as me, access anyone.
 * The site's TRACK.beacon points at the /exec URL of this deployment.
 */
var SHEET_ID = '1LijHTxeVHLFvNoy3RQ7iiTzyWS7lXht0t1uH5wPcdzM';
function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    SpreadsheetApp.openById(SHEET_ID).getSheets()[0].appendRow([new Date(), d.p || '', d.ev || '', d.n || '', d.sid || '', d.ref || '']);
  } catch (err) {}
  return ContentService.createTextOutput('ok');
}
