from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("member", "date", "amount", "note")
    list_filter = ("date",)
    search_fields = ("member__name",)
    date_hierarchy = "date"
