from django.contrib import admin
from .models import Thread
from stumee_auth.models import CustomUser
# Register your models here.


class ThreadAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'tag']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(CustomUser)
