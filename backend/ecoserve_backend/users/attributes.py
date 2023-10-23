from django.db import models

class Country(models.TextChoices):
    NGIGERIA = 'NGIGERIA'
    GHANA = 'GHANA'

class State(models.TextChoices):
    ABUJA = 'ABJ'
    KANO = 'KN'
    LAGOS = 'LG'

class City(models.TextChoices):
    pass

class Local_gov(models.TextChoices):
    pass

class Gender(models.TextChoices):
    MALE = 'M'
    FEMALE = 'F'
