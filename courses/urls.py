from django.urls import path

from courses.views import index, LanguageListView, LevelListView, StudentListView, info, LessonListView, \
    LessonDetailView, StudentDetailView, StudentCreateView, StudentDeleteView, toggle_assign_to_lesson

urlpatterns = [
    path("index/", index, name="index"),
    path(
        "languages/",
        LanguageListView.as_view(),
        name="language-list",
    ),
    path(
        "levels/",
        LevelListView.as_view(),
        name="level-list",
    ),
    path("students/", StudentListView.as_view(), name="student-list"),
    path("info/", info, name="info"),
    path("shedule/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path(
        "students/<int:pk>/delete/",
        StudentDeleteView.as_view(),
        name="student-delete",
    ),
    path(
        "lessons/<int:pk>/toggle-assign/",
        toggle_assign_to_lesson,
        name="toggle-lesson-assign",
    ),
]

app_name = "courses"
