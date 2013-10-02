Demarrer
========

Demarrer is a Django project template that follows [the 12-factor app][1] methodology as closely as possible. Namily it tries to be hosting environment agnostic. Each setting that could change in each enviroment should be set as an environment variable. e.g. DEBUG and SECRET_KEY.

[1]: http://12factor.net

Setup local development
-----------------------

You need to update the following files.

* Uncomment any needed packages in requirements.txt
* Run `fab local_venv`

Start the test server with the following commands:

* `vagrant up`
* `cp env.example .env`
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


Setup staging...

        heroku create --remote staging --region eu demarrer-staging
        git config heroku.remote staging

        heroku labs:enable user-env-compile
        heroku addons:add pgbackups
        heroku addons:add memcachier:dev

        heroku config:set \
            DJANGO_SECRET_KEY=??? \
            DEFAULT_FILE_STORAGE=apps.s3utils.MediaStorage \
            STATICFILES_STORAGE=apps.s3utils.StaticStorage \
            AWS_ACCESS_KEY_ID=??? \
            AWS_SECRET_ACCESS_KEY=??? \
            AWS_STORAGE_BUCKET_NAME=demarrer-staging \
            EMAIL_BACKEND=django_ses.SESBackend \
            MEDIA_DOMAIN=???.cloudfront.net \
            ALLOWED_HOSTS=demarrer-staging.herokuapp.com

        git push staging master
        heroku run python manage.py syncdb --migrate

Now production...

        heroku create --remote production --region eu demarrer-production

        heroku labs:enable user-env-compile --remote production
        heroku addons:add pgbackups --remote production
        heroku addons:add memcachier:dev --remote production
        heroku domains:add www.demarrer.com --remote production

        heroku config:set \
            DJANGO_SECRET_KEY=??? \
            DEFAULT_FILE_STORAGE=apps.s3utils.MediaStorage \
            STATICFILES_STORAGE=apps.s3utils.StaticStorage \
            AWS_ACCESS_KEY_ID=??? \
            AWS_SECRET_ACCESS_KEY=??? \
            AWS_STORAGE_BUCKET_NAME=demarrer-media \
            EMAIL_BACKEND=django_ses.SESBackend \
            MEDIA_DOMAIN=???.cloudfront.net \
            ALLOWED_HOSTS=www.demarrer.com \
            --remote production

        git push production master
        heroku run python manage.py syncdb --migrate --remote production
