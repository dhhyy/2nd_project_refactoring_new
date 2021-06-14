from django.db    import models
from django.db.models.query import QuerySet

class Category(models.Model):
    name        = models.CharField(max_length=45)
    image_url   = models.URLField(max_length=2000)
    destination = models.ManyToManyField('Destination', through='CategoryDestination')
    
    class Meta:
        db_table = 'categories'

class Destination(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)
    
    class Meta:
        db_table = 'destinations'

class CategoryDestination(models.Model):
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'category_destinations'


class City(models.Model):
    name = models.CharField(max_length=45, null=True)
    
    class Meta:
        db_table = 'cities'

class District(models.Model):
    name = models.CharField(max_length=45)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'districts'

class RoomType(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'room_types'

class Room(models.Model):
    star_rating = models.SmallIntegerField(default=0)
    room_type   = models.ForeignKey('RoomType', on_delete=models.SET_NULL,null=True)
    convenience = models.ManyToManyField('Convenience', through='RoomConvenience')
    
    class Meta:
        db_table = 'rooms'

class ServiceType(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'service_types'

class Convenience(models.Model):
    name         = models.CharField(max_length=45)
    service_type = models.ForeignKey('ServiceType', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'conveniences'

class RoomConvenience(models.Model):
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE)
    convenience  = models.ForeignKey('Convenience', on_delete=models.CASCADE)
    room         = models.ForeignKey('Room', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'room_conveniences'

class DinningType(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'dinning_types'

class FoodType(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'food_types'

class Dinning(models.Model):
    dinning_type = models.ForeignKey('DinningType', on_delete=models.SET_NULL, null=True)
    food_type    = models.ForeignKey('FoodType', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'dinnings'

class DinningOption(models.Model):
    name        = models.CharField(max_length=45)
    price       = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.TextField()
    dinning     = models.ForeignKey('Dinning', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'dinning_options'

class Product(models.Model):
    name        = models.CharField(max_length=45)
    rating      = models.DecimalField(max_digits=3,decimal_places=1)
    description = models.TextField()
    address     = models.CharField(max_length=100)
    latitude    = models.DecimalField(max_digits=20, decimal_places=17)
    longitude   = models.DecimalField(max_digits=20, decimal_places=17)
    category    = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey('Destination', on_delete=models.SET_NULL, null=True)
    city        = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    district    = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)
    price       = models.DecimalField(max_digits=18, decimal_places=2)
    is_room     = models.BooleanField(default=False)
    room        = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    is_dinning  = models.BooleanField(default=False)
    dinning     = models.ForeignKey('Dinning', on_delete=models.SET_NULL, null=True)
    is_popular  = models.BooleanField(default=0)
    is_activity = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'product_images'

class Review(models.Model):
    dinning     = models.ForeignKey('Dinning', on_delete=models.CASCADE)
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment     = models.TextField()
    star_rating = models.SmallIntegerField(default=0)
    
    class Meta:
        db_table = 'reviews'