from django.urls import path
from pracaDyplomowaAplikacja.views import przepisy, nowy_przepis, edytuj_przepis, usun_przepis, register, updateItem, koszyk

urlpatterns = [
    path('',przepisy,name="przepisy"),
    path('nowy/',nowy_przepis,name="nowy_przepis"),
    path('edytuj/<int:id>/',edytuj_przepis, name="edytuj_przepis"),
    path('usun/<int:id>/',usun_przepis, name="usun_przepis"),
    path('update_item/', updateItem, name="update_item"),
]