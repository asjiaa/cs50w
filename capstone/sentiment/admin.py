from django.contrib import admin

from .models import User, Topic, Log, Article, Sentiment

# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Log)
admin.site.register(Article)
admin.site.register(Sentiment)