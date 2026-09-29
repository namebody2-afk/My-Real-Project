from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import City, House


def home(request):
    houses = House.objects.select_related('city').all().order_by('-created_at')
    cities = City.objects.annotate(
        house_count=Count('houses')
    ).order_by('-house_count', 'name')
    agents = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    return render(request, "index.html", {
        "houses": houses,
        "cities": cities,
        "agents": agents,
    })


def about(request):
    return render(request, 'about.html')


def agent(request):
    agents = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    return render(request, "agent.html", {"agents": agents})


def services(request):
    return render(request, "services.html")


def contacts(request):
    return render(request, "contact.html")


@login_required(login_url='/auth/login')
def add_house(request):
    cities = City.objects.all().order_by('name')
    if request.method == "POST":
        try:
            House.objects.create(
                img=request.FILES.get('img'),
                type=request.POST.get('type', 'Sale'),
                price=request.POST.get('price') or 0,
                city_id=request.POST.get('city') or None,
                address=request.POST.get('address', '').strip(),
                description=request.POST.get('description', '').strip(),
                room_count=request.POST.get('room_count') or 1,
                floor=request.POST.get('floor') or 1,
                floor_count=request.POST.get('floor_count') or 1,
                area=request.POST.get('area') or 0,
                title=request.POST.get('title', '').strip(),
                broker=request.user,
            )
            return redirect('home')
        except Exception as e:
            return render(request, "add_house.html", {"cities": cities, "error": str(e)})
    return render(request, "add_house.html", {"cities": cities})