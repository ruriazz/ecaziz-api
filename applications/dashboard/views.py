from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.utils.handlers import is_authenticated

from usecases.dashboard.get_dashboard_data import get_dashboard_data


class DashboardView:
    
    @api_view(['GET'])
    @is_authenticated
    def index(request) -> Response:
        return get_dashboard_data()