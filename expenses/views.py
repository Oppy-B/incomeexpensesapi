from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializer
from .models import Expenses
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.

class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    # we need to overwrite the method that create an instance of the class above 
    # and tell it which owner it will be that can access this class which will be set to the current active user 

    def perform_create(self, serializer):  # overwrite this method to be the owner
        return serializer.save(owner=self.request.user)

    def get_queryset(self):                # Overwriting this function to return queryset for the current user
        return self.queryset.filter(owner = self.request.user)

class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner) # adding the ISowner class to ensure that the owner and authenticated user is the one accessing this class
                                                                # while ensuring they are the one getting the dataa
    lookup_field = "id"   # get the current user by id

    def perform_create(self, serializer):  # overwrite this method to be the owner
        return serializer.save(owner=self.request.user)

    def get_queryset(self):                # Overwriting this function to return queryset for the current user
        return self.queryset.filter(owner = self.request.user)
