from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "status", "joined_date")
    list_filter = ("status",)
    search_fields = ("name", "phone", "email")
