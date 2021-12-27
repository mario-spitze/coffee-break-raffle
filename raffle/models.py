from django.db import models

# Create your models here.

class Person(models.Model):
    name_text = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name_text

class Event(models.Model):
    event_name_text = models.CharField(max_length=20)

    def __str__(self):
        return self.event_name_text

class Pairing(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    personA = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='personA')
    personB = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='personB')

    cleaning_task = models.BooleanField(default = False)

    def __str__(self):
        return self.event.__str__() + " => " + self.personA.__str__() + " - " + self.personB.__str__()