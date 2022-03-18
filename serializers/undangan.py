from core.utils.serializers import DynamicFieldsModelSerializer
from applications.undangan.models import Undangan

# TODO: serializers.UserSerializer
class UndanganSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Undangan
        fields = '__all__'
