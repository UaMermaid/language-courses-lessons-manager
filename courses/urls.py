from django.urls import path

from courses.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "courses"
