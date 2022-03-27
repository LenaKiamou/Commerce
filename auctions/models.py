from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title =  models.CharField(max_length = 100)
    image = models.URLField(max_length = 2000, blank=True, null=True)
    description = models.TextField(max_length = 2000)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    starting_bid = models.FloatField()
    status = models.BooleanField(default=True) #active
    current_bid = models.FloatField(null=True, blank=True)
    watchlist_list = models.ManyToManyField(User, null=True, blank=True, related_name="watchlist_items")
    

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} by {self.owner} : {self.description}"


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.content} by {self.author} for: {self.listing}"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    value_offer = models.FloatField(null=True)

    def __str__(self):
        return f"{self.value_offer}"
