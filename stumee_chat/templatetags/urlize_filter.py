from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
import re
from django.utils.safestring import mark_safe


register = template.Library()


# この関数に時間を渡して、そのファイルが開けるかどうか判定する
# もし開けなかったら、disableをつけるなりして、リンクを渡さないようにする
# AWSのアクセス許容時間を調べる

@register.filter
@stringfilter
def my_urlize(text, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = (lambda x: x)

    if "<a href" in text:
        file_link = re.match(r'<a.*?href=(.*?)>', text)
        file_name = re.match(r'<a.*?>(.*?)</a>', text)
        result = '<a href={}>{}</a>'.format(file_link.group(1), file_name.group(1))
    else:
        result = esc(text)
    return mark_safe(result)


my_urlize.needs_autoescape = True
