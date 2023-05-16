# Rule Creator App

This is a web application for creating rules for data processing. The rules are created based on templates and can be customized with exceptions.

![Layout de la aplicación](app-titulos/assets/imgs/app_layout.png)

## Technologies Used
The app was built with the following technologies:

Python 3.9
Dash 2.0.0
Pandas 1.5.2
Numpy 1.23.5
Matplotlib
Seaborn 0.12.1
Openpyxl
Tqdm
Google-auth
Gspread
Bootstrap 5.1.3
The specific versions of each package used can be found in the `environment.yml` file.

## How to Run the App
1. Clone this repository to your local machine
2. Create a new virtual environment using conda or venv and activate it
3. Install the dependencies listed in the environment.yml file by running the following command in your terminal:

```conda env create -f environment.yml```

4. Once the environment is created, activate it:

```conda activate title```

5. Run the app by executing the following command in your terminal:

```python app.py```

6. Open your web browser and go to http://127.0.0.1:8050/ to see the app running.

## How to Use the App

1. Select a template from the dropdown menu
2. Add fields to the template by clicking on the "Add Field" button and filling in the required information
3. Customize the fields with exceptions by clicking on the "Add Exception" button and selecting the desired options
4. Click on the "Create Rule" button to generate the rule
5. The rule will be displayed on the screen and can be copied to Excel by clicking on the "Copy to Excel" button

## App Structure
The app is divided into six rows, each with its own set of callbacks:
1. Selecting a template
2. Adding fields to the template and displaying the "Add Field" button
3. Customizing fields with exceptions and displaying the "Add Exception" and "Create Rule" buttons
4. Adding exceptions to the rule
5. Displaying the created rule and copying it to Excel
6. Placeholder row for future functionality

