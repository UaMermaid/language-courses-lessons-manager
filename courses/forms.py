import django_filters
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from courses.models import Student, Language, Level, Lesson


class StudentCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+380000000000"}),
        validators=[RegexValidator(
            regex=r"['+380'][0-9]{9}",
            message="Please use number like +380XXXXXXXXX")]
    )

    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + (
            "phone_number",
            "first_name",
            "last_name",
            "student_language",
            "student_level",
        )


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "phone_number",
            "student_language",
            "student_level"
        ]

    phone_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
                regex=r"['+380'][0-9]{9}",
                message="Please write number like +380XXXXXXXXX")
        ]
    )


class LessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that
        only language of the current user
        """

        self.request = kwargs.pop("request")
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields["language"].queryset = Language.objects.filter(
            name=self.request.user.student_language)

    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select
    )
    date_time = forms.DateTimeField(
        input_formats=["%d.%m.%y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d.%m.%y %H:%M",
            attrs={"type": "datetime", "placeholder": "DD.MM.YY HH:MM"},
        )
    )

    class Meta:
        model = Lesson
        fields = ["title", "language", "level", "date_time"]


class LessonUpdateForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        input_formats=["%d.%m.%y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d.%m.%y %H:%M",
            attrs={"type": "datetime", "placeholder": "DD.MM.YY HH:MM"},
        )
    )

    class Meta:
        model = Lesson
        fields = ["title", "date_time"]


class StudentSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."})
    )


class LessonFilter(django_filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ["language", "level"]
