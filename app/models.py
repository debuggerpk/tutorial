from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    )

ORIENTATION_CHOICES = (
    ('S', 'Straight'),
    ('Bi', 'Bisexial'),
    ('Homo', 'HomeSexual'),
    ('O', 'Other')
    )

RELATIONSHIP_CHOICES = (
    ('S', 'Single'),
    ('IAR', 'In a Relationship'),
    ('M', 'Married'),
    ('E', 'Engaged'),
    ('D', 'Divorced')
    )

INCOME_CHOICES = (
    ('A', 'Below 20K'),
    ('B', 'Below 30K'),
    ('C', 'Below 40K')
    )

INDUSTRY_CHOICES = (
    ('Tech', 'Technology'),
    ('Fashion', 'Fashion'),
    )

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=75)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    accepted_eula = models.BooleanField(default=False)
    #updated eula if terms and conditions change.
    updated_eula = models.BigIntegerField(null=True, blank=True)
    updated_eula_date = models.DateField(null=True, blank=True)
    dob = models.DateField(auto_now=True)
    is_enabled = models.BooleanField(default=False)
    joined_on = models.DateField(auto_now=True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES, default='M')
    hometown = models.ForeignKey(City, related_name='home city',null=True, blank=True)
    current_city = models.ForeignKey(City, related_name='current city', null=True, blank=True)
    cc_since = models.DateField(blank=True, null=True)
    past_cities = models.ManyToManyField(City, related_name='past cities',null=True, blank=True)
    country = models.CharField(max_length=45, null=True, blank=True)
    #on user registration, the country field will be populated automagically, and will not be visible to user.
    #the field is made for making the life easier when querying relationships and data mining fashions relating to regions.
    orientation = models.CharField(max_length=10, default='S', choices=ORIENTATION_CHOICES, null=True, blank=True)
    relationship_status = models.CharField(max_length=10, default='S', choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    income = models.CharField(max_length=10, default='A', choices=INCOME_CHOICES, null=True, blank=True)
    industry = models.CharField(max_length=20, default='Fashion', choices=INDUSTRY_CHOICES, null=True, blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class UserGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    can_op = models.BooleanField(default=True)
    can_swop = models.BooleanField(default=True)

class UserNetwork(models.Model):
    user = models.ForeignKey(User, related_name='person')
    friend = models.ForeignKey(User, related_name='friend')
    group = models.ManyToManyField(UserGroup)
    can_op = models.BooleanField(default=True)
    can_swop = models.BooleanField(default=True)

class Brand(models.Model):
    name = models.CharField(max_length=50)
    catagory = models.CharField(max_length=50)

class UserBrand(models.Model):
    user = models.OneToOneField(User)
    #preferences
    dressing_priority = models.CharField(max_length=15, blank=True, null=True)
    brand_priority = models.CharField(max_length=15, blank=True, null=True)
    shopping_behaviour = models.CharField(max_length=15, blank=True, null=True)
    shopping_habbit = models.CharField(max_length=15, blank=True, null=True)
    #foriegnkeys
    apparel = models.ManyToManyField(Brand, related_name='apparel', blank=True, null=True)
    shoes = models.ManyToManyField(Brand, related_name='shoes', blank=True, null=True)
    jewlery = models.ManyToManyField(Brand, related_name='jewelery', blank=True, null=True)
    accesories = models.ManyToManyField(Brand, related_name='accessories', blank=True, null=True)
    smells = models.ManyToManyField(Brand, related_name='smells', blank=True, null=True)

class OpLink(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(blank=True, null=True, upload_to="/uploads/")
    url = models.URLField(blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField()
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(blank=True, null=True)

class Op(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField()
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(blank=True, null=True)
    brand = models.ForeignKey(Brand, blank=True, null=True)
    price = models.IntegerField(max_length=50)
    currency = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    links = models.ManyToManyField(OpLink, blank=True, null=True)
    #user should be able to tag individuals as well as multiple groups
    tag = models.ManyToManyField(UserNetwork, blank=True, null=True)
    tag_groups = models.ManyToManyField(UserGroup, blank=True, null=True)
    #recieved opinions
    comments = models.ManyToManyField(Comment, blank=True, null=True)