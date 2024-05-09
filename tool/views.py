from django.shortcuts import render
from tool.SensitivityTool.Sensitivity import analyzer
import time

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
import os
import subprocess
import shutil
from django.contrib.auth.decorators import login_required
from zipfile import ZipFile
from django.contrib.auth import authenticate, login, logout


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
            # #Check prject and delete it at the end
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
        
        # Go to results page
            return render(request, "tool/home.html")

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