from core.utils.serializers import DynamicFieldsModelSerializer
from .models import User

# TODO: serializers.UserSerializer
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
