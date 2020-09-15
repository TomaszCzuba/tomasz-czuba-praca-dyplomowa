from django.contrib import admin
from .models import Przepis, Skladniki, Dodatkowe, Zakupy, ZakupyElementy, Customer

# Register your models here.

#admin.site.register(Przepis)

@admin.register(Przepis)
class PrzepisAdmin(admin.ModelAdmin):
    list_display = ["nazwa","edytowane"]

admin.site.register(Skladniki)
admin.site.register(Dodatkowe)
admin.site.register(Zakupy)
admin.site.register(ZakupyElementy)
admin.site.register(Customer)
