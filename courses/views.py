import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
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


class LevelListView(LoginRequiredMixin, generic.ListView):
    model = Level
    template_name = "courses/level_list.html"


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    paginate_by = 1


def info(request):
    return render(request, "courses/info.html")


class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    queryset = Lesson.objects.all().filter(date_time__gt=datetime.datetime.now())


class LessonDetailView(LoginRequiredMixin,generic.DetailView):
    model = Lesson


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    queryset = Student.objects.all().prefetch_related("lessons__level")


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Student
    form_class = StudentCreationForm


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy("courses:student-list")


@login_required
def add_student_to_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.students.add(request.user.id)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


@login_required
def driver_delete_from_car(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.students.add(request.user.id)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
