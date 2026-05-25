import os
from flask import Flask, render_template, Response, request, redirect

app = Flask(__name__)

SITE_DOMAIN    = os.environ.get('SITE_DOMAIN', 'gi.riseforafrica.no')
SITE_URL       = f'https://{SITE_DOMAIN}'
GOFUNDME_URL   = "https://www.gofundme.com/f/support-vulnerable-children-through-education-in-burundi"

RAISED_NOK         = 9_358
GOAL_NOK           = 1_000_000
DONORS             = 16
COST_PER_CHILD     = 1_050
CHILDREN_GOAL      = 1_000
CHILDREN_LAST_YEAR = 800
CHILDREN_FUNDED    = max(1, int(RAISED_NOK / COST_PER_CHILD))
PROGRESS_PCT       = round(RAISED_NOK / GOAL_NOK * 100, 1)


def _vars(lang='nb'):
    sep = ' ' if lang == 'nb' else ','
    return dict(
        gofundme_url=GOFUNDME_URL,
        site_url=SITE_URL,
        raised_nok=f"{RAISED_NOK:,}".replace(',', sep),
        goal_nok=f"{GOAL_NOK:,}".replace(',', sep),
        donors=DONORS,
        children_funded=CHILDREN_FUNDED,
        children_goal=CHILDREN_GOAL,
        children_last_year=CHILDREN_LAST_YEAR,
        progress_pct=PROGRESS_PCT,
        cost_per_child=f"{COST_PER_CHILD:,}".replace(',', sep),
        locale='nb-NO' if lang == 'nb' else 'en-US',
    )


@app.before_request
def canonical_www():
    host = request.host.split(':')[0]
    if host == f'www.{SITE_DOMAIN}':
        return redirect(SITE_URL + request.full_path.rstrip('?'), 301)


@app.route('/robots.txt')
def robots_txt():
    return Response(
        f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n',
        mimetype='text/plain'
    )


@app.route('/sitemap.xml')
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}/</loc><lastmod>2026-05-25</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>{SITE_URL}/en/</loc><lastmod>2026-05-25</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
</urlset>"""
    return Response(xml, mimetype='application/xml')


@app.route('/')
def index():
    return render_template('index.html', **_vars('nb'))


@app.route('/en/')
@app.route('/en')
def index_en():
    return render_template('index_en.html', **_vars('en'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
