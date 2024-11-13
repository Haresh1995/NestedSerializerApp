from django.contrib import admin
from .models import InvoiceDetailModel, InvoiceModel

admin.site.register(InvoiceDetailModel)
admin.site.register(InvoiceModel)


