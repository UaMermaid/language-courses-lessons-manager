from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Language, Level

LEVEL_LIST_URL = reverse("courses:level-list")


class PublicLeveLTest(TestCase):
    def test_level_list_login_required(self):
        res = self.client.get(LEVEL_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateLevelTest(TestCase):
    def setUp(self) -> None:
        language = Language.objects.create(name="EN")
        self.user = get_user_model().objects.create_user(
            username="test_level",
            password="test1234test",
            student_language=language
        )
        self.client.force_login(self.user)

    def test_retrieve_level_list(self):
        level1 = Level.objects.create(level="A1", description="a1")
        level2 = Level.objects.create(level="A2", description="a2")

        res = self.client.get(LEVEL_LIST_URL)
        levels = [level1, level2]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["level_list"]),
            list(levels)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="courses/level_list.html"
        )
