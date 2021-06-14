from django.db.models.query import QuerySet
from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Q

from .models import (
    Category,
    Destination,
    CategoryDestination,
    City,
    District,
    Room,
    ServiceType,
    Convenience,
    RoomConvenience,
    Dinning,
    FoodType,
    DinningOption,
    Product,
    ProductImage,
    )

class CategoryView(View):
    def get(self, request):
        try: 
            category = [
                {
                    'name'        : category.name,
                    'image_url'   : category.image_url
                    } for category in Category.objects.all()
                ]
            return JsonResponse({'message' : category}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class ProductListView(View):
    def get(self, request):
        try:
            
            order_condition = request.GET.get('order')
            is_room     = request.GET.get('is_room', None)
            is_dinning  = request.GET.get('is_dinning', None)
            is_activity = request.GET.get('is_activity', None)
            limit        = int(request.GET.get('limit', 0))
            offset       = int(request.GET.get('offset', 0))
            
            q = Q()
            
            if is_room:
                q = Q(is_room=True)
                
            if is_dinning:
                q = Q(is_dinning=True)
                
            if is_activity:
                q = Q(is_activity=True)
                
            products = Product.objects.filter(q)
            
            if order_condition == 'min_price':
                products = products.order_by('price')
                
            if order_condition == 'max_price':
                products = products.order_by('-price')
                
            if order_condition == 'rating':
                products = products.order_by('-rating')
                
            # ordering_type ={
            #     'min_price' : 'price',
            #     'max_price' : '-price',
                
            # }
            
            #  products = Product.objects.filter(q).order_by(ordering_type[order_condition])

            product_list = [
                    {
                        'name'        : product.name,
                        'rating'      : product.rating,
                        'city'        : product.city.name,
                        'district'    : product.district.name,
                        'price'       : product.price,
                        'image'       : product.productimage_set.first().image_url,
                        'room_type'   : product.room.room_type.name if is_room else None,
                        'star_rating' : product.room.star_rating if is_room else None,
                        'dining_type' : product.dinning.dinning_type.name if is_dinning else None,
                        'food_type'   : product.dinning.food_type.name if is_dinning else None
                        } for product in products
                    ][offset:offset+limit]
            
            return JsonResponse({'message' : product_list}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class ProductDetailView(View):
    def get(self, request, product_id = None):
        
        if not product_id or not Product.objects.filter(id=product_id):
            return JsonResponse({'message' : 'NOTHING_PRODUCT'}, status=400)
        
        product = Product.objects.get(id=product_id)
        
        product_list = []
        
        if Product.objects.filter(id=product_id):

            product_list.append(
            {
                'name'        : product.name,
                'rating'      : product.rating,
                'description' : product.description,
                'address'     : product.address,
                'latitude'    : product.latitude,
                'longitude'   : product.longitude,
                'city'        : product.city.name,
                'district'    : product.district.name,
                'price'       : product.price,
                'is_room'     : product.is_room,
                'is_dinning'  : product.is_dinning,
                'image' : [
                    {'image_url' : image.image_url} for image in product.productimage_set.all()]
                } 
                            )
        
        if Product.objects.filter(id=product_id, is_room=True):
            
            product_list.append(
                {
                'room_type'   : product.room.room_type.name,
                'star_rating' : product.room.star_rating,
                'convenience' : [
                    {
                        'name'         : convenience.name,
                        'service_type' : convenience.service_type.name
                        } for convenience in product.room.convenience.all()]
                    }
                                )
            
            return JsonResponse({'message' : product_list}, status=200)

        if Product.objects.filter(id=product_id, is_dinning=True):
            product_list.append(
                {
                'food_type'    : product.dinning.food_type.name,
                'dinning_type' : product.dinning.dinning_type.name
                    }
                )

            return JsonResponse({'message' : product_list}, status=200)
        
        if Product.objects.filter(id=product_id, is_activity=True):
            return JsonResponse({'message' : product_list}, status=200)
            
        return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

# class FilterView(View):
#     def get(self, request):
#         print(request)
#         try:
#             order_condition = request.GET.get('order')
#             is_room         = request.GET.get('is_room', None)
#             is_dinning      = request.GET.get('is_dinning', None)
#             is_activity     = request.GET.get('is_activity', None)

#             q = Q()
            
#             if is_room:
#                 q = Q(is_room=True)
                
#             if is_dinning:
#                 q = Q(is_dinning=True)
                
#             if is_activity:
#                 q = Q(is_activity=True)

#             products = Product.objects.filter(q)
            
#             if order_condition == 'min_price':
#                 products = products.order_by('price')
                
#             if order_condition == 'max_price':
#                 products = products.order_by('-price')
                
#             if order_condition == 'rating':
#                 products = products.order_by('-rating')
                
#             print(products)
#             print(order_condition)

#             result = [
#                 {
#                     'name'        : product.name,
#                     'rating'      : product.rating,
#                     'description' : product.description,
#                     'address'     : product.address,
#                     'latitude'    : product.latitude,
#                     'longitude'   : product.longitude,
#                     'city'        : product.city.name,
#                     'district'    : product.district.name,
#                     'price'       : product.price,
#                     } for product in products
#                 ]
#             return JsonResponse({'message' : result}, status=200)
            
#         except:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)