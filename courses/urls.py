from django.urls import path

from courses.views import index, LanguageListView, LevelListView, StudentListView

urlpatterns = [
    path("", index, name="index"),
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
]

app_name = "courses"
