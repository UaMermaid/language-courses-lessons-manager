from django.urls import path, include

from courses.views import (
    index,
    LanguageListView,
    LevelListView,
    StudentListView,
    info,
    LessonListView,
    LessonDetailView,
    StudentDetailView,
    StudentCreateView,
    StudentDeleteView,
    toggle_assign_to_lesson,
    confirm_lesson,
    LanguageDetailView,
    LessonCreateView,
    LanguageCreateView,
    LanguageDeleteView,
    LessonDeleteView,
    LessonUpdateView,
    lesson_filtered_list,
    LanguageUpdateView,
    CalendarView,
    StudentUpdateView
)

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path("study/", index, name="index"),
    path(
        "languages/",
        LanguageListView.as_view(),
        name="language-list",
    ),
    path(
        "languages/<int:pk>/",
        LanguageDetailView.as_view(),
        name="language-detail",
    ),
    path(
        "language/create/",
        LanguageCreateView.as_view(),
        name="language-create"
    ),
    path(
        "language/<int:pk>/update/",
        LanguageUpdateView.as_view(),
        name="language-update"
    ),
    path(
        "language/<int:pk>/delete/",
        LanguageDeleteView.as_view(),
        name="language-delete"
    ),
    path(
        "levels/",
        LevelListView.as_view(),
        name="level-list",
    ),
    path("students/", StudentListView.as_view(), name="student-list"),
    path("", info, name="info"),
    path("shedule/", LessonListView.as_view(), name="lesson-list"),
    path(
        "lessons/<int:pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail"
    ),
    path(
        "lessons/<int:pk>/update/",
        LessonUpdateView.as_view(),
        name="lesson-update"
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDeleteView.as_view(),
        name="lesson-delete"
    ),
    path(
        "lessons/filtered/",
        lesson_filtered_list,
        name="lesson-filtered-list"),
    path(
        "students/<int:pk>/",
        StudentDetailView.as_view(),
        name="student-detail"
    ),
    path(
        "students/create/",
        StudentCreateView.as_view(),
        name="student-create"
    ),
    path(
        "students/<int:pk>/delete/",
        StudentDeleteView.as_view(),
        name="student-delete",
    ),
    path(
        "students/<int:pk>/update/",
        StudentUpdateView.as_view(),
        name="student-update"
    ),
    path(
        "lessons/<int:pk>/toggle-assign/",
        toggle_assign_to_lesson,
        name="toggle-lesson-assign",
    ),
    path(
        "lessons/<int:pk>/confirm/",
        confirm_lesson,
        name="confirm-lesson",
    ),
    path("lesson/create/", LessonCreateView.as_view(), name="lesson-create"),
    path("lesson/calendar/", CalendarView.as_view(), name="calendar"),
]

app_name = "courses"
