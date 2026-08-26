# Ribble Outliers 2027, partner microsite

A single-page partner pitch for the 2027 season, hosted on GitHub Pages with per-prospect link tracking.

## Going live, two steps

1. **Upload the images.** On this repo page click Add file -> Upload files, and drag the `img` folder in (it lives in the Ribble Cycles/Microsite folder). Commit to main.
2. **Turn on Pages.** Settings -> Pages -> Deploy from a branch -> `main`, folder `/ (root)`. Save. The site appears at `https://scylark.github.io/ribbleoutliers/` within a minute or two.

## Tracking

Every outreach email uses a minted link from `links.csv`, for example `?p=mucoff`. The page logs open, read time (10-second heartbeats), scroll depth, and clicks on the contact button.

To collect the data, follow the setup notes in `collector/apps-script.gs`. It writes every event to a Google Sheet you own. Once deployed, set `TRACK.beacon` in `index.html` to the web app URL. A GA4 property can be added later by setting `TRACK.ga4`.

Read time per visit is the highest heartbeat count for a session multiplied by ten seconds.

## Notes

- The page carries `noindex`, so search engines stay away while outreach runs.
- Pricing on the page matches the partner deck. Edit the tier cards in `index.html` to change it.
- Contact routes to partnerships@ribble.com.
