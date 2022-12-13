import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from courses.forms import StudentCreationForm
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


class LanguageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Language

    def get_context_data(self, **kwargs):
        language = self.object.name
        num_lessons = Lesson.objects.filter(language__name__icontains=language).count()
        num_students = Student.objects.filter(student_language__name__icontains=language).count()

        context = {
            "num_students": num_students,
            "num_lessons": num_lessons,
        }
        return context


class LevelListView(LoginRequiredMixin, generic.ListView):
    model = Level
    template_name = "courses/level_list.html"


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    paginate_by = 3


def info(request):
    num_students = Student.objects.count()
    num_lessons = Lesson.objects.count()
    num_languages = Language.objects.count()

    context = {
        "num_students": num_students,
        "num_lessons": num_lessons,
        "num_languages": num_languages,
    }
    return render(request, "courses/info.html", context=context)


class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    paginate_by = 10
    queryset = Lesson.objects.all().select_related("level").filter(date_time__gt=datetime.datetime.now())


class LessonDetailView(LoginRequiredMixin,generic.DetailView):
    model = Lesson


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    queryset = Student.objects.all().prefetch_related("lessons__level")


class StudentCreateView(generic.CreateView):
    model = Student
    form_class = StudentCreationForm


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy("courses:student-list")


@login_required
def toggle_assign_to_lesson(request, pk):
    student = Student.objects.get(id=request.user.id)
    if (
        Lesson.objects.get(id=pk) in student.lessons.all()
    ):
        student.lessons.remove(pk)
    else:
        student.lessons.add(pk)
    return HttpResponseRedirect(reverse_lazy("courses:lesson-detail", args=[pk]))


def confirm_lesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    if lesson.is_approved is False:
        lesson.is_approved = True
    else:
        lesson.is_approved = False
    lesson.save()
    return HttpResponseRedirect(reverse_lazy("courses:lesson-detail", args=[pk]))
