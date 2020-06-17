# clinic
#### Refugee Clinic Management System
Includes two main modules:
1. **Clinic calendar:** To be used in the reception desk
  	- Show scheduled appointments (month & day view)
    - Create / edit appointment
    - Query a patient and view their profile
  	- Link to clinic management page (create / edit patients, doctor's shifts and more)
  
2. **Doctor interface:** The doctor's "home-page"
  	- Show all of today's scheduled appointments
  	- Query a patient
  	- link to patient interface - view the medical record of a patient
  	- Start session (between doctor and patient during an appointment)
  	- Prescribe medications (and export copy for patient)
  	- Ask for blood test
  	- Ask manager for special requests (e.g. MRI scan)
 
## Installation:
1. Download / clone project to your computer:
  ```
  git clone https://github.com/impact-oriented-programming/clinic.git
  ```
2. Install Django and other required libraries:
  ```
  pip install Django==3.0.5
  pip install django-crispy-forms
  pip install pycountry
  pip install django-autocomplete-light
  pip install --pre xhtml2pdf
  pip install xhtml2pdf
  ```
3. Create a new, empty DB (the repository does not include one):
  ```
  python manage.py migrate
  ```
4. Add medical data to the DB:
  ```
 python manage.py add_medical_db
  ```

## Usage:
1. Enter the library where the project is stored through the command line.
2. Create an admin user (follow command-line instructions)
  ```
  python manage.py createsuperuser
  ```
3. Run the Django server:
  ```
  python manage.py runserver
  ```
Now you can go to:  http://localhost:8000/accounts/login and log into the system with the admin you created. :nail_care:

