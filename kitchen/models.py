from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.urls import reverse
from multiselectfield import MultiSelectField
class Day(models.Model):
    MONDAY = 1
    TUESDSDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    DAY_CHOICES = (
        (MONDAY, "Monday"),
        (TUESDSDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    )

    id = models.PositiveIntegerField(choices=DAY_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

class Kitchen(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    image = models.ImageField(upload_to="kitchen/", blank=True, null=True)
    days = models.ManyToManyField(Day, related_name="days")

    # DAY_CHOICES = (
    #     ('Mon', 'Monday'),
    #     ('Tue', 'Tuesday'),
    #     ('Wed', 'Wednesday'),
    #     ('Thu', 'Thursday'),
    #     ('Fri', 'Friday'),
    #     ('Sat', 'Saturday'),
    #     ('Sun', 'Sunday'),
    # )
    # TIME_CHOICES = (('00:00:00', 'Midnight'),
    #                 ('01:00:00', '01 AM'),
    #                 ('02:00:00', '02 AM'),
    #                 ('03:00:00', '03 AM'),
    #                 ('04:00:00', '04 AM'),
    #                 ('05:00:00', '05 AM'),
    #                 ('06:00:00', '06 AM'),
    #                 ('07:00:00', '07 AM'),
    #                 ('08:00:00', '08 AM'),
    #                 ('09:00:00', '09 AM'),
    #                 ('10:00:00', '10 AM'),
    #                 ('11:00:00', '11 AM'),
    #                 ('12:00:00', 'Noon'),
    #                 ('13:00:00', '01 PM'),
    #                 ('14:00:00', '02 PM'),
    #                 ('15:00:00', '03 PM'),
    #                 ('16:00:00', '04 PM'),
    #                 ('17:00:00', '05 PM'),
    #                 ('18:00:00', '06 PM'),
    #                 ('19:00:00', '07 PM'),
    #                 ('20:00:00', '08 PM'),
    #                 ('21:00:00', '09 PM'),
    #                 ('22:00:00', '10 PM'),
    #                 ('23:00:00', '11 PM'),)
    # working_day = MultiSelectField(choices=DAY_CHOICES,max_choices=7)
    # start_time = models.CharField(choices=TIME_CHOICES, max_length=10, default='00:00:00')
    # end_time = models.CharField(choices=TIME_CHOICES, max_length=10, default='00:00:00')

    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:kitchen_detail', kwargs={'pk': self.pk})


class Item(models.Model):
    name = models.CharField(max_length=50)
    VEGAN_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    vegan = models.CharField(max_length=3,choices=VEGAN_CHOICES)

    price = models.PositiveIntegerField(blank=True, null=True)
    kitchen = models.ForeignKey(Kitchen, related_name='kitchen', on_delete=models.CASCADE)
    # user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    security_question1 = models.CharField(max_length=255)
    answer_question1 = models.CharField(max_length=255)
    security_question2 = models.CharField(max_length=255)
    answer_question2 = models.CharField(max_length=255)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Profile._meta.fields]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
        # Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()