from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def index(request, rec_name):
    servings_count = int(request.GET.get("servings", 1))
    final_data = {key: round(value * servings_count, 2) for key, value in DATA[rec_name].items()}
    context = {
      'recipe': final_data,
    }
    return render(request, 'calculator/index.html', context)
