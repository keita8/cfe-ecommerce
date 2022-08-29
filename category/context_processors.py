from .models import *

def mycategories(request):
    categories = Categorie.objects.all()
    return dict(categories=categories)