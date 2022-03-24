from core.utils.serializers import DynamicFieldsModelSerializer
from applications.ucapan.models import Ucapan

class UcapanSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Ucapan
        fields = '__all__'