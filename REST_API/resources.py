from import_export import resources

from REST_API.models import ParkingSpace


class ParkingSpaceResourse(resources.ModelResource):

    class Meta:
        model = ParkingSpace
        fields = ['id', 'name', 'number', 'rate', 'occupied']
        skip_unchanged = True
        use_bulk = True
