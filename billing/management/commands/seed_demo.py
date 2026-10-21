from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from bazaar.models import Expense
from billing.models import Payment
from meals.models import Meal
from members.models import Member


class Command(BaseCommand):
    help = "Load demo members, meals, expenses and payments for the current month."

    def handle(self, *args, **options):
        today = timezone.now().date()

        members = {
            "Rahim": Member.objects.create(
                name="Rahim", phone="01700000001", status="active"
            ),
            "Karim": Member.objects.create(
                name="Karim", phone="01700000002", status="active"
            ),
            "Rahima": Member.objects.create(
                name="Rahima", phone="01700000003", status="active"
            ),
            "Kamal": Member.objects.create(
                name="Kamal", phone="01700000004", status="active"
            ),
        }

        # Meals: a few per member over the current month.
        meal_plan = {
            "Rahim": [1, 2, 3, 4, 5, 6, 7, 8],
            "Karim": [1, 2, 3, 4, 5, 6],
            "Rahima": [1, 2, 3, 4],
            "Kamal": [1, 2, 3, 4, 5, 6, 7],
        }
        for name, days in meal_plan.items():
            for d in days:
                day = min(d, 28)
                Meal.objects.create(
                    member=members[name],
                    date=today.replace(day=day),
                    count=1,
                )

        # Bazaar expenses.
        expenses = [
            ("Rice 5kg", Decimal("650.00")),
            ("Chicken", Decimal("800.00")),
            ("Vegetables", Decimal("450.00")),
            ("Oil & spices", Decimal("520.00")),
        ]
        for i, (title, amount) in enumerate(expenses):
            Expense.objects.create(
                date=today.replace(day=min(i + 1, 28)),
                title=title,
                amount=amount,
                paid_by=members["Rahim"],
            )

        # A payment advance.
        Payment.objects.create(
            member=members["Karim"],
            date=today,
            amount=Decimal("500.00"),
            note="Advance",
        )

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
