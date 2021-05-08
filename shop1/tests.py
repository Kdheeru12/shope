import pdb
from django.test import TestCase
from graphene.test import Client

from mixer.backend.django import mixer
from .schema import *
from graphql_jwt.testcases import JSONWebTokenTestCase

# Create your tests here.

ALL_PRODUCTS = """
    query{
    allProducts{
        id
        name
        price
        image
        inOffer
        offerPercentage
    }
    }
"""
ALL_CART = """query{
  allCartitems{
    id
    product {
      id
      name
      image
    }
    quantity
    price
    totalPrice
  }
  allWishlistitems {
    id
    product {
      id
      name
      image
      price
    }
  	dateAdded
  }
    
}"""

SEARCH = """query Search($query:String!){
  getSearch(q:$query) {
    id
    name
    price
    image 
  }
}
"""
ORDER_ITEMS = """
query allorderitems($id:ID!){
  allOrderitems(id:$id){
    id
    product {
      id
      name
      image
    }
    quantity
    price
    totalPrice
    
  }
}"""

    
class TestBlogSchema(JSONWebTokenTestCase):

    def setUp(self):
        self.product = mixer.blend(Product)
        self.user = mixer.blend(ExtendUser)
        self.client.authenticate(self.user)
        Customer.objects.create(user=self.user)
        self.order = mixer.blend(Order)
        self.cart = mixer.blend(OrderItem)
        self.wishlist = mixer.blend(WishListItem)

    def test_single_blog_query(self):
        res = self.client.execute(ALL_PRODUCTS)
        ok = res.data.get('allProducts')
        assert ok
    def test_cart(self):
        res = self.client.execute(ALL_CART)
        ok = res.data.get('allCartitems')
    def test_search(self):
        res = self.client.execute(SEARCH,variables={"query":'f' })
        ok = res.data
        assert ok
    def test_order_items(self):
        res = self.client.execute(ORDER_ITEMS,variables={"id":self.order})
    def test_none_orrder(self):
        res1 = self.client.execute(ORDER_ITEMS,variables={"ind":11})
    
