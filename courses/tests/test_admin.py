from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from courses.models import Language, Level


class AdminSiteCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin4321"
        )
        self.client.force_login(self.admin_user)
        language = Language.objects.create(name="EN")
        level = Level.objects.create(level="A1", description="a")
        self.student = get_user_model().objects.create_user(
            username="test_student",
            password="test1234Test",
            phone_number="+380001112233",
            student_language=language,
            student_level=level
        )

    def test_student_phone_number_listed(self):
        url = reverse("admin:courses_student_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.student.phone_number)

    def test_student_detailed_phone_number_listed(self):
        url = reverse("admin:courses_student_change", args=[self.student.id])
        res = self.client.get(url)

        self.assertContains(res, self.student.phone_number)
