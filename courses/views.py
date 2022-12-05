from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from courses.models import Student, Lesson, Language, Level


@login_required
def index(request):
    """View function for the home page of the site."""

    num_students = Student.objects.count()
    num_lessons = Lesson.objects.count()
    num_languages = Language.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_students": num_students,
        "num_lessons": num_lessons,
        "num_languages": num_languages,
        "num_visits": num_visits + 1,
    }

    return render(request, "courses/index.html", context=context)


class LanguageListView(LoginRequiredMixin, generic.ListView):
    model = Language
    template_name = "courses/language_list.html"
    paginate_by = 5


class LevelListView(LoginRequiredMixin, generic.ListView):
    model = Level
    template_name = "courses/level_list.html"


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    paginate_by = 1


def info(request):
    return render(request, "courses/info.html")