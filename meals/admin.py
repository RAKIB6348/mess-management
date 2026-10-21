from django.contrib import admin

from .models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("member", "date", "count", "note")
    list_filter = ("date",)
    search_fields = ("member__name",)
    date_hierarchy = "date"
