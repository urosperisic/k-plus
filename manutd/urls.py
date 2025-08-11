from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, MatchViewSet

router = DefaultRouter()
router.register('players', PlayerViewSet)
router.register('matches', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
