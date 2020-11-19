from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer, OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer_class = OrderUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for order in instance.order_detail.all():
            order.product.stock += order.quantity 
            order.product.save()
        instance.delete()