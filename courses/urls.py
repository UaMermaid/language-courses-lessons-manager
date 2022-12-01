from django.urls import path

from courses.views import index, LanguageListView, LevelListView

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
]

app_name = "courses"
