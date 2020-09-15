from django.shortcuts import render, get_object_or_404, redirect
from .models import Przepis, Skladniki, ZakupyElementy, Zakupy, Customer
from .forms import PrzepisForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import JsonResponse
import json

# Create your views here.


def przepisy(request):
    # return HttpResponse("<h1>To jest nasz pierwszy test</h1>")
    # test = "To jest cos we views"
    skladniki = list(Skladniki.objects.all())  # lista wszystkich skladnikow, do autouzupelniania
    wszystkie = Przepis.objects.all()
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        z = q.split('%2C+')  # rozdzielanie odebranych danych
        y = [n.replace(', ', " ") for n in z] # zamiana przecinka i spacji na sama spacje
        m = ' '.join(y) # laczenie elementow w stringa i rozdzielenie ich spacja
        u = list(m.split(" ")) # rozdzielenie stringow oraz utworzenie z nich listy
        del u[-1]
        for x in u:
            przepis = Przepis.objects.filter(skladniki__nazwa__contains=x)
        zawartosc = przepis.order_by('-stopien_trudnosci')
        template_name = 'search.html'
    else:
        template_name = 'przepisy.html'
        zawartosc = {}

    return render(request, template_name, {'skladniki': skladniki, 'przepis': zawartosc, 'wszystkie': wszystkie})

@login_required
def nowy_przepis(request):
    form = PrzepisForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(przepisy)
    return render(request, 'nowy_przepis.html',{'form': form})

@login_required
def edytuj_przepis(request, id):
    przepis = get_object_or_404(Przepis, pk=id)
    form = PrzepisForm(request.POST or None, request.FILES or None, instance=przepis)
    if form.is_valid():
        form.save()
        return redirect(przepisy)
    return render(request, 'nowy_przepis.html', {'form': form})

@login_required
def usun_przepis(request, id):
    przepis = get_object_or_404(Przepis, pk=id)

    if request.method == "POST":
        przepis.delete()
        return redirect(przepisy)

    return render(request, 'potwierdz.html', {'przepis': przepis})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zostało utworzone. Teraz możesz się zalogować {username}!')
            return redirect('przepisy')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def search(request):
    template_name = 'search.html'
    return render(request, template_name)

def koszyk(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Zakupy.objects.get_or_create(klient=customer, zakonczone=False)
        items = order.zakupyelementy_set.all()
    else:
        items = []

    context = {'items':items}
    return render(request, 'koszyk.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Przepis.objects.get(id=productId)
    order, created = Zakupy.objects.get_or_create(klient=customer, zakonczone=False)

    orderItem, created = ZakupyElementy.objects.get_or_create(zakupy=order, element=product)

    if action == 'add':
        orderItem.ilosc = (orderItem.ilosc + 1)
    elif action == 'remove':
        orderItem.ilosc = (orderItem.ilosc - 1)

    orderItem.save()

    if orderItem.ilosc <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)