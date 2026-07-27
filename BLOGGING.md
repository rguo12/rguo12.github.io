# Writing blog posts

This site is built with Jekyll. To publish a post, create a Markdown file in
`_posts/` named `YYYY-MM-DD-your-post-title.md`. Jekyll turns it into a page
automatically and adds it to the [Blog](/year-archive/) archive.

Use this starting point:

```markdown
---
title: "A clear, useful post title"
date: 2026-07-19
excerpt: "A one-sentence summary shown in listings."
tags:
  - machine learning
  - research
---

An introductory paragraph in **Markdown**.

## A section heading

Use a link: [my website](https://rguo12.github.io/).

Inline math works with `\(` and `\)`: \(f(x) = x^2 + 1\).

Display math works with either `\[` / `\]` or `$$`:

\[
  \mathcal{L}(\theta) = -\sum_{i=1}^{n} \log p_\theta(y_i \mid x_i).
\]

```python
def greet(name):
    return f"Hello, {name}!"
```
```

## English and Chinese versions

For a bilingual post, create two Markdown files: one English and one Chinese.
Give them the same `translation_key`, and set `lang` to `en` or `zh`. The
Chinese file is what appears in the blog, tag, and category archives; each
version has a language switcher linking readers to the other one.

For example, use these filenames:

```
_posts/2026-07-20-my-post.md
_posts/2026-07-20-my-post-zh.md
```

Use matching front matter in the two files (with the appropriate title and
content for each language):

```markdown
---
title: "My post title"
date: 2026-07-20
lang: en
translation_key: my-post
---
```

```markdown
---
title: "我的文章标题"
date: 2026-07-20
lang: zh
translation_key: my-post
---
```

Use a unique, URL-safe `translation_key` such as `causal-ml-notes`. Both
versions must use exactly the same key. A post without these fields continues
to work normally.

## Notes

- Do not put spaces in the filename's date portion; the date determines the
  post URL and ordering.
- Write ordinary prose with standard Markdown: headings, lists, links, images,
  block quotes, and fenced code blocks are supported.
- MathJax renders LaTeX in the browser. Use `\(...\)` for inline equations
  and `\[...\]` or `$$...$$` for a centered equation. Avoid `$...$` inline
  delimiters so currency values such as `$20` remain ordinary text.
- If an equation contains a Liquid expression (two opening or closing curly
  braces), surround the equation with Liquid's `raw` and `endraw` tags to
  prevent Jekyll from interpreting it as a template expression.

To preview changes locally after installing the Ruby dependencies, run:

```sh
bundle install
bundle exec jekyll serve -l -H localhost
```

Then open <http://localhost:4000/year-archive/>. Push the committed changes to
GitHub and GitHub Pages will publish the site.
