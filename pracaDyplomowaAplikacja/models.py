from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/pl/3.0/ref/models/fields/

#model składników
class Skladniki(models.Model):
    TYP = {
        (0, 'brak wybranego typu'),
        (1, 'Warzywo'),
        (2, 'Przyprawa'),
        (3, 'Mieso'),
        (4, 'Ryba'),
        (5, 'Owoc'),
        (6, 'Owoce morza'),
    }
    nazwa = models.CharField(max_length=64, blank=False,unique=True)
    typ = models.PositiveSmallIntegerField(default=0, choices=TYP)

    def __str__(self):
        return self.nazwa


#Głowny model
class Przepis(models.Model):
    nazwa = models.CharField(max_length=64, blank=False, unique=True)
    opis = models.TextField(default="", null=True, blank=True)
    zdjecie = models.ImageField(upload_to="zdjecia", null=True, blank=True)
    data_dodania = models.DateField(auto_now_add=True,editable=False)
    edytowane = models.DateField(auto_now=True,editable=False)
    czas_przygotowania = models.DurationField(default=0, blank=True)
    stopien_trudnosci = models.DecimalField(max_digits=4, decimal_places=2)
    #relacja z modelem Skladniki
    skladniki = models.ManyToManyField(Skladniki, through='Dodatkowe')

    def __str__(self):
        return self.nazwa

class Dodatkowe(models.Model):
    skladnik = models.ForeignKey(Skladniki, on_delete=models.CASCADE, blank=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, blank=True)
    ilosc = models.IntegerField()

class Customer(models.Model):
    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nazwa = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.nazwa


class Zakupy(models.Model):
   klient = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
   data_utworzenia = models.DateTimeField(auto_now_add=True)
   zakonczone = models.BooleanField(default=False, null=True, blank=False)
   zakupy_id = models.CharField(max_length=200, null=True)

   def __str__(self):
       return str(self.id)


class ZakupyElementy(models.Model):
    element = models.ForeignKey(Przepis, on_delete=models.SET_NULL, blank=True, null=True)
    zakupy = models.ForeignKey(Zakupy, on_delete=models.SET_NULL, blank=True, null=True)
    ilosc = models.IntegerField(default=0, null=True, blank=True)
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ilosc)