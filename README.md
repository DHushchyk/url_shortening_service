# URL Shortening Service

API service for shortening url written on DRF

Python3 must be already installed

Install SQLite and create db

```shell
git clone https://github.com/DHushchyk/url_shortening_service.git
cd url_shortening_service
python3 -m venv venv
source venv\Scripts\activate (on Windows)
source venv\bin\activate (on Mac)
pip install -r requirements.txt
```

## Getting access
* create user via python manage.py createsuperuser
* all guests get access to api


## Features
* Admin panel /admin/
* Creating short urls and getting lisl of them /api/links/
* Getting statistics of redirect /api/links/<link_id>/ (only for owners)
* Short link redirect server_url/redirect/short_url/
