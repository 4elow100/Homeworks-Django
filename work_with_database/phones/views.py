from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_dict = {
        'id': 'id',
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }
    sort_mode = request.GET.get('sort', 'id')
    template = 'catalog.html'
    phones = Phone.objects.all().order_by(sort_dict[sort_mode])
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {
        'phone': Phone.objects.get(slug=slug)
    }
    return render(request, template, context)
