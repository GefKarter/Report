from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Category'))

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Notification(models.Model):
    notification_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(
        'The user who wants to become the author of the notification'))
    notification_category = models.ManyToManyField(Category, verbose_name=_('Notification category'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date creation'))
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.SmallIntegerField(default=0, verbose_name=_('Rating'))
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name=_('Photo'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('Board:notification_detail', args=[str(self.id)])

    # save используется вместе с get_object в классе NotificationDetail
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'notification-{self.pk}')

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-date_creation', 'rating']


class Responses(models.Model):
    responses_advertising = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name=_('Notification'))
    responses_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.TextField(verbose_name=_('Response text'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date the response was created'))
    status = models.IntegerField(choices=((0, 'Not considered'), (1, 'Accept'), (2, 'Reject')), default=0,
                                 verbose_name=_('Status response'))

    def __str__(self):
        return self.text.title()

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
