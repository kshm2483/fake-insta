from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content+' '
    hashtags = post.hashtags.all()
    
    # hashtags 를 순회하면서 , contnent 내에서 해당 문자열(해시태그)를 링크를 포함한 문자열로 치환한다
    for hashtag in hashtags:
        content = content.replace(hashtag.content+' ', '<a href="/posts/hashtag/{}/">{}</a>'.format(hashtag.pk, hashtag.content))
    return content