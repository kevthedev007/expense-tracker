from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expense_tracker.app.expenses.views import ExpenseAPIViewSet


router = DefaultRouter()
router.register('', ExpenseAPIViewSet)

app_name = 'expenses'

urlpatterns = [
  path('', include(router.urls))
]
