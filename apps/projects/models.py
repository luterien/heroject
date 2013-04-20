from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from projectbonus.utils import slugify
from apps.profiles.models import Profile

## TODO
## Project permissions

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
        return ('project_details', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Project, self).save(*args, **kwargs)

    def completed_tasks(self):
        return self.task_set.filter(is_done=True)

    def active_tasks(self):
        return self.task_set.filter(is_done=False)

    def discussions(self):
        return self.discussion_set.all()

    def progress(self):
        todo_count = self.task_set.all().count()
        done_count = self.task_set.filter(is_done=True).count()
        try:
            return done_count*100/todo_count
        except ZeroDivisionError:
            return None    


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
        return ('discussion_details', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Discussion, self).save(*args, **kwargs)

    def posts(self):
        return self.discussioncomment_set.all()

    def latest_post(self):
        pass#return self.discussioncomment_set.order_by('-date_started')


class Task(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    title = models.CharField(_("Title"), max_length=200, null=True, blank=True)
    slug = models.SlugField()
    content = models.TextField(_("Content"), null=True, blank=True) ## remove this field
    ordering = models.IntegerField(_("Ordering"))
    deadline = models.DateTimeField(_("Deadline"), null=True, blank=True)
    is_done = models.BooleanField(_("Is completed"), default=False)

    started_by = models.ForeignKey(Profile, verbose_name=_("Started by"))

    people = models.ManyToManyField(Profile, verbose_name=_("People"), related_name="assigned_people")

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ('ordering',)

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_absolute_url(self):
        return ('task_details', (), {'pk':self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Task, self).save(*args, **kwargs)

    def deadline_status(self):
        pass

    def comments(self):
        return self.taskcomment_set.all()

    def comment_count(self):
        return self.taskcomment_set.count()

    def assigned_peoples(self):
        return self.people.all()



class BaseComment(models.Model):
    started_by = models.ForeignKey(Profile, verbose_name=_("Started By"))
    content = models.TextField(_("Content"), null=True, blank=True)
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()

    date_started = models.DateTimeField(_("Date Started"), default=datetime.now())

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(BaseComment, self).save(*args, **kwargs)


class DiscussionComment(BaseComment):
    discussion = models.ForeignKey(Discussion, verbose_name=_("Discussion"))

    def __unicode__(self):
        return u"%s" % (self.title)


class TaskComment(BaseComment):
    task = models.ForeignKey(Task, verbose_name=_("Task"))

    def __unicode__(self):
        return u"%s" % (self.title)


