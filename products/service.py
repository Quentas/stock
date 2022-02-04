import string
import random
from .models import *

def random_string(to_exclude):  
    letters = string.ascii_letters + string.digits
    result = ''.join((random.sample(letters, 20)))
    if result in to_exclude:
        random_string(to_exclude)
    return result  