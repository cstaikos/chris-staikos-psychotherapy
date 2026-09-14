# Chris Staikos Psychotherapy — Woodland

The selected Woodland design, now a seven-page Jekyll website. Original olive colours and serif typography, with stronger cream, pale olive and deep green sections. The supplied headshot appears on Home and About, with local nature photography elsewhere.

## Local preview

```sh
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Open http://127.0.0.1:4000/. Keep the server running while reviewing. If dependencies are absent, run `bundle install` first.

Pages: `/`, `/about/`, `/psychotherapy/`, `/breathwork/`, `/psychedelic-support/`, `/faq/`, `/contact/`.

The other nine prototypes and review gallery have been removed. Woodland now lives at the site root.

## Editing and adding pages

- `_data/content.yml`: biography, credentials, focus areas, FAQs and contact links.
- `_data/navigation.yml`: navigation labels and page paths. Add an entry here to put a new page in the main menu.
- `_layouts/site.html`: common page shell.
- `_includes/home.html`: home page introduction and onward links.
- `_includes/`: content sections for each page.
- `assets/site.css`: Woodland design and responsive layouts.
- `assets/site.js`: mobile menu and email reveal.

Psychotherapy uses `_data/psychotherapy.yml` for its opening `approach` paragraph and ordered `focus` sections. Each section has a `title` and `description`; Markdown and paragraphs are supported. The opening paragraph sits in the page body, followed by spacious sections for each topic.

To add a page, create a directory with `index.html`, using the existing pages’ front matter as a starting point. Add its content include and matching case to `_layouts/site.html`, then add a navigation entry if appropriate. Assets and navigation use Jekyll’s `relative_url` filter for GitHub Pages project paths.

## Validation

```sh
bundle exec jekyll build
python3 scripts/check_site.py
```

Checks seven pages, internal routes, assets, anchors, single H1s, language, descriptions, preview noindex tags, essential draft content, and absence of private client notes and old prototype navigation. Update the expected page count when adding pages.

GitHub Pages project-path check:

```sh
bundle exec jekyll build --baseurl /new-website --destination tmp/baseurl
python3 scripts/check_site.py tmp/baseurl /new-website
```

These are build/source checks, not browser screenshot or interaction tests.

## SEO and search-console setup

`_includes/seo.html` supplies page titles, descriptions, canonical URLs, robots directives, Google/Bing ownership verification tags, Open Graph/X text metadata, and JSON-LD for the website, pages and Chris. No address, reviews, or additional professional claims are invented. `sitemap.xml` includes all indexable pages using the site layout and updates when pages are added. `robots.txt` advertises it on production builds.

Before publishing, set these fields in `_config.yml`:

- `url`: final HTTPS origin, without a trailing slash (e.g. `https://example.org`).
- `baseurl`: repository path such as `/new-website`, or empty for a custom domain/user site.
- `search_indexing`: `true` when the public site is ready to be indexed.
- `google_site_verification`: only the content value from Google's verification tag.
- `bing_site_verification`: only the content value from Bing's `msvalidate.01` tag.

Use `JEKYLL_ENV=production bundle exec jekyll build` for deployment. GitHub Pages sets the production environment for its native Jekyll build. Indexing requires all three: production environment, a configured HTTPS URL, and `search_indexing: true`. Local development stays noindex, omits public canonical/structured URLs, and produces an empty sitemap. Crawling stays allowed so search engines can read the noindex directive. Per-page `noindex: true` also removes that page from the sitemap; `sitemap: false` only excludes its sitemap entry.

For Google, add a **URL-prefix property** matching the public site URL, select HTML tag verification, and paste the token into configuration. A **Domain property** uses DNS verification instead. For Bing, use its HTML meta tag method or import a verified Google Search Console site. Deploy the configured tokens before clicking Verify. Keep the tokens configured after verification. Then submit the public `sitemap.xml` URL to both services. On a GitHub project site, sitemap and canonical paths include the repository path; robots.txt is only authoritative at the host root, so submit the sitemap directly when you cannot control that root.

No search-console account has been connected and no site has been submitted automatically. The tokens are public ownership-verification values, not passwords.

Official setup references:

- [Google ownership verification](https://support.google.com/webmasters/answer/9008080?hl=en)
- [Bing site verification](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b)
- [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

### SEO validation

Run the regular preview build/check above, then create `tmp/seo-production.yml` with a test HTTPS origin, base path, `search_indexing: true`, and test tokens:

```yaml
url: https://example.org
baseurl: /practice
search_indexing: true
google_site_verification: test-google-token
bing_site_verification: test-bing-token
```

```sh
JEKYLL_ENV=production bundle exec jekyll build --config _config.yml,tmp/seo-production.yml --destination tmp/seo-production
python3 scripts/check_seo.py
```

Test configuration/output stays under excluded `tmp/` and is never part of the public site. The checks cover preview behaviour, production tags, JSON syntax, canonical/base paths, sitemap entries and robots.txt. Restart `jekyll serve` after editing configuration so it reloads the settings.

## Content and photography

The supplied PDF is the content source. Private ideal-client notes are excluded. The qualifying credential, breathwork readiness and integration details, actual booking link, and email-reveal behaviour are retained. No fees, office address, consultation duration, or clinical outcomes were invented. Psychedelic support uses the existing FAQ; the draft's passing legal statement about the Special Access Program remains omitted pending verification.

`assets/images/chris-staikos.jpg` is copied from the supplied headshot, unchanged. CSS controls its displayed shape.

Placeholder nature photos:

- Forest: https://images.unsplash.com/photo-1448375240586-882707db888b
- Shoreline: https://images.unsplash.com/photo-1475924156734-496f6cac6ec1
- Sunlit woodland: https://images.unsplash.com/photo-1441974231531-c6227db76b6e

These illustrate atmosphere, not a promised practice location. Email reveal reduces casual scraping but is not a security boundary.

Additional banner photography (Unsplash):

- About: [Antje Winkler — sunlit forest path](https://unsplash.com/photos/a-shaded-forest-path-bathed-in-sunlight-8cH5aFnggnk), saved as `assets/images/woodland-path.jpg`.
- FAQs: [Luke Ellis-Craven — green fern](https://unsplash.com/photos/green-fern-plant-G-S8UGXf_NE), saved as `assets/images/ferns.jpg`.
