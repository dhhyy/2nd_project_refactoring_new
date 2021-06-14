import json
import unittest

from logging     import disable
from os          import CLD_EXITED
from django.http import response
from django.test import TestCase, Client, testcases

from .models     import Category, CategoryDestination, City, Convenience, Destination, District, Product, ProductImage, RoomConvenience, RoomType, Room, ServiceType


client = Client()

class CategoryTest(TestCase):
    def setUp(self):
        Category.objects.create(
            name        = "숙박업소",
            image_url   = "test_url",
        )
        
        Destination.objects.create(
            name = '부산',
            image_url = 'test_url'
        )
        
        CategoryDestination.objects.create(
            category = Category.objects.get(id=1),
            destination = Destination.objects.get(id=1)
        )
    
    def tearDown(self):
        Category.objects.all().delete()
        Destination.objects.all().delete()
        CategoryDestination.objects.all().delete()
    
    def test_success_category(self):
        
        category = [
            {
            'name'      : '숙박업소',
            'image_url' : 'test_url',
            }
                    ]
        
        response = client.get('/products/category')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message':category})
        
class ProductListTest(TestCase):
    def setUp(self):
        
        Category.objects.create(
            name        = '숙박업소',
            image_url   = 'test_url',
        )
        
        Destination.objects.create(
            name      = '부산',
            image_url = 'test_url'
        )
        
        CategoryDestination.objects.create(
            category    = Category.objects.get(name='숙박업소'),
            destination = Destination.objects.get(name='부산')
        )
        
        City.objects.create(
            name = '부산'
        )

        District.objects.create(
            name = '해운대구',
            city = City.objects.get(name='부산')
        )
        
        RoomType.objects.create(
            name = '호텔'
        )
        
        Room.objects.create(
            star_rating = 5,
            room_type   = RoomType.objects.get(name='호텔'),
        )
        
        ServiceType.objects.create(
            name = '시설'
        )
        
        Convenience.objects.create(
            name         = 'wifi',
            service_type = ServiceType.objects.get(name='시설')
        )
        
        RoomConvenience.objects.create(
            service_type = ServiceType.objects.get(name='시설'),
            convenience  = Convenience.objects.get(name='wifi'),
            room         = Room.objects.get(star_rating=5)
        )
        
        Product.objects.create(
            name        = '부산 호텔',
            rating      = 9.1,
            description = '좋은 호텔',
            address     = '부산시 해운대구',
            latitude    = 35.1553354579046,
            longitude   = 129.124772824535,
            category    = Category.objects.get(name='숙박업소'),
            destination = Destination.objects.get(name='부산'),
            city        = City.objects.get(name='부산'),
            district    = District.objects.get(name='해운대구'),
            price       = 101010.00,
            # 스트링 처리. 
            is_room     = True,
            room        = Room.objects.get(star_rating=5)
            # is_dinning  = models.BooleanField(default=False)
            # dinning     = models.ForeignKey('Dinning', on_delete=models.SET_NULL, null=True)
            # is_popular  = models.BooleanField(default=0)
            # is_activity = models.BooleanField(default=0)
        )
        
        ProductImage.objects.create(
            image_url = 'test_url',
            product  = Product.objects.get(name='부산 호텔')
        )
        
        # print(Category.objects.get(id=2).id)
        
    def tearDown(self):
        Category.objects.all().delete()
        Destination.objects.all().delete()
        CategoryDestination.objects.all().delete()
        City.objects.all().delete()
        District.objects.all().delete()
        RoomType.objects.all().delete()
        Room.objects.all().delete()
        ServiceType.objects.all().delete()
        Convenience.objects.all().delete()
        RoomConvenience.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        
    def test_succuss_product_list(self):

        product_list = [
            {
            "name": "부산 호텔",
            "rating": "9.1",
            "city": "부산",
            "district": "해운대구",
            "price": "101010.00",
            "image": "test_url",
            "room_type": "호텔",
            "star_rating": 5,
            "dining_type": None,
            "food_type": None
        }
            ]

        response = client.get('/products?is_room=True&offset=0&limit=1&order=max_price')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message':product_list})
        
