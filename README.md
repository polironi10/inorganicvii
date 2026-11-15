# inorganicvii

Static multi-page notes site for Cloudflare Pages.
Production URL: https://inorganicvii.pages.dev

## Structure

- `index.html` — chapter list
- `chapters/01-solid-state/` — 14 topic pages, transcribed from the 23-page PDF
- `chapters/02-…/06-…/` — planned chapters, awaiting notes
- `sources.html` — verification log
- `assets/style.css` — Hallmark Almanac theme

## Deploy to Cloudflare Pages

```bash
cd inorganicvii
npx wrangler login
npx wrangler pages deploy . --project-name inorganicvii
```

First time only: `npx wrangler pages project create inorganicvii --production-branch main`

Or in the dashboard: Workers & Pages → Create → Pages → Upload assets → upload this folder, project name `inorganicvii`.

No build step. No server code.
