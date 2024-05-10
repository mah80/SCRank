from django.shortcuts import render
from tool.SensitivityTool.Sensitivity import analyzer
import time


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from pathlib import Path
import os
import subprocess
import shutil
from django.contrib.auth.decorators import login_required
from zipfile import ZipFile
from django.contrib.auth import authenticate, login, logout

import pandas as pd
import zipfile
from django.core.files import File
from .models import *


@login_required(login_url='login')
def index(request):
    messages = []
    return render(request, "tool/home.html")

@login_required(login_url='login')
def git_process(request):
    messages = []
    if request.method == 'POST':
        # print(request.POST.get("GitHub_repo"))
        if request.POST.get("GitHub_repo"):
            # time.sleep(1000)
            print(request.POST.get("GitHub_repo"))
            BASE_DIR = Path(__file__).resolve().parent
            WORKING_DIR = os.path.join(BASE_DIR, "SensitivityTool", 'projects')
            if not os.path.exists(WORKING_DIR):
                os.makedirs(WORKING_DIR)
            os.chdir(WORKING_DIR)
            
            # # Get repo URL 
            repo_url = request.POST.get("GitHub_repo")

            projectID = repo_url.rsplit('/', 1)[1]+ "-"+ str(int(time.time() * 1000))
            project_path =  os.path.join(WORKING_DIR, repo_url.rsplit('/', 1)[1])
            # print(1,project_path)
            try:
                subprocess.check_output(['git', 'clone', repo_url])
            except subprocess.CalledProcessError as e:
                print('Cloning failed:', e)
                # message.append(f'Cloning failed: {e}')
                messages.append(f'Cloning failed please make sure the repository exists, and is publicly available.')
                print(project_path)
                if os.path.exists(project_path):
                    shutil.rmtree(project_path)
                context = {'messages':messages}
                return render(request, "tool/home.html",context=context)
            
            os.chdir(os.path.join(BASE_DIR, "SensitivityTool"))
            # try:
            #call the backend function
            output = analyzer(project_path, projectID)
            # except Exception as e:
            #     print(e)

            print(output)

            files_to_zip = []
            for root, dirs, files in os.walk(output):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, output)
                    files_to_zip.append((relative_path, open(file_path, 'rb').read()))

            # Create a temporary zip file
            zip_file_path = f'output/{project_path.split("/")[-1]}.zip'  
            print(zip_file_path)
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                for file_name, file_content in files_to_zip:
                    zip_file.writestr(file_name, file_content)
            
            if request.user.is_authenticated:
                username = request.user
            else:
                username = None
            
            obj= Job.objects.create(
                                user=username, 
                                name= f'{project_path.split("/")[-1]}.zip'
                            )
            with open(zip_file_path,mode="rb") as f:
                obj.result = File(f, name=f'{project_path.split("/")[-1]}.zip')
                obj.save()
            


            # Bar Chart
            df = pd.read_csv(os.path.join(output,"Sorted Normalized Type Statistic.csv"))

            # Extract class names and sensitivity levels
            class_names = df['CLASS NAME'].tolist()
            sensitivity_levels = df['SENSITIVITY LEVEL'].tolist()


            # Pie Chart 
            df = pd.read_csv(os.path.join(output,"Statistics.csv"))

            # Prepare the data for Chart.js
            total_classes = df['NUMBER OF CLASSES'].iloc[0]
            sensitive_classes = df['NUMBER OF SENSITIVE CLASSES'].iloc[0]
            non_sensitive_classes = total_classes - sensitive_classes

            # Prepare the data for Chart.js for attributes and sensitive attributes
            total_attributes = df['NUMBER OF ATTRIBUTES'].iloc[0]
            sensitive_attributes = df['NUMBER OF SENSITIVE ATTRIBUTES'].iloc[0]
            non_sensitive_attributes = total_attributes - sensitive_attributes

            # Prepare the data for Chart.js for methods and sensitive methods
            total_methods = df['NUMBER OF METHODS'].iloc[0]
            sensitive_methods = df['NUMBER OF SENSITIVE METHODS'].iloc[0]
            non_sensitive_methods = total_methods - sensitive_methods

            data = {
                'labels': ['Sensitive Classes', 'Non-sensitive Classes'],
                'values': [sensitive_classes, non_sensitive_classes],
                'labels_attributes': ['Sensitive Attributes', 'Non-sensitive Attributes'],
                'values_attributes': [sensitive_attributes, non_sensitive_attributes],
                'labels_methods': ['Sensitive Methods', 'Non-sensitive Methods'],
                'values_methods': [sensitive_methods, non_sensitive_methods],
                'class_names': class_names,
                'sensitivity_levels': sensitivity_levels,
            }

            # #Check prject and delete it at the end
            if os.path.exists(project_path):
                try:
                    shutil.rmtree(project_path)
                except Exception as e:
                    print(e)
            
            if os.path.exists(output):
                try:
                    shutil.rmtree(output)
                except Exception as e:
                    print(e)
        
        # Go to results page
            return render(request, "tool/results.html", context={'data': data, 'zip': f'{project_path.split("/")[-1]}.zip'})

        else:
            messages.append("No repository link or file was provided!")
            context = {'messages':messages}
            return render(request, "tool/home.html",context=context)

@login_required(login_url='login')       
def zip_process(request):
    messages = []
    if request.method == 'POST':
        if request.FILES['zip_file']:
            if not request.FILES['zip_file'].name.endswith(".zip"):
                messages.append(f'This is not a ZIP file.')
                print("This is not a ZIP file.")
                context = {'messages':messages}
                return render(request, "tool/home.html",context=context)
            zip_file = request.FILES['zip_file']
            # uploaded_file = request.FILES['file']
            file_name = zip_file.name
            BASE_DIR = Path(__file__).resolve().parent
            WORKING_DIR = os.path.join(BASE_DIR, "SensitivityTool", 'projects')
            file_path = os.path.join(WORKING_DIR, file_name[:-4] + "-" + str(int(time.time() * 1000)))
            print(file_path)
            with ZipFile(zip_file) as zObject:
                zObject.extractall(path=f"{file_path}")
            # with open(file_path, 'wb+') as f:
            #     for chunk in uploaded_file.chunks():
            #         f.write(chunk)

            #call the backend function
            output = analyzer(file_path)

            print(output)
            # #Check prject and delete it at the end
            if os.path.exists(file_path):
                shutil.rmtree(file_path)

            return render(request, "tool/home.html")
            # return HttpResponse("File uploaded to: "+ file_path)
            
    else:
        messages.append("No repository link or file was provided!")
        context = {'messages':messages}
        return render(request, "tool/home.html",context=context)


@login_required(login_url='login')
def report_view(request):   
    return render(request, "tool/reports.html")

# def login_view(request):
    
#     if request.method == 'POST':
#         print("Here")
#         return HttpResponseRedirect(reverse('index'))

    
#     return render(request, "tool/login.html")

def login_view(request):
    message = None

    if request.method == 'POST':

        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            message = ('invalid credentials!')

    #if GET request
    #if user is logged in already
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    return render(request, "tool/login.html", {'message': message})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def logging(log):
    #Will update late
    print(log)

def download_zip(request, name):
    # Retrieve the Job instance
    job = Job.objects.filter(name=name, user__username=request.user)[0]
    BASE_DIR = Path(__file__).resolve().parent
    os.chdir(os.path.join(BASE_DIR, "SensitivityTool"))
    # Open the zip file associated with the Job instance
    if job:
        with open(os.path.join('output',job.name), 'rb') as zip_file:
            # Create a response with the zip file contents
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{job.result.name}"'

    return response