class ProductDetailTest(TestCase):
    
    def setUp(self):
        Category.objects.create(
            name        = '숙박업소',
            image_url   = 'test_url',
        )
        
        Destination.objects.create(
            name      = '부산',
            image_url = 'test_url'
        )
        
        CategoryDestination.objects.create(
            category    = Category.objects.get(name='숙박업소'),
            destination = Destination.objects.get(name='부산')
        )
        
        City.objects.create(
            name = '부산'
        )

        District.objects.create(
            name = '해운대구',
            city = City.objects.get(name='부산')
        )
        
        RoomType.objects.create(
            name = '호텔'
        )
        
        Room.objects.create(
            star_rating = 5,
            room_type   = RoomType.objects.get(name='호텔'),
        )
        
        ServiceType.objects.create(
            name = '시설'
        )
        
        Convenience.objects.create(
            name         = 'wifi',
            service_type = ServiceType.objects.get(name='시설')
        )
        
        RoomConvenience.objects.create(
            service_type = ServiceType.objects.get(name='시설'),
            convenience  = Convenience.objects.get(name='wifi'),
            room         = Room.objects.get(star_rating=5)
        )
        
        Product.objects.create(
            name        = '부산 호텔',
            rating      = 9.1,
            description = '좋은 호텔',
            address     = '부산시 해운대구',
            #latitude    = 35.1553354579046,
            latitude    = '35.0000000000000',
            #longitude   = 129.124772824535,
            longitude   = '129.000000000000',
            category    = Category.objects.get(name='숙박업소'),
            destination = Destination.objects.get(name='부산'),
            city        = City.objects.get(name='부산'),
            district    = District.objects.get(name='해운대구'),
            price       = 101010.00,
            # 스트링 처리. 
            is_room     = True,
            room        = Room.objects.get(star_rating=5)
            # is_dinning  = models.BooleanField(default=False)
            # dinning     = models.ForeignKey('Dinning', on_delete=models.SET_NULL, null=True)
            # is_popular  = models.BooleanField(default=0)
            # is_activity = models.BooleanField(default=0)
        )
        
        ProductImage.objects.create(
            image_url = 'test_url',
            product = Product.objects.get(name='부산 호텔')
        )
        
    def tearDown(self):
        Category.objects.all().delete()
        Destination.objects.all().delete()
        CategoryDestination.objects.all().delete()
        City.objects.all().delete()
        District.objects.all().delete()
        RoomType.objects.all().delete()
        Room.objects.all().delete()
        ServiceType.objects.all().delete()
        Convenience.objects.all().delete()
        RoomConvenience.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
    
    def test_success_product_detail_list(self):
        
        product_list = [
            {'name': '부산 호텔', 
             'rating': '9.1', 
             'description': '좋은 호텔', 
             'address': '부산시 해운대구', 
             'latitude': '35.00000000000000000', 
             'longitude': '129.00000000000000000', 
             'city': '부산', 
             'district': '해운대구', 
             'price': '101010.00', 
             'is_room': True, 
             'is_dinning': False, 
             'image': [
                 {
                     'image_url': 'test_url'
                     }
                 ]
             },
            
            {
                'room_type': '호텔', 
                'star_rating': 5,
                'convenience': [
                    {
                        'name': 'wifi', 
                        'service_type': '시설'
                        }
                    ]
                }
            ]
        
        # product_list = [
        #     {
        #                 "name": "부산 호텔",
        #                 "rating": "9.1",
        #                 "description": "좋은 호텔",
        #                 "address": "부산시 해운대구",
        #                 "latitude": '35.00000000000000000',
        #                 "longitude": '129.00000000000000000',
        #                 "city": "부산",
        #                 "district": "해운대구",
        #                 "price": "101010.00",
        #                 "is_room": True,
        #                 "is_dinning": False,
        #                 "image": [
        #                     {
        #                         "image_url": "https://i.travelapi.com/hotels/1000000/800000/793900/793876/cf20fa42_z.jpg"
        #                         },
        #                     {
        #                         "image_url": "https://i.travelapi.com/hotels/1000000/800000/793900/793876/3734b004_z.jpg"
        #                         }
        #                     ]
        #                 },
        #             {
        #                 "room_type": "호텔",
        #                 "star_rating": 5,
        #                 "convenience": [
        #                     {
        #                         "name": "무료 WiFi",
        #                         "service_type": "인터넷"
        #                         }

        #                     ]
        #                 }
        #             ]
                
        response = client.get('/products/1')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message':product_list})
         
if __name__ == '__main__':
    unittest.main()


# AssertionError: 
# {'mes[114 chars]000000000', 'longitude': '129.0000000000000000[228 chars]}]}]} 
# != 
# {'mes[114 chars]00000', 'longitude': '129.000000000000', 'city[382 chars]}]}]}