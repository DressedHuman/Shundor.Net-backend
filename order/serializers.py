from rest_framework import serializers
from .models import Order, OrderItem


# Orders can have multiple items, each with its own details
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("id", "total_amount")

    def create(self, validated_data):
        """
        Create an order. `serializer.save(...)` may merge extra kwargs
        (like `user`) into `validated_data` before `create` is called,
        so we pop `user` out if present to avoid passing it twice to
        `Order.objects.create()`.

        Supports guest orders when `user` is None.
        """
        items_data = validated_data.pop("items", [])

        # DRF merges serializer.save(kwargs) into validated_data. Pop 'user'
        # if present so we don't pass it twice when creating the model.
        user = validated_data.pop("user", None)

        # Calculate total_amount
        total = 0
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            total += product.price * quantity

        order = Order.objects.create(user=user, total_amount=total, **validated_data)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data["product"],
                quantity=item_data["quantity"],
                price=item_data["product"].price,
            )

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

