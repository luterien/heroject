from apps.projects.models import *
from django.contrib import admin

admin.site.register(Project)
admin.site.register(Discussion)
admin.site.register(Task)
admin.site.register(DiscussionComment)
admin.site.register(ToDoComment)