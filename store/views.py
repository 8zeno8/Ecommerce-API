from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import status
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from .serializers import * 
from .models import *
from .filters import ProductFilter
from .pgination import DefaultPgaination



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPgaination
    search_fields = ['title','description','category__title']
    ordering_fields = ['unit_price','last_update']
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count()>0:
            return Response({'error: product cannot be deleted because it is associated with order item.'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
     
    
class CategoryViewSet(ModelViewSet):
    queryset =  Category.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CategorySerializer 
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.products_count > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more product item(s).'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
    

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id ': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer 
    

class CartItemViewSet(ModelViewSet):
    
    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method =='POST':
            return AddCartItemSerializer
        elif self.request.method =='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    serializer_class = CartItemSerializer
    
    def get_serializer_context(self):
        return{'cart_id':self.kwargs['cart_pk']}
        
    def get_queryset(self):
        return CartItem.objects.\
            filter(cart_id = self.kwargs['cart_pk']).\
            select_related('product')    
    
     