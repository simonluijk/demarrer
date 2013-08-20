Demarrer
========

Demarrer is a Django project template.

Setup local development
-----------------------

You need to update the following files.

* Uncomment any needed packages in requirements.txt
* Run `fab local_venv`

Start the test server with the following commands:

* `vagrant up`
* `foreman run python manage.py syncdb --migrate`
* `foreman run python manage.py runserver`

Run with gunicorn locally
-------------------------

* `fab setup_s3:bucket_name=demarrer-dev`
* Copy the settings returned into ~/.env
* Uncomment the storage envs in ~/.env
* Run `foreman start`

Deploy to staging/production (Heroku)
-----------------------------

* Setup IAM accounts for staging and production
* Generate secrate keys with `openssl rand -base64 45`
* `fab setup_s3:bucket_name=demarrer-staging`
* `fab setup_s3:bucket_name=demarrer-media`

heroku create --remote staging --region eu demarrer-staging
git config heroku.remote staging
heroku config:set \
    DJANGO_SECRET_KEY=??? \
    DEFAULT_FILE_STORAGE=apps.s3utils.MediaStorage \
    STATICFILES_STORAGE=apps.s3utils.StaticStorage \
    AWS_ACCESS_KEY_ID=??? \
    AWS_SECRET_ACCESS_KEY=??? \
    AWS_STORAGE_BUCKET_NAME=demarrer-staging \
    EMAIL_BACKEND=django_ses.SESBackend \
    MEDIA_DOMAIN=???.cloudfront.net

heroku run python manage.py syncdb --migrate
git push staging master

heroku create --remote production --region eu demarrer-production
heroku config:set \
    DJANGO_SECRET_KEY=??? \
    DEFAULT_FILE_STORAGE=apps.s3utils.MediaStorage \
    STATICFILES_STORAGE=apps.s3utils.StaticStorage \
    AWS_ACCESS_KEY_ID=??? \
    AWS_SECRET_ACCESS_KEY=??? \
    AWS_STORAGE_BUCKET_NAME=demarrer-media \
    MEDIA_DOMAIN=???.cloudfront.net \
    EMAIL_BACKEND=django_ses.SESBackend \
    --remote production

heroku run python manage.py syncdb --migrate --remote production
git push production master
