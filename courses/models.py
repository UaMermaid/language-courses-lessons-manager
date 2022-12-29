import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Level(models.Model):
    level = models.CharField(max_length=2, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return f"{self.level}"


class Student(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)
    student_language = models.ForeignKey(
        to=Language,
        on_delete=models.CASCADE,
        default=Language.objects.get(id=1).pk
    )
    student_level = models.ForeignKey(
        to=Level,
        on_delete=models.CASCADE,
        default=Level.objects.get(level="A1").pk
    )

    class Meta:
        ordering = ["first_name"]
        verbose_name = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("courses:student-detail", kwargs={"pk": self.pk})


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        datetime.datetime,
        default=datetime.datetime.now()
    )
    is_approved = models.BooleanField(default=False)
    students = models.ManyToManyField(to=Student, related_name="lessons")

    class Meta:
        ordering = ["date_time"]

    def __str__(self):
        date = datetime.datetime.strftime(self.date_time, '%d.%m.%y %H:%M')
        return f"{date} {self.title} ({self.language}, {self.level})"

    @property
    def get_html_url(self):
        url = reverse("courses:lesson-detail", args=(self.id,))
        return f"<a href='{url}'>" \
               f"{datetime.datetime.strftime(self.date_time, '%H:%M')} " \
               f"{self.title} ({self.language})</a>"
