#!/usr/bin/env python
"""Sync _bibliography/papers.bib with a Google Scholar profile.

Additive and safe to re-run:
  * papers already in papers.bib (matched by normalized title) are never rewritten,
    except that a missing `google_scholar_id` is filled in so citation badges work;
  * papers on Scholar that are not in papers.bib are appended at the end of the file,
    below the AUTO_MARKER line. Edit or move them freely afterwards (add `selected`,
    `preview`, `pdf`, `code`, ...); later runs will not touch them again.

Scholar rate-limits and sometimes blocks cloud IPs. If a request fails the script
keeps whatever it managed to fetch and exits 0, so a scheduled run never breaks the
site. At most --max-new papers are fetched in full per run; the rest are picked up
on later runs.
"""

import argparse
import os
import re
import sys
import time
import unicodedata

import yaml
from scholarly import scholarly
from scholarly._proxy_generator import ProxyGenerator


class ScholarBlocked(Exception):
    pass


def _refuse_captcha(self, url):
    # scholarly's default is to open a Selenium browser and wait for a human.
    raise ScholarBlocked("Google Scholar asked for a CAPTCHA")


ProxyGenerator._handle_captcha2 = _refuse_captcha

BIB_FILE = "_bibliography/papers.bib"
SOCIALS_FILE = "_data/socials.yml"
AUTO_MARKER = "% --- Added automatically from Google Scholar (edit freely) ---"

CONF_WORDS = re.compile(
    r"conference|proceedings|workshop|symposium|annual meeting|advances in neural|"
    r"international conference|\bicml\b|\biclr\b|\bneurips\b|\bkdd\b|\bwww\b|\bacl\b|"
    r"\bemnlp\b|\bwsdm\b|\bcikm\b|\bijcai\b|\baaai\b|\bsigir\b|\brecsys\b|\bsdm\b|\bicdm\b",
    re.I,
)


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def scholar_id() -> str:
    with open(SOCIALS_FILE) as f:
        sid = (yaml.safe_load(f) or {}).get("scholar_userid")
    if not sid:
        sys.exit(f"No scholar_userid in {SOCIALS_FILE}")
    return sid


def read_existing(text: str):
    """Return {normalized title: (start, end)} spans of each @entry in the bib text."""
    entries = {}
    for m in re.finditer(r"^@\w+\{[^,]+,", text, re.M):
        start = m.start()
        nxt = re.search(r"^@\w+\{", text[m.end():], re.M)
        end = m.end() + nxt.start() if nxt else len(text)
        block = text[start:end]
        t = re.search(r"title\s*=\s*[{\"](.+?)[}\"],?\s*\n", block, re.S)
        if t:
            entries[norm(re.sub(r"[{}]", "", t.group(1)))] = (start, end)
    return entries


def bib_escape(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def make_key(authors: str, year, title: str, used: set) -> str:
    first = norm(authors.split(" and ")[0]).split()
    last = first[-1] if first else "anon"
    word = next((w for w in norm(title).split() if len(w) > 3), "paper")
    base = f"{last}{year}{word}"
    key, i = base, 2
    while key in used:
        key, i = f"{base}{i}", i + 1
    used.add(key)
    return key


def build_entry(pub: dict, sid_pub: str, used: set) -> str:
    bib = pub["bib"]
    title = bib.get("title", "").strip()
    authors = bib.get("author", "")
    year = bib.get("pub_year", "")
    venue = (bib.get("journal") or bib.get("conference") or bib.get("booktitle")
             or bib.get("publisher") or "").strip()
    is_preprint = bool(re.search(r"arxiv|preprint|openreview|ssrn|researchgate", venue, re.I))
    is_conf = not is_preprint and bool(CONF_WORDS.search(venue))
    etype, vfield = ("inproceedings", "booktitle") if is_conf else ("article", "journal")

    fields = {
        "bibtex_show": "true",
        "title": f"{{{bib_escape(title)}}}",
        "author": "{" + bib_escape(authors) + "}",
        vfield: "{" + bib_escape(venue) + "}" if venue else None,
        "volume": bib.get("volume"),
        "number": bib.get("number"),
        "pages": bib.get("pages"),
        "year": year,
        "publisher": bib.get("publisher") if venue != bib.get("publisher") else None,
        "abstract": bib.get("abstract"),
        "url": pub.get("pub_url") or bib.get("pub_url"),
        "google_scholar_id": sid_pub,
    }
    m = re.search(r"arxiv[: ]*(\d{4}\.\d{4,5})", venue, re.I)
    if m:
        fields["arxiv"] = m.group(1)

    key = make_key(authors, year, title, used)
    lines = [f"@{etype}{{{key},"]
    for k, v in fields.items():
        if not v:
            continue
        v = str(v)
        if not (v.startswith("{") and v.endswith("}")):
            v = "{" + bib_escape(v).replace("{", "").replace("}", "") + "}" if k == "abstract" else "{" + v + "}"
        lines.append(f"  {k} = {v},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-new", type=int, default=20, help="max new papers to fetch in full per run")
    ap.add_argument("--delay", type=float, default=3.0, help="seconds between Scholar requests")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(BIB_FILE, encoding="utf-8") as f:
        text = f.read()
    existing = read_existing(text)
    used_keys = set(re.findall(r"^@\w+\{([^,]+),", text, re.M))

    sid = scholar_id()
    print(f"Fetching publication list for Scholar profile {sid} ...")
    try:
        author = scholarly.fill(scholarly.search_author_id(sid), sections=["publications"])
    except Exception as e:  # blocked, captcha, network
        print(f"Could not reach Google Scholar ({e!r}); leaving {BIB_FILE} unchanged.")
        return
    pubs = author.get("publications", [])
    print(f"Scholar lists {len(pubs)} publications; {len(existing)} already in {BIB_FILE}.")

    # 1) give already-present entries their google_scholar_id (citation badges)
    patched = 0
    for pub in pubs:
        t = norm(pub["bib"].get("title", ""))
        if t in existing:
            start, end = existing[t]
            block = text[start:end]
            if "google_scholar_id" not in block:
                gid = pub["author_pub_id"].split(":", 1)[1]
                first_nl = block.index("\n")
                block = block[:first_nl] + f"\n  google_scholar_id = {{{gid}}}," + block[first_nl:]
                text = text[:start] + block + text[end:]
                patched += 1
                existing = read_existing(text)  # offsets moved
    print(f"Added google_scholar_id to {patched} existing entries.")

    # 2) append papers that are on Scholar but not in the bib
    new = [p for p in pubs if norm(p["bib"].get("title", "")) not in existing]
    print(f"{len(new)} papers are new; fetching up to {args.max_new}.")
    added = []
    for pub in new[: args.max_new]:
        try:
            time.sleep(args.delay)
            full = scholarly.fill(pub)
        except Exception as e:  # incl. ScholarBlocked
            print(f"  stopped early at {pub['bib'].get('title')!r}: {e!r}")
            break
        gid = pub["author_pub_id"].split(":", 1)[1]
        entry = build_entry(full, gid, used_keys)
        added.append(entry)
        print(f"  + {full['bib'].get('title')}")
        if AUTO_MARKER not in text:
            text = text.rstrip() + f"\n\n{AUTO_MARKER}\n"
        text = text.rstrip() + "\n\n" + entry + "\n"
        if not args.dry_run:  # save after every paper so a block mid-run loses nothing
            with open(BIB_FILE, "w", encoding="utf-8") as f:
                f.write(text)
    if args.dry_run:
        print("Dry run: not writing.")
        return
    with open(BIB_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Done: {patched} patched, {len(added)} added, {len(new) - len(added)} still pending.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    main()
