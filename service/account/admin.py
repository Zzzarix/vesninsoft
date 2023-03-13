from django.contrib import admin
from account.models import *

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
