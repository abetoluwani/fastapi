from dataclasses import field
from itertools import product
from operator import index
from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime
from  tortoise.contrib.pydantic import pydantic_model_creator

# Creating The Database

class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=255, null = False) #the null indicates that the field cannot be empty
    email = fields.CharField(max_length=255, null = False)
    password = fields.CharField(max_length=255, null = False)
    is_verified = fields.BooleanField(default = False)
    joined = fields.DatetimeField(auto_now_add = True, default=datetime.utcnow)


class Business(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255, null = False, unique=True)
    city = fields.CharField(max_length=255, null = False)
    region = fields.CharField(max_length=255, null = False)
    country = fields.CharField(max_length=255, null = False)
    business_type = fields.CharField(max_length=255, null = False)
    business_description = fields.TextField(max_length=255, null = True)
    logo = fields.CharField(max_length=255, null = False)
    owner = fields.ForeignKeyField('models.User', related_name='business') # this is because the business should be a user also


class Product(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255, null = False)
    image = fields.CharField(max_length=255, null = False)
    price = fields.DecimalField(max_digits=10, decimal_places=2, null = False)
    category = fields.CharField(max_length=255, null = False, index= True)
    new_price = fields.DecimalField(max_digits=10, decimal_places=2, null = True)
    percentage_discount = fields.DecimalField(max_digits=5, decimal_places=2, null = True)
    offer_expiration_date = fields.DatetimeField(auto_now_add = True, default=datetime.utcnow)
    business = fields.ForeignKeyField('models.Business', related_name='products')


user_pydantic = pydantic_model_creator(User, name= 'User', exclude= ("is_verified",))
user_pydanticIn = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name='UserOut', exclude=('password'))


business_pydantic= pydantic_model_creator(Business, name='Business')
business_pydanticIn = pydantic_model_creator(Business, name='BusinessIn', exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name='Product')
product_pydanticIn = pydantic_model_creator(Product, name='ProductIn', exclude=('percentage_discount'))