## Steps to Run

- Clone this repo to a folder
- Ensure python, pip and pipenv are installed
- Within the cloned folder, enter virtual shell `pipenv shell`
- Install dependancies `pipenv install` or `pip install -r requirements.txt`
- Do migrations `python manage.py migrate`
- Create a superuser `python manage.py createsuperuser`
- Run the server `python manage.py runserver`
- Go to http://localhost:8000 in your browser

## User generation and permission management

- Go to http://localhost:8000/admin in your browser to get django's inbuild admin system and login as superadmin
- Add users, and choose the following permission for them
  - level_one_approval ( Permission to do 1st approval )
  - level_two_approval ( Permission to do 2nd approval )
- Login with the desired user at http://localhost:8000

NB: This sample app can't be considered a well built nor secure, Rather it's a quick prototype developed under 6 hours.






 
