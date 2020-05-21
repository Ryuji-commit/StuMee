from django.shortcuts import render
from django.http import HttpResponse
import datetime


# temp view
def temp_view(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)