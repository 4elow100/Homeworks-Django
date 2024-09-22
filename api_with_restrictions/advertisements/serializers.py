from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        message_lim = 'Превышен лимит(10) открытых объявлений'
        current_user_id = self.context['request'].user.id
        adv_open_count = len(Advertisement.objects.all().filter(creator_id=current_user_id, status='OPEN'))
        if self.context["request"].method == "POST":
            if adv_open_count == 10:
                raise serializers.ValidationError(message_lim)
        elif self.context["request"].method in ["PATCH", "PUT"]:
            if data['status'] == 'OPEN' and adv_open_count == 10:
                raise serializers.ValidationError(message_lim)
        return data
