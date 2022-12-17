from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expense_tracker.app.stats.views import ExpenseStatsViewSet, IncomeStatsViewSet

router = DefaultRouter()
router.register('', ExpenseStatsViewSet)
router.register('', IncomeStatsViewSet)

urlpatterns = [
  path('', include(router.urls))
]