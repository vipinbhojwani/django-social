
from django.shortcuts import render, redirect
from .forms import TweetForm
from .models import Tweet, Profile
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    form = TweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("advik:dashboard")
    
    followed_tweets = Tweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request, 
        "advik/dashboard.html",
        {"form": form, "tweets": followed_tweets},
        )


@login_required
def profile_list(request):
    if not request.user.is_authenticated:
        profiles = Profile.objects.all()
    else:
        profiles = Profile.objects.exclude(user = request.user)
    return render(request, "advik/profile_list.html", {"profiles": profiles})


@login_required
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user = request.user)
        missing_profile.save()
    profile = Profile.objects.get(pk = pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "advik/profile.html", {"profile": profile})