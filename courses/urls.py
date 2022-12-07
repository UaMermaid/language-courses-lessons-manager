from django.urls import path

from courses.views import index, LanguageListView, LevelListView, StudentListView, info, LessonListView, \
    LessonDetailView

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

]

app_name = "courses"
