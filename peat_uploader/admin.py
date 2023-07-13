from django.contrib import admin
from .models import PeatProject, PeatPoint, PeatContractor, UserProfile

admin.site.register(PeatProject)
admin.site.register(UserProfile)
admin.site.register(PeatContractor)
admin.site.register(PeatPoint)

# Register your models here.
