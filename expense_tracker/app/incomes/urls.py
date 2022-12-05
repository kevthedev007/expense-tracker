from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expense_tracker.app.incomes.views import IncomeAPIViewSet


router = DefaultRouter()
router.register('', IncomeAPIViewSet)

app_name = 'incomes'

urlpatterns = [
  path('', include(router.urls))
]
