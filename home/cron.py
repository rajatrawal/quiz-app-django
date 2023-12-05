from . models import Category
import random

def print_hello():
        number = random.randint(0,100)
        Category.objects.get_or_create(name = number)    