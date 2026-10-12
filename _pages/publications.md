---
layout: page
permalink: /publications/
title: publications
description: peer-reviewed publications, followed by arXiv-only preprints. Synced from Google Scholar and OpenAlex.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

<h2 class="mt-4">Published</h2>

{% bibliography --query @*[pubtype=published] %}

<h2 class="mt-5">Preprints (arXiv only)</h2>

{% bibliography --query @*[pubtype=preprint] %}

</div>
