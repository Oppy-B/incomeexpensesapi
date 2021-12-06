from rest_framework import serializers

from .models import Expenses

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = ['id','date', 'description','category','amount']