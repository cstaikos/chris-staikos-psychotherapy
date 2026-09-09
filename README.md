# Chris Staikos Psychotherapy — Woodland

The selected Woodland design, now a six-page Jekyll website. Original olive colours and serif typography, with stronger cream, pale olive and deep green sections. The supplied headshot appears on Home and About, with local nature photography elsewhere.

## Local preview

```sh
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Open http://127.0.0.1:4000/. Keep the server running while reviewing. If dependencies are absent, run `bundle install` first.

Pages: `/`, `/about/`, `/breathwork/`, `/psychedelic-support/`, `/faq/`, `/contact/`.

The other nine prototypes and review gallery have been removed. Woodland now lives at the site root.

## Editing and adding pages

- `_data/content.yml`: biography, credentials, focus areas, FAQs and contact links.
- `_data/navigation.yml`: navigation labels and page paths. Add an entry here to put a new page in the main menu.
- `_layouts/site.html`: common page shell.
- `_includes/home.html`: home page introduction and onward links.
- `_includes/`: content sections for each page.
- `assets/site.css`: Woodland design and responsive layouts.
- `assets/site.js`: mobile menu and email reveal.

The focus areas are a modest list on About and explicitly non-exhaustive. Extend the `focus` list in `_data/content.yml` as needed.

To add a page, create a directory with `index.html`, using the existing pages’ front matter as a starting point. Add its content include and matching case to `_layouts/site.html`, then add a navigation entry if appropriate. Assets and navigation use Jekyll’s `relative_url` filter for GitHub Pages project paths.

## Validation

```sh
bundle exec jekyll build
python3 scripts/check_site.py
```

Checks six pages, internal routes, assets, anchors, single H1s, language, descriptions, preview noindex tags, essential draft content, and absence of private client notes and old prototype navigation. Update the expected page count when adding pages.

GitHub Pages project-path check:

```sh
bundle exec jekyll build --baseurl /new-website --destination tmp/baseurl
python3 scripts/check_site.py tmp/baseurl /new-website
```

These are build/source checks, not browser screenshot or interaction tests.

## Publishing later

Set `_config.yml` `url` to the final HTTPS origin and `baseurl` to the repository path (empty for a custom domain or user site). Confirm the draft content and replace or approve the nature photographs. Remove the preview `noindex, nofollow` tag from `_layouts/site.html` and add canonical URLs and a sitemap when the domain is known. The site has static HTML content, semantic headings and navigation, descriptive page metadata, and no custom Jekyll plugins. It remains local and unindexed during review.

## Content and photography

The supplied PDF is the content source. Private ideal-client notes are excluded. The qualifying credential, breathwork readiness and integration details, actual booking link, and email-reveal behaviour are retained. No fees, office address, consultation duration, or clinical outcomes were invented. Psychedelic support uses the existing FAQ; the draft's passing legal statement about the Special Access Program remains omitted pending verification.

`assets/images/chris-staikos.jpg` is copied from the supplied headshot, unchanged. CSS controls its displayed shape.

Placeholder nature photos:

- Forest: https://images.unsplash.com/photo-1448375240586-882707db888b
- Shoreline: https://images.unsplash.com/photo-1475924156734-496f6cac6ec1
- Sunlit woodland: https://images.unsplash.com/photo-1441974231531-c6227db76b6e

These illustrate atmosphere, not a promised practice location. Email reveal reduces casual scraping but is not a security boundary.
