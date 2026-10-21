from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "amount", "paid_by")
    list_filter = ("date",)
    search_fields = ("title", "paid_by__name")
    date_hierarchy = "date"
