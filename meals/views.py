from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MealForm
from .models import Meal


@login_required
def meal_list(request):
    meals = Meal.objects.select_related("member").all()
    return render(request, "meals/meal_list.html", {"meals": meals})


@login_required
def meal_add(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal recorded.")
            return redirect("meal_list")
    else:
        form = MealForm()
    return render(request, "meals/meal_form.html", {"form": form})


@login_required
def meal_edit(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal updated.")
            return redirect("meal_list")
    else:
        form = MealForm(instance=meal)
    return render(
        request, "meals/meal_form.html", {"form": form, "meal": meal}
    )


@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == "POST":
        meal.delete()
        messages.success(request, "Meal deleted.")
    return redirect("meal_list")
