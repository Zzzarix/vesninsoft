from django.contrib import admin
from .models import *

admin.site.register(
    [
        User,
        Company,
        PayslipRegistry,
        PayslipSheet,
        CompanyAdmin
    ]
)

# Register your models here.
