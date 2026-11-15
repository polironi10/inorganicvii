# inorganicvii

Static multi-page notes site for Cloudflare Pages.
Production URL: https://inorganicvii.pages.dev

## Structure

- `index.html`, chapter list (4 syllabus chapters)
- `chapters/04-solids/`, 6 section pages, transcribed from the 23-page PDF
- `chapters/01-bonding-quantum/`, `02-elements-coordination/`, `03-organometallic/`, upload soon
- `sources.html`, verification log and syllabus coverage
- `assets/style.css`, site theme

## Deploy to Cloudflare Pages

```bash
cd inorganicvii
npx wrangler login
npx wrangler pages deploy . --project-name inorganicvii
```

First time only: `npx wrangler pages project create inorganicvii --production-branch main`

Or in the dashboard: Workers and Pages, then Create, then Pages, then Upload assets, then upload this folder, project name `inorganicvii`.

No build step. No server code.
