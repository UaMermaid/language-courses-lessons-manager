import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic

from courses.forms import (
    StudentCreationForm,
    LessonForm,
    LessonUpdateForm,
    StudentSearchForm,
    LessonFilter,
    StudentUpdateForm
)
from courses.models import Student, Lesson, Language, Level
from courses.utils import Calendar


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


class LanguageListView(LoginRequiredMixin, generic.ListView):
    model = Language
    template_name = "courses/language_list.html"


class LanguageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Language

    def get_context_data(self, **kwargs):
        language_name = self.object.name
        language_pk = self.object.id
        actual_lesson_query = Lesson.objects.filter(
            language__name__icontains=language_name,
            date_time__gt=datetime.datetime.now()
        )
        num_lessons = actual_lesson_query.count()
        num_students = Student.objects.filter(
            student_language__name__icontains=language_name
        ).count()
        language_lessons_list = actual_lesson_query.values()

        context = {
            "num_students": num_students,
            "num_lessons": num_lessons,
            "language_pk": language_pk,
            "language_name": language_name,
            "language_lessons_list": language_lessons_list
        }
        return context


class LanguageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Language
    fields = "__all__"
    success_url = reverse_lazy("courses:language-list")


class LanguageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Language
    fields = "__all__"
    success_url = reverse_lazy("courses:language-list")


class LanguageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Language
    success_url = reverse_lazy("courses:language-list")


class LevelListView(LoginRequiredMixin, generic.ListView):
    model = Level
    template_name = "courses/level_list.html"


class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    paginate_by = 5
    queryset = Lesson.objects.all().select_related(
        "language"
    ).select_related("level").filter(
        date_time__gt=datetime.datetime.now()
    )


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy("courses:lesson-list")

    def get_form_kwargs(self):

        kwargs = super(LessonCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class LessonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    form_class = LessonUpdateForm
    success_url = reverse_lazy("courses:lesson-list")


class LessonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson
    success_url = reverse_lazy("courses:lesson-list")


class LessonLanguageListView(LoginRequiredMixin, generic.ListView):
    model = Lesson


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    paginate_by = 6  # better to be multiple of 3
    queryset = Student.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = StudentSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = StudentSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    queryset = Student.objects.all().prefetch_related("lessons__language")


class StudentCreateView(generic.CreateView):
    model = Student
    form_class = StudentCreationForm


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy("courses:student-list")


class StudentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Student
    form_class = StudentUpdateForm
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
    return HttpResponseRedirect(
        reverse_lazy("courses:lesson-detail", args=[pk])
    )


def confirm_lesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    if lesson.is_approved is False:
        lesson.is_approved = True
    else:
        lesson.is_approved = False
    lesson.save()
    return HttpResponseRedirect(
        reverse_lazy("courses:lesson-detail", args=[pk])
    )


def lesson_filtered_list(request):
    f = LessonFilter(
        request.GET,
        queryset=Lesson.objects.all().select_related(
            "language"
        ).select_related("level").filter(
            date_time__gt=datetime.datetime.now()
        )
    )
    return render(request, "courses/lesson_filtered_list.html", {"filter": f})


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Lesson

    template_name = "courses/calendar.html"
    success_url = reverse_lazy("courses/calendar.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth()

        context = {
            "calendar": mark_safe(html_cal),
            "prev_month": prev_month(d),
            "next_month": next_month(d),
        }

        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    month_prev = first - datetime.timedelta(days=1)
    month = 'month=' + str(month_prev.year) + '-' + str(month_prev.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    month_next = last + datetime.timedelta(days=1)
    month = 'month=' + str(month_next.year) + '-' + str(month_next.month)
    return month
