from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Lesson, Language, Level

LESSON_LIST_URL = reverse("courses:lesson-list")
LESSON_DETAIL_URL = reverse("courses:lesson-detail", args=[1])


class PublicCarTest(TestCase):
    def test_lesson_list_login_required(self):
        res = self.client.get(LESSON_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_lesson_detail_login_required(self):
        res = self.client.get(LESSON_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_student",
            password="test1234test"
        )
        self.client.force_login(self.user)

    def test_retrieve_lesson_list(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a1")
        lesson1 = Lesson.objects.create(
            title="Test title",
            language=language,
            level=level
        )

        res = self.client.get(LESSON_LIST_URL)
        lessons = [lesson1]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["lesson_list"]),
            list(lessons)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="courses/lesson_list.html"
        )

    def test_retrieve_lesson_detail(self):
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a1")
        Lesson.objects.create(
            title="Test title 2",
            language=language,
            level=level
        )

        res = self.client.get(LESSON_DETAIL_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            response=res,
            template_name="courses/lesson_detail.html"
        )
