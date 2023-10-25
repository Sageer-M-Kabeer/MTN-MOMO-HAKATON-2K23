from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Location

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        print("User created successfully!")

        # Create a Location object for the user
        location = Location.objects.create()
        location.save()
        print(f'DEBUG: Location {location} created successfully')

        # Create a Profile object for the user and associate it with the location
        profile = Profile.objects.create(user=instance, location=location)
        print(f'DEBUG: Profile {profile} created successfully')
