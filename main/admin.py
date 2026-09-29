from django.contrib import admin

from .models import City, House


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'broker', 'price', 'room_count', 'area', 'created_at')
    list_filter = ('city', 'type', 'created_at')
    search_fields = ('title', 'address', 'description')
    list_per_page = 20