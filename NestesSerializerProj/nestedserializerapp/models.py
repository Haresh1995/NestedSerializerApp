from django.db import models

class InvoiceModel(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.invoice_number

class InvoiceDetailModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE, related_name='details')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"
