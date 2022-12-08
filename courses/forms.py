from django import forms
from django.contrib.auth.forms import UserCreationForm

from courses.models import Student, Language, Level, Lesson


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + (
            "phone_number",
            "first_name",
            "last_name",
        )


class LessonForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all(), widget=forms.Select)
    level = forms.ModelChoiceField(queryset=Level.objects.all(), widget=forms.Select)

    class Meta:
        model = Lesson
        fields = "__all__"
