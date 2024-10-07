# SCRank

## Setup Instructions

Follow these steps to set up and run the Django app locally:

### 1. Clone the Repository and change the directory to the main directory 


### 2. Create a Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies. If you don't have `virtualenv` installed, you can install it using pip:

```bash
pip install virtualenv
```

Create a virtual environment:

```bash
virtualenv venv
```

Activate the virtual environment:

**For Windows:**

```bash
venv\Scripts\activate
```

**For macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Django App

Run the development server:

```bash
python manage.py runserver
```

You should see output similar to the following:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 10, 2024 - 23:00:26
Django version 4.2.3, using settings 'sensitivity_tool.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```


### 6. Access the App

Open your web browser and navigate to [http://127.0.0.1:8000/tool](http://127.0.0.1:8000/tool) to view the app.

```
# Class-Sensitivity-Attributes-and-Methods-Check
This project reads the java source code, generates its abstract syntax tree, and navigates it to identify each sensitive class based on the attributes and methods. The class is classified as sensitive if it has at least one sensitive attribute or it has at least one sensitive method. The attribute is classified a sensitive attribute if it exists in the dictionary of sensitive keywords. The method is classified as sensitive if: it has at least one parameter which is an object from a sensitive class, it has at least one local variable which is an object from a sensitive class, it has an assignment of a sensitive attribute in the same class.
```
