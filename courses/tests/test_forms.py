from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.forms import StudentCreationForm
from courses.models import Language, Level


class FormsTests(TestCase):
    def test_student_creation_form_with_phone_first_last_name_is_valid(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a")
        form_data = {
            "username": "test",
            "password1": "test1234test",
            "password2": "test1234test",
            "phone_number": "+380001112233",
            "first_name": "Test",
            "last_name": "Testson",
            "student_language": language,
            "student_level": level
        }
        form = StudentCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

#    def test_lesson_creation_form(self):
#        language = Language.objects.create(name="EN")
#        level = Level.objects.create(level="A1", description="a")
#        student = get_user_model().objects.create_user(
#            username="test_student",
#            phone_number="+380001112233",
#            student_language=language,
#            student_level=level
#        )
#        form_data = {
#            "title": "Test title",
#            "language": student.student_language,
#            "level": level,
#        }
#        form = LessonForm(data=form_data)
#        self.assertTrue(form.is_valid())
#        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTest(TestCase):
    def test_student_search_form_by_username(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a")
        self.user = get_user_model().objects.create_user(
            username="test_student",
            password="test1234test",
            phone_number="+380001112233",
            student_language=language,
            student_level=level
        )
        self.client.force_login(self.user)
        search_data = {"username": "test_student"}
        res = self.client.get(
            path=reverse("courses:student-list"),
            data=search_data
        )

        self.assertContains(res, search_data["username"])
