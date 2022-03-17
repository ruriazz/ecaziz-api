from core.utils.serializers import DynamicFieldsModelSerializer
from applications.users.models import User

# TODO: serializers.UserSerializer
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
