from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Language, Level

LANGUAGE_LIST_URL = reverse("courses:language-list")
LANGUAGE_DETAIL_URL = reverse("courses:language-detail", args=[1])


class PublicLanguageTest(TestCase):
    def test_language_list_login_required(self):
        res = self.client.get(LANGUAGE_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_language_detail_login_required(self):
        res = self.client.get(LANGUAGE_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateLanguageTest(TestCase):
    def setUp(self) -> None:
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="1", description="test")
        self.user = get_user_model().objects.create_user(
            username="test_level",
            password="test1234test",
            student_language=language,
            student_level=level
        )
        self.client.force_login(self.user)

    def test_retrieve_language_list(self):
        Language.objects.create(name="UA")
        Language.objects.create(name="PL")

        res = self.client.get(LANGUAGE_LIST_URL)
        languages = []
        for language in Language.objects.all():
            languages.append(language)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["language_list"]),
            list(languages)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="courses/language_list.html"
        )

    def test_retrieve_language_detail(self):

        res = self.client.get(LANGUAGE_DETAIL_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            response=res,
            template_name="courses/language_detail.html"
        )
