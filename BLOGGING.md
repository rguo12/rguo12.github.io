# Writing posts

Create `_posts/YYYY-MM-DD-your-title.md`, commit, push to `master`. GitHub Actions builds and deploys.

```markdown
---
layout: post
title: A clear post title
date: 2026-10-10
description: One-sentence summary shown in the blog list.
tags: causal-inference reinforcement-learning
categories: research
thumbnail: assets/img/posts/my-post/cover.jpg   # optional
toc:
  sidebar: left                                  # optional table of contents
---
```

## LaTeX

Inline: `$$ f(x) = x^2 $$` or `\( f(x) = x^2 \)`. Display math:

```
$$
\mathcal{L}(\theta) = -\sum_{i=1}^{n} \log p_\theta(y_i \mid x_i)
$$
```

## Images

Put files in `assets/img/posts/<post-name>/` and use the figure include (click-to-zoom, responsive, dark-mode aware):

```liquid
{% include figure.liquid path="assets/img/posts/my-post/plot.png" class="img-fluid rounded z-depth-1" caption="Figure 1. Caption here." %}
```

Side by side:

```liquid
<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/posts/my-post/a.png" class="img-fluid rounded" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/posts/my-post/b.png" class="img-fluid rounded" %}
  </div>
</div>
```

Plain Markdown `![alt](/assets/img/posts/my-post/plot.png)` also works.

## Other things that work

- Code blocks with highlighting (` ```python `), tables, footnotes (`[^1]`)
- Mermaid / Chart.js / Plotly / Jupyter notebooks (see https://github.com/alshedivat/al-folio/tree/main/docs)
- `giscus` comments: set `giscus.repo_id` and `category_id` in `_config.yml` (get them from https://giscus.app), then add `giscus_comments: true` to a post's front matter
- `pinned: true` or `featured: true` in front matter to highlight a post

## Preview locally

```bash
export PATH=/opt/homebrew/opt/ruby@3.3/bin:$PATH LC_ALL=en_US.UTF-8
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

# Publications

`_bibliography/papers.bib` drives the Publications page. A GitHub Action
(`.github/workflows/update-publications.yml`, Mondays, or run it manually from the
Actions tab) syncs it with your Google Scholar profile:

- papers on Scholar but not in the file are **appended** at the bottom;
- existing entries are never overwritten, so you can freely add `selected={true}`,
  `preview={fig.png}` (image in `assets/img/publication_preview/`), `pdf=`, `code=`,
  `abbr={ICML}` etc. to any entry;
- `bin/sync_openalex_publications.py` (OpenAlex, not rate-limited) fills gaps and sets
  `pubtype = {published}` or `{preprint}` on each entry; the page shows these as two sections.
  Change `pubtype` by hand if a paper is classified wrongly (it is never overwritten);
- citation badges are turned off in `_config.yml` (`enable_publication_badges`); the counts need Scholar, which blocks automated requests.

Google Scholar sometimes blocks requests from GitHub's servers. When that happens the run
changes nothing and the site keeps its last data. Run locally instead:

```bash
pip install scholarly pyyaml
python bin/sync_scholar_publications.py
python bin/update_scholar_citations.py
```
