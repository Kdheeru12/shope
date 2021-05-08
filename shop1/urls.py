from django.urls import path,include 
from django.conf import settings
import graphql
from .import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('h/',views.hello),
    path("graphl",csrf_exempt(GraphQLView.as_view(graphiql=True)))

]