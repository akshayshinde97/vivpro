# Songs api backend 

Overview

Project: 
Description: <ONE-LINE_DESCRIPTION_OF_YOUR_API/BACKEND>
Stack: Django, Django REST Framework, SQLITE
Base URL (dev): http://localhost:8000
API Prefix: musiclytics/analytics/api/v1

## steps to setup backend
1)git clone then cd <vivpro>

# create virtualenv
2)python -m venv .venv
### macOS/Linux
source .venv/bin/activate
### Windows (PowerShell)
.venv\Scripts\Activate.ps1

### install dependencies
3)pip install -r requirements.txt


### Run Server
4) python manage.py runserver


##API CURLS
Paginated api GET:-  curl --location --request GET 'http://127.0.0.1:8000/musiclytics/analytics/api/v1/songs/ 
Serach song by name :- curl --location --request GET 'http://127.0.0.1:8000/musiclytics/analytics/api/v1/songs/?page=1&query=3AM'
Post song rating :- curl --location --request POST 'http://127.0.0.1:8000/musiclytics/analytics/api/v1/rate_song/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "rating": 3,
    "song_id": "5vYA1mW9g2Coh1HUFUSmlb"
}'
