---
layout: archive
title: "Hobbies"
permalink: /hobbies/
author_profile: true
---

{% include base_path %}

Things I do when I'm not doing research: road trips, hiking, and chasing waterfalls
with a camera.

<style>
.hobby-list { list-style: none; padding: 0; margin: 1.5em 0 0; }
.hobby-card {
  display: flex; gap: 1.25em; align-items: flex-start;
  padding: 1.1em 0; border-top: 1px solid #e5e5e5;
}
.hobby-card:last-child { border-bottom: 1px solid #e5e5e5; }
.hobby-card img {
  width: 220px; max-width: 38%; height: 150px; object-fit: cover;
  border-radius: 6px; flex: 0 0 auto;
}
.hobby-card h3 { margin: 0 0 .25em; font-size: 1.15em; }
.hobby-card h3 a { text-decoration: none; }
.hobby-meta { font-size: .82em; text-transform: uppercase; letter-spacing: .06em; color: #898781; margin-bottom: .4em; }
.hobby-card p { margin: 0; font-size: .95em; }
@media (max-width: 600px) {
  .hobby-card { flex-direction: column; }
  .hobby-card img { width: 100%; max-width: 100%; height: 180px; }
}
</style>

<ul class="hobby-list">
  <li class="hobby-card">
    <a href="{{ base_path }}/hobbies/roadtrip-2026/">
      <img src="{{ base_path }}/images/roadtrip_2026/photos/multnomah.jpg" alt="Multnomah Falls">
    </a>
    <div>
      <div class="hobby-meta">Road trip &middot; Summer 2026</div>
      <h3><a href="{{ base_path }}/hobbies/roadtrip-2026/">Mountain View, CA &rarr; Bellevue, WA</a></h3>
      <p>1,200 miles up the spine of the Cascades: 19 waypoints, 6 waterfalls.
      Interactive route map and photos.</p>
    </div>
  </li>
</ul>
