from django.db import models

class Country(models.TextChoices):
    NIGERIA = 'NGIGERIA'
    GHANA = 'GHANA'

class State(models.TextChoices):
    Abia = 'Umuahia'	
    Adamawa = 'Yola'
    Akwa_Ibom = 'Uyo'
    Anambra = 'Awka'
    Bauchi = 'Bauchi'
    # Bayelsa
    # Benue
    # Borno
    # Cross River
    # Delta
    # Ebonyi
    # Edo
    # Ekiti
    # Enugu
    # Gombe
    # Imo
    # Jigawa
    # Kaduna
    # Kano
    # Katsina
    # Kebbi
    # Kogi
    # Kwara
    # Lagos
    # Nasarawa
    # Niger
    # Ogun
    # Ondo
    # Osun
    # Oyo
    # Plateau
    # Rivers
    # Sokoto
    # Taraba
    # Yobe
    # Zamfara
    # Territory
    # Federal Capital Territory


class City(models.TextChoices):
    IKEJA = 'IKJ'

class Local_gov(models.TextChoices):
    pass

class Gender(models.TextChoices):
    NONE = ""
    MALE = 'M'
    FEMALE = 'F'
