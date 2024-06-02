from django.contrib import admin
from .models import User, Doctor, Review

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Review)