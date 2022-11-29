from django.contrib.auth.models import AbstractUser
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]


class Level(models.Model):
    level = models.CharField(max_length=2, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return f"{self.level} \n{self.description}"


class Student(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
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
        verbose_name = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField()
    students = models.ManyToManyField(to=Student, related_name="lessons")

    class Meta:
        ordering = ["date_time"]

    def __str__(self):
        return f"{self.title} ({self.language}, {self.level})"
