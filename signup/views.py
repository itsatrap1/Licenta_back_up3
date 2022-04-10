from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(response):
    if response.method == "POST":
        form = SignupForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignupForm()
    return render(response, "signup/signup.html", {"form": form})
