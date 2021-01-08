from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
import re
from django.utils.safestring import mark_safe


register = template.Library()


# この関数に時間を渡して、そのファイルが開けるかどうか判定する
# もし開けなかったら、disableをつけるなりして、リンクを渡さないようにする
# AWSのアクセス許容時間を調べる
# あと、チャット送信時にバリデーションを行うようにする

@register.filter
@stringfilter
def my_urlize(text, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = (lambda x: x)

    pattern = re.compile(r'<(?!/)(?!a\s+href\s?=\s?"?https?.*?(192.168.99.102|ymir.eng.kagawa-u.ac.jp)).*?>', re.S)
    if pattern.search(text):
        result = esc(text)
    else:
        result = text

    return mark_safe(result)


my_urlize.needs_autoescape = True
