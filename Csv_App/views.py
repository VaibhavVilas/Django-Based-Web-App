from django.shortcuts import render
from .Modules import data_analysis
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import os

# allowed file extension
DATASET_EXTENSIONS = {'csv'}

# function to check whether uploaded file is of allowed extension


def allowed_dataset_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in DATASET_EXTENSIONS

# to exempt the view function from CSRF protection


@csrf_exempt
# function to handle Http request to URL mentioned in urls.py
def home(request):

    # to handle POST request made by the user
    if request.method == 'POST':
        # to intialize the form with the POST data and files submitted by the user
        form = UploadForm(request.POST, request.FILES)
        # to check if the form is valid
        if form.is_valid():

            # assigning uploaded file with 'file'  key to a variable
            csv_file = request.FILES['file']

            # to check if the uploaded file is a csv
            if allowed_dataset_file(csv_file.name):

                # to save the csv file uploaded by the user
                fs = FileSystemStorage()
                csv_name = fs.save(csv_file.name, csv_file)
                csv_path = fs.path(csv_name)

                # performing actual analysis on the csv file
                result = data_analysis.perform(csv_path)

                # after getting our results, we delete the csv file
                if os.path.exists(csv_path):
                    os.remove(csv_path)

                # preparing context with analysis results, so we can render via html
                context = {
                    'head': result['head'],
                    'structure': result['structure'],
                    'description': result['description'],
                    'median': result['median'],
                    'check_missing_values': result['check_missing_values'],
                    'plots': result['plots']
                }

                # render result template with context values
                return render(request, 'result.html', context)

    # render upload template for GET request
    return render(request, 'upload.html')
