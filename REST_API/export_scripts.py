import pandas as pd
from django.http import HttpResponse
from import_export.resources import modelresource_factory

from .models import ParkingSpace


def export_to_excel(request):
    # Use the model resource to get the data
    ModelResource = modelresource_factory(model=ParkingSpace)
    dataset = ModelResource().export()

    # Convert the dataset to a pandas DataFrame
    df = pd.DataFrame(dataset.dict)

    # Create an HttpResponse with the appropriate Excel headers
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    # Use pandas to write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
