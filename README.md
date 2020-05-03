# clinic
#### Refugee Clinic Management System
Includes two main modules (which are not complete yet):
1. **Clinic calendar:** To be used in the reception desk
  	- Shows scheduled appointments
  	- Query a day and view it's scheduled appointments
  	- Create / edit patients
  	- Create / edit appointment
  	- Add doctor time slot in system (doctor's shift hours)
  
2. **Doctor interface:** The doctor's "home-page"
  	- Shows all of today's scheduled appointments
  	- Query a patient
  	- links to patient interface - view the medical record of a patient
  	- Start session (between doctor and patient during an appointment)
  	- Prescribe medications (and export copy for patient)
  	- Ask for blood test
  	- Ask manager for special requests (e.g. MRI scan)
 
2. **Other features**
  	- Send SMS reminders to patients

## Installation:
1. Download / clone project:
```
git clone https://github.com/impact-oriented-programming/meat-is-murder.git
```
2. Install Django and other required libraries:
```
pip install Django==3.0.5
pip install django-crispy-forms
pip install pycountry
```
## Usage:
Enter the library where the project is stored and run the django server:
```
python manage.py runserver
```
Now you can go to:  http://localhost:8000/accounts/login and log into the system :nail_care:

Toy doctor user (not admin):
- username: Johndoe
- password: abcd@1234
