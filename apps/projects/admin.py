from apps.projects.models import *
from django.contrib import admin


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class DiscussionInline(admin.TabularInline):
    model = Discussion
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_started',)
    search_fields = ('title',)
    list_filter = ('date_started',)
    inlines = [TaskInline, DiscussionInline]


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'date_created', 'is_done',)
    search_fields = ('project', 'title',)
    list_filter = ('date_created', 'is_done',)
    raw_id_fields = ('project',)
    inlines = [TaskCommentInline]


class DiscussionCommentInline(admin.TabularInline):
    model = DiscussionComment
    extra = 0


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'started_by', 'content',
                    'date_started',)
    search_fields = ('project', 'title', 'content', 'started_by',)
    list_filter = ('date_started',)
    raw_id_fields = ('project', 'started_by',)
    inlines = [DiscussionCommentInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(DiscussionComment)
admin.site.register(TaskComment)