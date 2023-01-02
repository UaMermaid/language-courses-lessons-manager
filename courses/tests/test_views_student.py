from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Language, Level

STUDENT_LIST_URL = reverse("courses:student-list")
STUDENT_DETAIL_URL = reverse("courses:student-detail", args=[1])
STUDENT_CREATE_URL = reverse("courses:student-create")


class PublicStudentTest(TestCase):
    def test_student_list_login_required(self):
        res = self.client.get(STUDENT_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_student_detail_login_required(self):
        res = self.client.get(STUDENT_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_student_create_login_not_required(self):
        res = self.client.get(STUDENT_CREATE_URL)

        self.assertEqual(res.status_code, 200)


class PrivateStudentTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_student",
            password="student1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_student_list(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a1")
        get_user_model().objects.create_user(
            username="test_student_1",
            first_name="first_name_1",
            last_name="last_name_1",
            phone_number="+380001112233",
            student_language=language,
            student_level=level
        )
        get_user_model().objects.create_user(
            username="test_student_2",
            first_name="first_name_2",
            last_name="last_name_2",
            phone_number="+380001112244",
            student_language=language,
            student_level=level
        )

        res = self.client.get(STUDENT_LIST_URL)

        students = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["student_list"]),
            list(students)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="courses/student_list.html"
        )

    def test_retrieve_student_detail(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a1")
        get_user_model().objects.create_user(
            username="test_student_1",
            first_name="first_name_1",
            last_name="last_name_1",
            phone_number="+380001112233",
            student_language=language,
            student_level=level
        )

        res = self.client.get(STUDENT_DETAIL_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            response=res,
            template_name="courses/student_detail.html"
        )
