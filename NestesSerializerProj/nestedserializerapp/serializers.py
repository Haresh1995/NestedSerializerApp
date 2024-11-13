from rest_framework import serializers
from .models import InvoiceModel, InvoiceDetailModel

class InvoiceDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetailModel
        fields = ['id', 'description', 'quantity', 'price', 'line_total']
        read_only_fields = ['line_total']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

class InvoiceModelSerializer(serializers.ModelSerializer):
    details = InvoiceDetailModelSerializer(many=True)

    class Meta:
        model = InvoiceModel
        fields = ['id', 'invoice_number', 'customer_name', 'date', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        invoice = InvoiceModel.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetailModel.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        instance.details.all().delete()
        for detail_data in details_data:
            InvoiceDetailModel.objects.create(invoice=instance, **detail_data)

        return instance
    
    def validate(self, data):
        if 'details' in data and not data['details']:
            raise serializers.ValidationError("Invoice must have at least one detail line.")
        return data