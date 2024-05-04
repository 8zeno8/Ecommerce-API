from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html , urlencode
from django.urls import reverse
from django.db.models.aggregates import Count
from . import models


#inventory filter
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    #function for loocups
    def lookups(self, request, model_admin):
        
        return [
            ('<10' , 'low'),
        ]
    #filtering logic
    def queryset(self, request, queryset):
        
        if self.value() == '<10':
           return queryset.filter(inventory__lt = 10)
       
    
   
    
            
    
#registering products:
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display=['title' , 'unit_price','inventory_status','category']
    list_editable=['unit_price']
    list_filter = ['category','last_update',InventoryFilter]
    list_per_page = 20
    actions = ['clear_inventory']
    prepopulated_fields = {
        'slug' : ['title']
    }
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        elif product.inventory == 0:
            return "Out of stock"
        else:
            return 'OK' 
    
     #clearing inventory(custom action)
    @admin.action(description='clear inventroy')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated."
        )    
        
 
#registering customers
@admin.register(models.Customer)    
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name' , 'last_name','membership']
    list_editable=['membership']
    list_per_page = 20
    ordering = ['first_name' , 'last_name']
    search_fields = ['first_name__startswith' , 'last_name__startswith']
    
#registering categories      
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self,category):
        
        url = (reverse('admin:store_product_changelist')
              + '?' 
              + urlencode({
                  'category__id':str(category.id)
              }))
        
        return format_html('<a href ="{}">{}</a>',url ,category.products_count)
         
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            
            products_count = Count('products')
        )
    
#managing orders
class OrderItemInline(admin.TabularInline):
    search_fields =['product']
    model = models.OrderItem
    extra = 1
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id' , 'placed_at' , 'customer']
    

