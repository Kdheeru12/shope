from django.db import models
import graphene 
from graphene import Node,relay, Connection, ConnectionField
from graphql_auth import mutations
from graphql_auth.schema import UserQuery,MeQuery
from graphene_django import DjangoObjectType, fields
from .models import ExtendUser
from .models import *
from graphene_django.filter import DjangoFilterConnectionField
import datetime
from graphql import GraphQLError
import graphql_social_auth

# from django.db.models import Q


# from .utils import cookieCart,cartData,guestOrder


class Users(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields= ('email','id',)

class Products(DjangoObjectType):
    class Meta:
        model= Product
        fields: ('__all__')
        

class OrderItems(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields: ('__all__') 
class ShippingAddresses(DjangoObjectType):
    class Meta:
        model = ShippingAddress
        fields: ('__all__')
class WishListItems(DjangoObjectType):
    class Meta:
        model = WishListItem
        field: ('__all__')
class Orders(DjangoObjectType):
    class Meta:
        model=Order
        fields:('__all__')
        


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    social_auth = graphql_social_auth.SocialAuthJWT.Field()

class Query(UserQuery,MeQuery,graphene.ObjectType):
    all_users = graphene.List(Users)
    all_products = graphene.List(Products)
    all_cartItems = graphene.List(OrderItems)
    all_orderItems = graphene.List(OrderItems,id = graphene.ID())
    all_wishlistitems = graphene.List(WishListItems)
    get_product = graphene.Field(Products,id = graphene.ID())
    get_search = graphene.List(Products,q=graphene.String())
    get_order = graphene.List(Orders,id = graphene.ID())
    get_shipping = graphene.Field(ShippingAddresses,id = graphene.ID())
    def resolve_all_users(root,info):
        return ExtendUser.objects.all()
    def resolve_all_products(root,info):
        return Product.objects.all()
    def resolve_all_cartItems(root,info):
        if info.context.user.is_authenticated:
            # print('ddd')
            try:
                customer = info.context.user.customer
            except:
                customer = Customer.objects.create(user=info.context.user,)
            order,created = Order.objects.get_or_create(customer=customer,complete=False)
            # print(order)
            # print(created)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            return cartItems
        else:
            raise Exception('unauthorized')
        # if info.context.user.is_authenticated:
        #     return Product.objects.all()
        # else:
        #     return Product.objects.none()
    def resolve_all_orderItems(root,info,id=None):
        print(id)
        if info.context.user.is_authenticated:
            if id:
                return OrderItem.objects.filter(order=id)
            else:
                return 'failed'
        else:
            raise Exception('unauthorized')
    def resolve_all_wishlistitems(self, info):
        if info.context.user.is_authenticated:
            return WishListItem.objects.filter(customer=info.context.user.customer)
        else:
            raise Exception('unauthorized')
    def resolve_get_product(self,info,id=None):
        if id:
            try:
                return Product.objects.get(id=id)
            except:
                return 'invalid Id'
        else:
            return 'failed'
    def resolve_get_search(self,info,q):
        search_list = Product.objects.filter(
            name__icontains = q
        )
        return search_list
    def resolve_get_order(self,info,id=None):
        if info.context.user.is_authenticated:
            customer = info.context.user.customer
            if id != None:
                return Order.objects.filter(id=id)
            else:
                return Order.objects.filter(customer=customer,complete=True).order_by('-date_orderd')
        else:
            raise Exception('unauthorized')
    def resolve_get_shipping(self,info,id=None):
        if info.context.user.is_authenticated:
            return ShippingAddress.objects.get(id=id)
        else:
            raise Exception('unauthorized')
class AddMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        action = graphene.String()

    items = graphene.String()
    @classmethod
    def mutate(cls,root,info,id,action):
        product = Product.objects.get(pk=id)
        customer = info.context.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        print(order)
        orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        if product.in_offer:
            orderItem.price=float(product.price -(product.price*product.offer_percentage)/100)
            orderItem.total_price=float(orderItem.quantity*(product.price -(product.price*product.offer_percentage)/100))
        else:
            orderItem.price=float(product.price)
            orderItem.total_price=float(orderItem.quantity*product.price)
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
        elif action == 'delete':
            orderItem.delete()
            print('aaa')
        print(orderItem)
        return AddMutation(items='Success')
class CashOrderMutation(graphene.Mutation):
    class Arguments:
        address = graphene.String()
        city  = graphene.String()
        state = graphene.String()
        zipcode = graphene.String()
        total = graphene.Float()
        phone = graphene.String()

    response = graphene.ID()
    @classmethod
    def mutate(cls,root,info,total,address,city,state,zipcode,phone):
        customer = info.context.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        transaction_id = datetime.datetime.now().timestamp()
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            a = True
            order.complete = True
            order.ordertotal = total
        if a == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = address,
                city =city,
                state = state,
                zipcode = zipcode,
                phone = phone
            )
            order.save()
            print(a)

            return CashOrderMutation(response=order)
        else:
            return CashOrderMutation(response= 'failed')

class AddWishList(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    response = graphene.String()
    @classmethod
    def mutate(cls,root,info,id):
        print(id)
        customer = info.context.user.customer
        product = Product.objects.get(pk=id)
        try:
            item = WishListItem.objects.get(product=product)
        except:
            item = None
        if item:
            WishListItem.delete(item)
            return AddWishList(response = 'removed')
        else:
            WishListItem.objects.create(
                customer = customer,
                product = product
            )
            return AddWishList(response = 'added')
                    
class Mutation(AuthMutation,graphene.ObjectType):
    update_order = AddMutation.Field()
    cash_complete_order = CashOrderMutation.Field()
    add_wish_list = AddWishList.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)