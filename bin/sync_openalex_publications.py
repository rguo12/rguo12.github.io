#!/usr/bin/env python
"""Complete _bibliography/papers.bib using OpenAlex (no rate limiting, unlike Google Scholar)
and tag every entry as `pubtype = {published}` or `pubtype = {preprint}`.

The Publications page uses `pubtype` to show "Published" and "Preprints" sections.

  * New works (matched by normalized title) are appended below the AUTO marker.
  * If a paper exists both as an arXiv preprint and as a published version, only the
    published version is kept/added.
  * Existing entries are never rewritten, except: `pubtype` is added when missing, and an
    entry whose venue says "arXiv" but which OpenAlex knows as a published paper gets its
    venue replaced by the real one.
"""

import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

import yaml

BIB_FILE = "_bibliography/papers.bib"
SOCIALS_FILE = "_data/socials.yml"
MARKER = "% --- Added automatically from Google Scholar / OpenAlex (edit freely) ---"
PREPRINT_VENUE = re.compile(r"arxiv|preprint|openreview|ssrn|researchgate|biorxiv|techrxiv", re.I)
PUBLISHED_VENUE = re.compile(
    r"conference|proceedings|workshop|symposium|journal|transactions|letters|acm|ieee|"
    r"neurips|icml|iclr|kdd|sigir|www|wsdm|cikm|aaai|ijcai|acl|emnlp|naacl|recsys|sdm|icdm|"
    r"advances in neural|magazine|review",
    re.I,
)


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"[{}]", "", t).lower()).strip()


def esc(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def fetch_works(orcid: str, name: str):
    # Plain page= paging needs no API key (cursor= paging past page 1 now does).
    works, page = [], 1
    sel = "id,title,publication_year,type,primary_location,locations,doi,authorships,biblio"
    while True:
        q = urllib.parse.urlencode({
            "filter": f"author.orcid:{orcid}", "per-page": 100, "page": page, "select": sel,
        })
        with urllib.request.urlopen(f"https://api.openalex.org/works?{q}", timeout=60) as r:
            d = json.load(r)
        works += d["results"]
        if not d["results"] or len(works) >= d["meta"]["count"]:
            break
        page += 1
    last = name.split()[-1].lower()
    # keep only works where an author really is us (guards against ORCID mis-assignments)
    def junk(w):
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        return (w["publication_year"] or 0) < 2013 or "SpringerBriefs" in src

    return [w for w in works if w.get("title") and not junk(w) and any(
        name.lower() == (a["author"].get("display_name") or "").lower()
        or orcid in (a["author"].get("orcid") or "") for a in w["authorships"])]


def classify(w: dict) -> tuple:
    """-> (pubtype, venue)"""
    locs = [w["primary_location"]] + (w.get("locations") or []) if w.get("primary_location") else (w.get("locations") or [])
    venues = [(l.get("source") or {}).get("display_name") or "" for l in locs if l]
    stypes = [(l.get("source") or {}).get("type") for l in locs if l and l.get("source")]
    real = [v for v, t in zip(venues, stypes) if t in ("journal", "conference", "book series", "ebook platform")
            and not PREPRINT_VENUE.search(v)]
    if w["type"] == "preprint" and not real:
        return "preprint", "arXiv preprint"
    if real:
        return "published", real[0]
    if w["type"] in ("conference-paper", "article", "book-chapter", "book") and not (
            venues and PREPRINT_VENUE.search(venues[0])):
        return "published", venues[0] if venues else ""
    return "preprint", "arXiv preprint"


STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "via", "to", "from", "by", "using"}


def toks(t: str) -> set:
    return {w for w in t.split() if w not in STOP}


def same_paper(t1: str, y1, t2: str, y2) -> bool:
    a, b = toks(t1), toks(t2)
    if not a or not b:
        return False
    inter = len(a & b)
    jac, cont = inter / len(a | b), inter / min(len(a), len(b))
    return (jac >= 0.7 and cont >= 0.85) or (cont == 1 and y1 == y2 and min(len(a), len(b)) >= 3)


def find_dup(t, y, pool):
    """pool: iterable of (title, year); returns True if (t, y) duplicates one of them."""
    return any(same_paper(t, y, t2, y2) for t2, y2 in pool)


def heuristic(block: str) -> str:
    m = re.search(r"(?:journal|booktitle)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", block, re.S)
    v = m.group(1) if m else ""
    if PREPRINT_VENUE.search(v) or (not v and "arxiv" in block.lower()):
        return "preprint"
    return "published" if v else "preprint"


def spans(text: str):
    ms = list(re.finditer(r"^@\w+\{[^,]+,", text, re.M))
    for i, m in enumerate(ms):
        yield m.start(), (ms[i + 1].start() if i + 1 < len(ms) else len(text))


def title_of(block: str):
    t = re.search(r"title\s*=\s*[{\"](.+?)[}\"],?\s*\n", block, re.S)
    return norm(t.group(1)) if t else None


