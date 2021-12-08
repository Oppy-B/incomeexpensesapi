from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from expenses.models import Expenses
from rest_framework import status,response

# Create your views here.

class ExpenseSummaryStats(APIView):
    def get_amount_for_category(self, expense_list, category):
        expense_list = Expenses.objects.filter(category=category) #RETURN A LIST FILTERED BY THE CATEGORY NAME PROVIDED
        amount = 0

        for expense in expense_list:
            amount += expense.amount

        return {'amount':str(amount)}

    def get_category(self,expense):   #THIS FUNCTION RETURN THE CATEGORY FOR EXPENSES
        return expense.category

    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=30*12)
        expenses = Expenses.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date) # RETURNS A LONG LIST OF EXPENSES

        final= {}

        categories = list(set(map(self.get_category,expenses))) # MAP FUNCTION RUNNING ALL THE LIST OF EXPENSES FOR A YEAR AGO WITH THE CATEGORY FUNCTION

        for expense in expenses:
            for category in categories:
                final[category]= self.get_amount_for_category(expenses, category) # RUN THE TOTAL SUM OF EACH CATEGORY FROM THE EXPNSES LIST
        
        return response.Response({'category_data':final}, status= status.HTTP_200_OK)
