# URL Shortening Service

API service for shortening url written on DRF

## Check it out!

[URL Shortening Servicee project deployed to Heroku](https://url-shortener-dh.herokuapp.com/)

## Installation

Python3 must be already installed

Install SQLite and create db

```shell
git clone https://github.com/DHushchyk/url_shortening_service.git
cd url_shortening_service
python3 -m venv venv
source venv\Scripts\activate (on Windows)
source venv\bin\activate (on Mac)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Getting access
* access via admin panel /admin/ username: superuser, password: Afjo346@tr
* all guests get access to api and home page


## Features
* Admin panel /admin/
* Creating short urls and getting lisl of them
* Creating short urls and getting lisl of them via API /api/links/
* Getting statistics of redirect /api/links/<link_id>/ (only for owners)
* Short link redirect server_url/redirect/short_url/
