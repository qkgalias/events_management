# Advance Programming

## GETTING STARTED

### Setup the project locally

- Open Terminal and run

```bash
git clone https://github.com/qkgalias/events_management.git
```

- Navigate to the project directory
```bash
cd events_management
```

- Create a virtual environment
```bash
python3 -m venv venv
```

### Activate the virtual environment
- On Windows
```bash
venv\Scripts\activate
```

- On MacOS/Linux
```bash
source venv/bin/activate
```

### Setting up dependencies

- Install the required framework and libraries:
 ```bash
pip install -r requirements.txt
 ```

### Updating dependencies 

- To keep track of the libraries used in this project:

```bash
pip freeze > requirements.txt
```

### Database setup
- Apply database migrations
```bash
python manage.py makemigrations accounts events
python manage.py migrate
```

### Create a superuser (Admin account)
```bash
python manage.py createsuperuser
```

### Run the file
- To launch the local development server:
```bash
python manage.py runserver
```
### Once the server is running, you can access the system at:
- Admin Interface: http://127.0.0.1:8000/admin/
- Main Dashboard: http://127.0.0.1:8000/dashboard/
---

## LIBRARY DOCUMENTATIONS



- [Django Documentation](https://docs.djangoproject.com/en/6.0/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
