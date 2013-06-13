from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from projectbonus.utils import slugify

## TODO
## Project permissions


class Project(models.Model):
    title = models.CharField(_("Title"), max_length=100)

    slug = models.SlugField()

    description = models.TextField(_("Description"), null=True, blank=True)

    people = models.ManyToManyField(User, verbose_name=_("People"),
                                    null=True, blank=True)

    date_started = models.DateTimeField(_("Date Started"),
                                        auto_now_add=True)

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return reverse('project_details', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Project, self).save(*args, **kwargs)

    def completed_tasks(self):
        return self.task_set.filter(is_done=True)

    def active_tasks(self):
        return self.task_set.filter(is_done=False)

    def active_tasks_count(self):
        return self.active_tasks().count()

    def discussions(self):
        return self.discussion_set.all()

    def progress(self):
        todo_count = self.task_set.all().count()
        done_count = self.task_set.filter(is_done=True).count()

        try:
            return done_count*100/todo_count
        except ZeroDivisionError:
            return 0    


class Discussion(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"))

    started_by = models.ForeignKey(User, verbose_name=_("Started by"))

    date_started = models.DateTimeField(_("Date Started"),
                                        auto_now_add=True)

    title = models.CharField(_("Title"), max_length=100,
                             null=True, blank=True)

    slug = models.SlugField()

    content = models.TextField(_("Content"), null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return reverse('discussion_details', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Discussion, self).save(*args, **kwargs)

    def posts(self):
        return self.discussioncomment_set.all()

    def latest_post(self):
        pass#return self.discussioncomment_set.order_by('-date_started')


class Task(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"))

    title = models.CharField(_("Title"), max_length=200,
                             null=True, blank=True)

    slug = models.SlugField()

     ## remove this field
    content = models.TextField(_("Content"), null=True, blank=True)

    ordering = models.IntegerField(_("Ordering"))

    is_done = models.BooleanField(_("Is completed"), default=False)

    # dates
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    date_closed = models.DateTimeField(_("Date closed"),
                                       null=True, blank=True)

    deadline = models.DateTimeField(_("Deadline"), null=True, blank=True)

    date_started = models.DateTimeField(
        _("Starting Date"), null=True, blank=True,
        help_text="When the assigned people started working on the task")

    date_ended = models.DateTimeField(_("Ending Data"), null=True, blank=True)

    # people
    people = models.ManyToManyField(User, verbose_name=_("People"),
                                    related_name="assigned_people")

    started_by = models.ForeignKey(
        User, verbose_name=_("Started by"),
        help_text="The person who has created the task")

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ('ordering',)

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_absolute_url(self):
        return reverse('task_details', (), {'pk': self.pk})

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
    started_by = models.ForeignKey(User, verbose_name=_("Started By"))
    content = models.TextField(_("Content"), null=True, blank=True)
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()

    date_started = models.DateTimeField(_("Date Started"), auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(BaseComment, self).save(*args, **kwargs)


class DiscussionComment(BaseComment):
    discussion = models.ForeignKey(Discussion, verbose_name=_("Discussion"))

    def __unicode__(self):
        return u"%s" % self.title


class TaskComment(BaseComment):
    task = models.ForeignKey(Task, verbose_name=_("Task"))

    def __unicode__(self):
        return u"%s" % self.content


