from rest_framework import serializers
from .models import Player, Match, Goal

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class GoalInputSerializer(serializers.Serializer):
    last_name = serializers.CharField()
    count = serializers.IntegerField(default=1)

class GoalSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.last_name', read_only=True)

    class Meta:
        model = Goal
        fields = ['player_name', 'count']


class MatchSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    scorers = GoalInputSerializer(many=True, write_only=True)

    class Meta:
        model = Match
        fields = ['id', 'opponent', 'is_home', 'result', 'match_date', 'scorers', 'goals']

    def create(self, validated_data):
        scorers_data = validated_data.pop('scorers', [])
        match = Match.objects.create(**validated_data)

        for scorer in scorers_data:
            last_name = scorer['last_name']
            count = scorer['count']

            try:
                player = Player.objects.get(last_name__iexact=last_name)
                Goal.objects.create(match=match, player=player, count=count)
            except Player.DoesNotExist:
                continue

        return match