def entry(w: dict, ptype: str, venue: str, used: set) -> str:
    authors = " and ".join(a["author"]["display_name"] for a in w["authorships"])
    first = norm(w["authorships"][0]["author"]["display_name"]).split()[-1]
    word = next((x for x in norm(w["title"]).split() if len(x) > 3), "paper")
    key = base = f"{first}{w['publication_year']}{word}"
    i = 2
    while key in used:
        key, i = f"{base}{i}", i + 1
    used.add(key)
    is_conf = "conference-paper" == w["type"] or re.search(r"conference|proceedings|workshop|symposium", venue, re.I)
    vf = "booktitle" if (is_conf and ptype == "published") else "journal"
    b = w.get("biblio") or {}
    pages = "--".join(x for x in (b.get("first_page"), b.get("last_page")) if x)
    f = [("bibtex_show", "true"), ("pubtype", ptype), ("title", esc(w["title"])), ("author", esc(authors)),
         (vf, esc(venue)), ("volume", b.get("volume")), ("number", b.get("issue")), ("pages", pages),
         ("year", w["publication_year"]), ("doi", (w.get("doi") or "").replace("https://doi.org/", "")),
         ("arxiv", None)]
    for l in w.get("locations") or []:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", (l or {}).get("landing_page_url") or "")
        if m:
            f[-1] = ("arxiv", m.group(1))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in f if v)
    return f"@{'inproceedings' if vf == 'booktitle' else 'article'}{{{key},\n{body}\n}}"


def dedupe(text: str) -> str:
    """Drop entries that duplicate another (preprint loses to published, then the fuller entry wins)."""
    ents = []
    for s_, e_ in spans(text):
        b = text[s_:e_]
        m = re.search(r"year\s*=\s*[{\"]?(\d{4})", b)
        ents.append({"s": s_, "e": e_, "t": title_of(b), "y": m.group(1) if m else None,
                     "pub": "pubtype = {published}" in b, "n": len(b), "gs": "google_scholar_id" in b})
    drop = set()
    for i, a in enumerate(ents):
        for j in range(i + 1, len(ents)):
            b = ents[j]
            if i in drop or j in drop or not same_paper(a["t"], a["y"], b["t"], b["y"]):
                continue
            score = lambda x: (x["pub"], x["gs"], x["n"])
            drop.add(j if score(a) >= score(b) else i)
    for k in sorted(drop, reverse=True):
        print("  dropping duplicate:", text[ents[k]["s"]:ents[k]["e"]].split("title = {")[1][:70] if "title = {" in text[ents[k]["s"]:ents[k]["e"]] else ents[k]["t"])
        text = text[:ents[k]["s"]] + text[ents[k]["e"]:]
    return re.sub(r"\n{3,}", "\n\n", text)


def main() -> None:
    with open(SOCIALS_FILE) as f:
        soc = yaml.safe_load(f)
    orcid, name = soc["orcid_id"], "Ruocheng Guo"
    text = open(BIB_FILE, encoding="utf-8").read()
    try:
        works = fetch_works(orcid, name)
    except Exception as e:
        print(f"OpenAlex unreachable ({e!r}); leaving {BIB_FILE} unchanged.")
        return
    info = {}  # normalized title -> (pubtype, venue, work); published wins over preprint
    for w in works:
        k = norm(w["title"])
        t, v = classify(w)
        if k not in info or (info[k][0] == "preprint" and t == "published"):
            info[k] = (t, v, w)
    print(f"OpenAlex: {len(works)} works -> {len(info)} distinct titles.")

    # 1) tag existing entries, fix venues of preprint-labelled published papers
    out, last, tagged, fixed = [], 0, 0, 0
    for s, e in spans(text):
        blk = text[s:e]
        k = title_of(blk)
        h = heuristic(blk)
        # a real (non-arXiv) venue already in the file beats OpenAlex's guess
        t = h if (h == "published" and "arxiv" not in blk.lower().split("abstract")[0]) else (info[k][0] if k in info else h)
        if "pubtype" not in blk:
            nl = blk.index("\n")
            blk = blk[:nl] + f"\n  pubtype = {{{t}}}," + blk[nl:]
            tagged += 1
            if k in info and t == "published" and info[k][1]:
                nv = esc(info[k][1])
                blk2 = re.sub(r"((?:journal|booktitle)\s*=\s*)[{\"][^}\"]*(?:arxiv|preprint)[^}\"]*[}\"]",
                              lambda m: m.group(1) + "{" + nv + "}", blk, flags=re.I)
                fixed += blk2 != blk
                blk = blk2
        out.append(text[last:s] + blk)
        last = e
    text = "".join(out) + text[last:]

    if "--dedupe" in sys.argv:
        text = dedupe(text)

    # 2) add works missing from the file
    def year_of(b):
        m = re.search(r"year\s*=\s*[{\"]?(\d{4})", b)
        return m.group(1) if m else None

    have_pool = [(title_of(text[s:e]), year_of(text[s:e])) for s, e in spans(text)]
    have = {t for t, _ in have_pool}
    used = set(re.findall(r"^@\w+\{([^,]+),", text, re.M))
    new = [(k, v) for k, v in info.items()
           if k not in have and not find_dup(k, str(v[2]["publication_year"]), have_pool)]
    if new and MARKER not in text and "Added automatically" not in text:
        text = text.rstrip() + f"\n\n{MARKER}\n"
    for k, (t, v, w) in new:
        text = text.rstrip() + "\n\n" + entry(w, t, v, used) + "\n"
    open(BIB_FILE, "w", encoding="utf-8").write(text)
    n_pub = len(re.findall(r"pubtype = \{published\}", text))
    n_pre = len(re.findall(r"pubtype = \{preprint\}", text))
    print(f"tagged {tagged}, venue-fixed {fixed}, added {len(new)}. Now {n_pub} published, {n_pre} preprints.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    main()
