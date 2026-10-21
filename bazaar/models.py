from django.core.exceptions import ValidationError
from django.db import models

from members.models import Member


class Expense(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.date} - {self.title} ({self.amount})"

    def clean(self):
        if self.amount is not None and self.amount < 0:
            raise ValidationError("Expense amount cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
