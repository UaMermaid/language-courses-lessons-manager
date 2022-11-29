from django.urls import path

from courses.views import index, LanguageListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "languages/",
        LanguageListView.as_view(),
        name="language-list",
    ),
]

app_name = "courses"
