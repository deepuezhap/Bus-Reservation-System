from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    contact = models.TextField(null=True)

   
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, created, instance, **kwargs):
    if not created:
        instance.profile.save()



class Location(models.Model):

    location = models.CharField(max_length=255)
    def __str__(self):
        return self.location
    
class Bus(models.Model):

    bname = models.CharField(max_length=255)
    source = models.ForeignKey(Location,on_delete=models.CASCADE ,related_name="source")
    dest = models.ForeignKey(Location, on_delete=models.CASCADE,related_name="dest")
    nos = models.IntegerField()
    fare = models.FloatField()
    departure_time = models.TimeField(auto_now=False, auto_now_add=False)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    bus_operator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.bname


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    number = models.IntegerField()

@receiver(post_save, sender=Bus)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for seat_number in range(1, instance.nos + 1):
            instance.seat_set.create(number=seat_number)
    
class Booking(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seatno = models.IntegerField()
    status = models.BooleanField(default=False)
    price= models.FloatField(null=True)
    departure_date = models.DateField()
    booked_date = models.DateTimeField(auto_now=False, auto_now_add=True)







    
    


