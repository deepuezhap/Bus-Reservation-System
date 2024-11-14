from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Bus,Location,Profile,Booking
from .forms import BusForm,ProfileForm

class BusAdmin(admin.ModelAdmin):
    form = BusForm
    list_display = ('bname','source','dest','fare')




class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ('user','contact')

    def get_queryset(self, request):
        # Only show profiles belonging to the 'bus_operator' group
        qs = super().get_queryset(request)
        return qs.filter(user__groups__name='bus_operator')
    


# Register your models here.
admin.site.register(Bus,BusAdmin)
admin.site.register(Location)
admin.site.register(Profile,ProfileAdmin)

