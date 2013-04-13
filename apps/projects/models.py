from django.db import models
from apps.profiles.models import Profile
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse



class Project(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()
    description = models.TextField(_("Description"), null=True, blank=True)

    people = models.ManyToManyField(Profile, verbose_name=_("People"), null=True, blank=True)

    date_started = models.DateTimeField(_("Date Started"), default=datetime.now())

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('project_details', (), {'pk': self.pk, 'slug': self.slug})

    def todo_list(self):
        return self.todolist_set.all()

    def discussion_list(self):
        return self.discussion_set.all()

    def progress(self):
        todo_count = project.todolist_set.all().count()
        done_count = project.todolist_set.filter(is_done=True).count()
        return {'done':done_count, 'total':todo_count}


## TODO
## refactor model methods later

class Discussion(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    started_by = models.ForeignKey(Profile, verbose_name=_("Started by"))

    date_started = models.DateTimeField(_("Date Started"), default=datetime.now)

    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    slug = models.SlugField()
    content = models.TextField(_("Content"), null=True, blank=True)

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('discussion_details', (), {'pk': self.pk, 'slug': self.slug})

    def posts(self):
        return self.discussioncomment_set.all()

    def latest_post(self):
        pass#return self.discussioncomment_set.order_by('-date_started')


class ToDoList(models.Model):
    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    slug = models.SlugField()
    ordering = models.IntegerField(_("Ordering"))

    project = models.ForeignKey(Project, verbose_name=_("Project"))

    date_started = models.DateTimeField(_("Date Started"), default=datetime.now())
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        verbose_name = _("ToDo List")
        verbose_name_plural = _("ToDo Lists")
        ordering = ('ordering',)

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('todo_details', (), {'pk': self.pk, 'slug': self.slug})

    def comments(self):
        return self.todocomment_set.all()

    def tasks(self):
        return self.task_set.all()

    def completed_tasks(self):
        return self.tasks().filter(is_done=True)

    def active_tasks(self):
        return self.tasks().filter(is_done=False)



class Task(models.Model):
    todolist = models.ForeignKey(ToDoList, verbose_name=_("ToDo List"))
    title = models.CharField(_("Title"), max_length=200, null=True, blank=True)
    slug = models.SlugField()
    content = models.TextField(_("Content"), null=True, blank=True)
    ordering = models.IntegerField(_("Ordering"))
    deadline = models.DateTimeField(_("Deadline"), null=True, blank=True)
    is_done = models.BooleanField(_("Is completed"), default=False)

    people = models.ManyToManyField(Profile, verbose_name=_("People"))

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ('ordering',)

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_absolute_url(self):
        return ('task_details', (), {})



class BaseComment(models.Model):
    started_by = models.ForeignKey(Profile, verbose_name=_("Started By"))
    content = models.TextField(_("Content"), null=True, blank=True)
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()

    date_started = models.DateTimeField(_("Date Started"), default=datetime.now())

    class Meta:
        abstract = True


class DiscussionComment(BaseComment):
    discussion = models.ForeignKey(Discussion, verbose_name=_("Discussion"))

    def __unicode__(self):
        return u"%s" % (self.title)


class ToDoComment(BaseComment):
    todo = models.ForeignKey(Task, verbose_name=_("ToDO"))

    def __unicode__(self):
        return u"%s" % (self.title)


