import feedparser #feedparser.org
import datetime
from django import template
register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request):
        return 'active'
    return request

@register.inclusion_tag('feedreader.html')
def pull_feed(feed_url, posts_to_show=5):
    feed = feedparser.parse(feed_url)
    posts = []
    try:
        for i in range(posts_to_show):
            pub_date = feed['entries'][i].updated_parsed
            published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
            posts.append({
                'title': feed['entries'][i].title,
                'summary': feed['entries'][i].summary,
                'link': feed['entries'][i].link,
                'date': published,
                })
    except IndexError:
        pass
    return {'posts': posts}
