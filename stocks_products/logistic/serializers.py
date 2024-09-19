from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address'] + ['positions']

    def create(self, validated_data):
        print(validated_data)
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults=dict(
                    quantity=position['quantity'],
                    price=position['price']
                )
            )
        return stock
