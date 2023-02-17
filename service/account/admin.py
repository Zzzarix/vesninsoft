from django.contrib import admin
from .models import *

admin.site.register(
    [
        User,
        Company,
        PayslipRegistry,
        PayslipSheet
    ]
)

# Register your models here.
