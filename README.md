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

### Database setup
- Apply database migrations to create necessary tables
```bash
python manage.py makemigrations accounts events
python manage.py migrate
```

### Images Setup
- The /media/speakers/ and /media/event_banners/ folders should already exist in your local directory after cloning.
```bash
This project uses .gitkeep to preserve the media directory structure on GitHub. 
```
- Action: manually place the images set into these respective subfolders.

- import .json file to populate dashboard with the 5 prepared events and 5 speakers, run the following:
```bash
python manage.py loaddata dummy_data.json
```

### Create a superuser (to access Django Admin Panel)
```bash
python manage.py createsuperuser
```

### Run the system
- launch the local development server:
```bash
python manage.py runserver
```
### Once the server is running, you can access the system at:
- http://127.0.0.1:8000/
---

## TECH STACK
- Backend: [Django 4.2.27 ](https://docs.djangoproject.com/en/4.2/)
- Frontend: [Tailwind CSS Play CDN](https://tailwindcss.com/docs/installation/play-cdn)
- Database: [SQLite3]