from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from courses.models import Student, Language, Lesson, Level


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "phone_number",
                    )
                },
            ),
        )
    )


admin.site.register(Language)
admin.site.register(Level)
admin.site.register(Lesson)
