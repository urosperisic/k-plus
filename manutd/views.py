from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample

from .models import Player, Match
from .serializers import PlayerSerializer, MatchSerializer
from .permissions import IsAdminUserRole

@extend_schema(tags=["Players"])
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUserRole()]


@extend_schema(
    tags=["Matches"],
    request=MatchSerializer,
    examples=[
        OpenApiExample(
            name="Example Match Input with Last Names",
            value={
                "opponent": "Chelsea",
                "is_home": "H",
                "result": "2:1",
                "match_date": "2025-08-11",
                "scorers": [
                    {"last_name": "Højlund", "count": 2}
                ]
            },
            request_only=True,
        )
    ]
)
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUserRole()]
