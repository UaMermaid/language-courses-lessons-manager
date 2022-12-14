from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import request

from courses.models import Student, Language, Level, Lesson


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + (
            "phone_number",
            "first_name",
            "last_name",
            "student_language",
            "student_level",
        )


class LessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields["language"].queryset = Language.objects.filter(
            name=self.request.user.student_language)

    level = forms.ModelChoiceField(queryset=Level.objects.all(), widget=forms.Select)
    date_time = forms.DateTimeInput()

    class Meta:
        model = Lesson
        fields = ["title", "language", "level", "date_time"]
