from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from billing.services import calculate_bill
from bazaar.models import Expense
from meals.models import Meal
from members.models import Member


class MealModelTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Rahim", status="active")

    def test_meal_saved(self):
        meal = Meal.objects.create(
            member=self.member, date=date(2026, 10, 1), count=2
        )
        self.assertEqual(meal.count, 2)

    def test_count_must_be_at_least_one(self):
        meal = Meal(member=self.member, date=date(2026, 10, 1), count=0)
        with self.assertRaises(ValidationError):
            meal.save()

    def test_inactive_member_rejected(self):
        self.member.status = Member.Status.INACTIVE
        self.member.save()
        meal = Meal(member=self.member, date=date(2026, 10, 1), count=1)
        with self.assertRaises(ValidationError):
            meal.save()

    def test_duplicate_member_date_rejected(self):
        Meal.objects.create(
            member=self.member, date=date(2026, 10, 1), count=1
        )
        duplicate = Meal(
            member=self.member, date=date(2026, 10, 1), count=2
        )
        with self.assertRaises(ValidationError):
            duplicate.save()


class BillCalculationTests(TestCase):
    def setUp(self):
        self.a = Member.objects.create(name="A", status="active")
        self.b = Member.objects.create(name="B", status="active")
        self.inactive = Member.objects.create(name="X", status="inactive")

    def _add_meals(self):
        # A eats 6 meals, B eats 4 meals in Oct 2026 -> total 10
        for i in range(6):
            Meal.objects.create(
                member=self.a, date=date(2026, 10, i + 1), count=1
            )
        for i in range(4):
            Meal.objects.create(
                member=self.b, date=date(2026, 10, i + 1), count=1
            )

    def test_meal_rate_and_share(self):
        self._add_meals()
        Expense.objects.create(
            date=date(2026, 10, 1), title="Rice", amount=Decimal("100.00")
        )
        summary = calculate_bill(2026, 10)

        self.assertEqual(summary.total_meals, 10)
        self.assertEqual(summary.total_expense, Decimal("100.00"))
        self.assertEqual(summary.meal_rate, Decimal("10.00"))
        self.assertEqual(summary.total_share, Decimal("100.00"))

        shares = {m.member.name: m.share for m in summary.members}
        self.assertEqual(shares["A"], Decimal("60.00"))
        self.assertEqual(shares["B"], Decimal("40.00"))

    def test_no_meals_gives_zero_rate(self):
        Expense.objects.create(
            date=date(2026, 10, 1), title="Rice", amount=Decimal("100.00")
        )
        summary = calculate_bill(2026, 10)
        self.assertEqual(summary.meal_rate, Decimal("0.00"))
        self.assertEqual(summary.total_share, Decimal("0.00"))

    def test_inactive_member_excluded(self):
        self._add_meals()
        summary = calculate_bill(2026, 10)
        self.assertEqual(len(summary.members), 2)
        self.assertNotIn(self.inactive, [m.member for m in summary.members])

    def test_payment_reduces_due(self):
        self._add_meals()
        Expense.objects.create(
            date=date(2026, 10, 1), title="Rice", amount=Decimal("100.00")
        )
        from billing.models import Payment

        Payment.objects.create(
            member=self.a, date=date(2026, 10, 2), amount=Decimal("30.00")
        )
        summary = calculate_bill(2026, 10)
        shares = {m.member.name: m for m in summary.members}
        self.assertEqual(shares["A"].due, Decimal("30.00"))
        self.assertEqual(summary.total_paid, Decimal("30.00"))

    def test_only_selected_month_counted(self):
        self._add_meals()
        # Meals in September must not count for October.
        Meal.objects.create(
            member=self.a, date=date(2026, 9, 15), count=10
        )
        Expense.objects.create(
            date=date(2026, 10, 1), title="Rice", amount=Decimal("100.00")
        )
        summary = calculate_bill(2026, 10)
        self.assertEqual(summary.total_meals, 10)
