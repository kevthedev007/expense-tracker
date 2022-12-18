from rest_framework.permissions import IsAuthenticated
from expense_tracker.util.permissions import IsOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action

from expense_tracker.app.expenses.models import Expense
from expense_tracker.app.incomes.models import Income



def get_amount_for_category(expenses_list, category):
  expenses = expenses_list.filter(category=category)
  amount = 0
  for expense in expenses:
    amount += expense.amount
  return {'amount': str(amount)}  

def get_amount_from_source(income_list, source):
  incomes = income_list.filter(source=source)
  amount = 0
  for income in incomes:
    amount += income.amount
  return {'amount': str(amount)}



# Create your views here.
class ExpenseStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = Expense.objects.all()
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated, IsOwner]
  
  def get_queryset(self):
    return self.queryset.filter(owner = self.request.user)
    
  
  @action(methods=["get"], detail=False, url_path="monthly-expense-summary")
  def monthly_expense_summary(self, request, *args, **kwargs):
    month = request.query_params.get("month")
    
    if not month:
      return Response({ 'error': "Please select a period"})
    
    expenses = self.get_queryset().filter(date__month = month)
      
    if not expenses:
      return Response({ 'message': 'No Expenses for month'})
    
    final = {}
    categories = list(set(map(lambda a: a.category, expenses)))
    
    for expense in expenses:
      for category in categories:
        final[category] = get_amount_for_category(expenses, category)
        
    return Response({'category_data': final}, status=status.HTTP_200_OK)
  
  @action(methods=["get"], detail=False, url_path="yearly-expense-summary")
  def yearly_expense_summary(self, request, *args, **kwargs):
    year = request.query_params.get("year")
    
    if not year:
      return Response({ 'error': "Please select a period"})
      
    expenses = self.get_queryset().filter(date__year = year)
    
    if not expenses:
      return Response({ 'message': 'No Expenses for month'})
    
    final = {}
    categories = list(set(map(lambda a: a.category, expenses)))
    
    for expense in expenses:
      for category in categories:
        final[category] = get_amount_for_category(expenses, category)
        
    return Response({'category_data': final}, status=status.HTTP_200_OK)
  
  
  
class IncomeStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = Income.objects.all()
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated, IsOwner]
  
  def get_queryset(self):
    return self.queryset.filter(owner = self.request.user)
  
  @action(methods=['get'], detail=False, url_path='monthly-income-summary')
  def monthly_income_summary(self, request, *args, **kwargs):
    month = request.query_params.get("month")
 
    if not month:
      return Response({ 'error': "Please select a period"})
  
    incomes = self.get_queryset().filter(date__month = month)
    
    if not incomes:
      return Response({ 'message': 'No Income for month'})
    
    final = {}
    sources = list(set(map(lambda a: a.source, incomes)))
    
    for income in incomes:
      for source in sources:
        final[source] = get_amount_from_source(incomes, source)
        
    return Response({'income_source_data': final}, status=status.HTTP_200_OK)
  
  @action(methods=['get'], detail=False, url_path='yearly-income-summary')
  def yearly_income_summary(self, request, *args, **kwargs):
    year = request.query_params.get("year")
    
    if not year:
      return Response({ 'error': "Please select a period"})
      
    incomes = self.get_queryset().filter(date__year = year)
    
    if not incomes:
      return Response({ 'message': 'No Income for month'})
    
    final = {}
    sources = list(set(map(lambda a: a.source, incomes)))
    
    for income in incomes:
      for source in sources:
        final[source] = get_amount_from_source(incomes, source)
        
    return Response({'income_source_data': final}, status=status.HTTP_200_OK)
    
  
  

    
    
    
    
  
  
