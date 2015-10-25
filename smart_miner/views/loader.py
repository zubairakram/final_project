import csv

from django.shortcuts import render
from django.views.generic.base import View

from final_project.settings import MEDIA_ROOT
from smart_miner.forms import UploadForm


class Loader(View):
    """
    This class contains method for collecting data from file and parse the data.
    and the save the data in data base.
    """
    template = "upload.html"
    form = UploadForm
    context= {
              'form': form,
              'error': '',
              'success': '',
    }
    
    def __reset_context(self):
        "Private method resets the context values to defaults."
        self.context['error'] =''
        self.context['success']= ''
        
    def __process_file(self, file):
        "csv file writer"
        with open(MEDIA_ROOT + 'data.csv', 'wb+') as fout:
            for i in file.chunks():
                fout.write(i)

    def post(self, request):
        form = self.form(request.POST, request.FILES)        
        self.__reset_context()
        self.context['form'] = form
    
        if form.is_valid():
            self.__process_file(request.FILES['file'])
            self.context["success"] = 'Uploaded successfully!'
            return render(request, self.template, self.context)
        else:
            self.context['error'] = "cannot upload file!"
            return render(request, self.template, self.context)

    def get(self, request):
            form = self.form()
            self.__reset_context()
            self.context['form'] = form
            return render(request, self.template, self.context)

def read_csv():
    'read csv file from media directory and return in the form of table'
    file = MEDIA_ROOT+"data.csv"
    with open(file) as fin:
        return list(csv.reader(fin))
        