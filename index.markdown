---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

<h1>List of albums</h1>

<ul>
{% for album in site.data.albumlist %}
  <li>
    <a href="{{ 'albums/' | append: album.albumid | append: '.html' | relative_url }}">
      {{ album.albumtitle }}
    </a>
     ({{ album.year }}) 
    <a href="{{ album.musicbrainzlink }}">Musicbrainz record</a>
  </li>
{% endfor %}
</ul>
