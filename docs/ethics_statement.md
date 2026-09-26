# Ethical Data Collection Statement

**Project:** Colombo Stock Exchange — Web Data Collection
**Course:** DA 2009 — Data Collection Methods II, University of Colombo
**Group:** 25ada072 - Pasindu · 25ada073 - Sasini · 25ada141 - Salaama · 24ada076 - Nuhan
**Website:** https://www.cse.lk

---

## 1. What we collected

Everything we collect is public and visible to anyone without logging in:

- Share prices and daily trading figures for around 290 listed companies
- The market index (ASPI) and the sector indices
- Company details: price, market value, yearly high and low
- Company announcements and CSE circulars
- The PDF documents attached to those announcements

Every field describes a **company**, not a person. CSE publishes these figures
so that the public can read them.

### What we did not collect

- Anything behind a login, a paywall or a CAPTCHA
- Any personal information about any individual
- Anything in the `/cgi-bin/` section, which `robots.txt` asks bots to avoid

---

## 2. robots.txt

`robots.txt` is a file websites publish to tell automated programs which pages
they may visit. Following it is voluntary — we follow it because that is what
ethical scraping means.

We read it at the start of every run:

```
User-agent: *
Disallow:
Disallow: /cgi-bin/
Sitemap: https://www.cse.lk/sitemap.xml
```

- `User-agent: *` — the rules apply to every program, including ours
- `Disallow:` on its own means nothing is blocked by that line
- `Disallow: /cgi-bin/` blocks one section
- There is **no `Crawl-delay`**, so the site does not ask us to wait at all

We check every address against these rules before requesting it, using
Python's built-in `RobotFileParser`.

---

## 3. How we avoid overloading the server

The website does not ask us to slow down. We slow down anyway.

| What we do | Why |
|---|---|
| Wait 1.5 seconds between requests | Sending requests as fast as the computer can manage would put load on their server for no reason |
| Save a copy of every reply | So we never ask for the same thing twice |
| Use one `requests.Session` | Keeps the connection open instead of opening a new one each time |
| Download only the documents we need | There are far more PDFs on the site than we use |
| Stop on an error | If the server returns an error we report it, rather than requesting the same address again and again |

A full run of the app sends roughly 30 to 40 requests, spaced at least 1.5
seconds apart. Somebody browsing the same pages by hand would generate more
traffic than that, because each page load also fetches scripts, fonts and
images that we never request.

Every request is written to `logs/request_log.csv` with the time, the address,
the reply, and the delay we waited.

---

## 4. Saying who we are

Many scrapers copy a browser's User-Agent so they look like an ordinary
visitor. We do the opposite and say exactly who we are:

```
CSE-Academic-Scraper/1.0 (University of Colombo; DA 2009 group project;
contact: nuhanmalee@gmail.com)
```

If our requests ever caused a problem, the site administrator can see who sent
them and get in touch.

---

## 5. Using the addresses the website itself uses

The CSE website loads its data from addresses such as
`https://www.cse.lk/api/tradeSummary`. We found these by opening the site in a
browser and looking at the Network tab.

We think using them is the right choice for three reasons:

1. They need no login or key — it is the same request the page makes when
   anybody visits the site.
2. `robots.txt` does not ask us to avoid them.
3. It is **less work for their server**. Loading the whole page means CSE has
   to send the HTML, the JavaScript, the fonts and the images, and the browser
   then requests that same data address anyway. Reading it directly skips all
   of that.

---

## 6. Security controls

We do not get around any security measure.

- No logins or passwords
- No paywalls
- No CAPTCHAs

We never met a CAPTCHA on the CSE site, because we never behaved in a way that
would set one off. Being able to get past a control would not mean we were
allowed to.

---

## 7. Crediting the source

Every file we export contains, inside the file itself:

> Data source: Colombo Stock Exchange (https://www.cse.lk). Collected for
> academic purposes only - DA 2009, University of Colombo.

along with the date and time the data was collected. CSV files carry it as
comment lines at the top, Excel files as a second sheet named Source, and JSON
files in a details section above the records.

---

## 8. What we would do differently for anything beyond coursework

- We did not ask CSE for written permission. We relied on `robots.txt` and on
  the data being public, which is reasonable for a university assignment. For
  publishing or commercial use, written permission would be the correct next
  step.
- The data addresses are not officially documented, so CSE could change them
  at any time without telling anybody. That is their right.
- The data is a snapshot of one trading day, collected for an assignment. It
  is not redistributed, not sold, and not investment advice.
