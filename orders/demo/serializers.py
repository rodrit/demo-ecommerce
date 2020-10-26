from rest_framework import serializers
from .models import Product, Order, OrderDetail
from django.core.exceptions import ObjectDoesNotExist


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['cuantity', 'price', 'product']



class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, required=True)
    total = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = Order
        fields = ['id','date_time', 'details', 'total']


    def create(self, validated_data):
        '''
        Overrided create function to validate and save order data and child OrderDetail data
        '''
        detail_list = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail in detail_list:
            OrderDetail.objects.create(order=order,product=detail.pop('product'), **detail)
        return order

    def update(self,instance, validated_data):
        '''
        Overrided function to custom update order data
        '''
        detail_list = validated_data.pop('details')
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.save()
        updated_products = []
        current_products = [detail.product for detail in instance.details.all()]
        for detail in detail_list:
            if OrderDetail.objects.filter(product=detail['product'], order=instance):
                d = OrderDetail.objects.get(product=detail['product'], order=instance)
                d.cuantity = detail['cuantity']
                d.save()
            else:
                d = OrderDetail.objects.create(**detail, order=instance)
                d.save()
            updated_products.append(detail['product'].pk)
        for product in current_products:
            if product.pk not in updated_products:
                d = OrderDetail.objects.get(order=instance, product=product)
                d.delete()
        return instance

    def validate_details(self, value):
        '''
        Checks positive values for quantities and non-repetitive products for each order detail
        '''
        products = []
        for detail in value:
            try:
                if detail['cuantity'] <= 0:
                    raise serializers.ValidationError("Quantity product must me positive. Product: {}".format(detail['product']))
                if detail['product'].pk in products and 'product' in detail.keys():
                    raise serializers.ValidationError("Products must be different in orders. Product repeated: {}".format(detail['product']))
                else:
                    products.append(detail['product'].pk)
            except KeyError:
                raise serializers.ValidationError("Order detail needs no-empty cuantity and product fields")
        return value


    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['details'] = OrderDetailSerializer(instance.details.all(), many=True).data
        return representation
