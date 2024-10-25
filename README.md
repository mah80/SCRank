# SCRank

# The Home Page
[![Home Page] (https://github.com/malmukhtar/SCRank/blob/Main/Home%20Page.png)
](https://github.com/mah80/SCRank/issues/19#issuecomment-2437701491)
# Overview
This tool reads the Java source-code files of the project, generates the abstract syntax tree, and navigates it to identify each sensitive classifier (class, interface, enumeration) based on pre-defined keywords dictionary and rules.

# Mechanism
•	For dictionary, it is a collection of keywords that may be used as attribute names in classes, representing sensitive data within the code (e.g., username, password, email, patientId). These keywords are defined by the user based on their understanding of the project domain. The dictionary serves as a customizable tool to flag attributes that are potentially sensitive in the code.

•	For class, it is classified as sensitive if it has at least one sensitive attribute (attribute-based), or it has at least one sensitive method (method-based). The attribute is defined as sensitive if it matches one of the sensitive keywords in the dictionary. The method is defined as sensitive if: it accepts at least one parameter which is an object of a sensitive class (attribute-based), or it has at least one local variable which is an object of a sensitive class (attribute-based), or it accesses one of the sensitive attributes in the same class.

•	For interface, it is classified as sensitive if one of its abstract methods has at least one parameter which is an object of a sensitive class (attribute-based).

•	For enumeration, it is classified as sensitive if it has at least one enum constant which matches one of the sensitive keywords in the dictionary.

# Setup Instructions

Follow these steps to set up and run the Django app locally:

# 1. Clone the Repository and change the directory to the main directory 


# 2. Create a Virtual Environment

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

# 4. Run the Django App

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


# 6. Access the App

Open your web browser and navigate to [http://127.0.0.1:8000/tool](http://127.0.0.1:8000/tool) to view the app.

```
