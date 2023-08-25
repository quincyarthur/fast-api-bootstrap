# Fast API Rest API Template

This template is intended to quickly bootstrap a new REST API. It comes wired with the following features:

* User Creation
* User Signin (JWT)
* OAuth (Google)
* User Account Activation
* Resend Account Activation Email
* Forgot Password
* Background Job that removes users who have not activated their accounts within 24 hours


#### Project Dependencies:
* [Docker](https://www.docker.com/products/docker-desktop/) **_install if needed_**
* Python 3.11 (included in dockerfile)
* Postgres SQL 15.1 (included in dockerfile)
* [Send In Blue Transactional Email Account](https://account-app.sendinblue.com/account/login) **_Optional_**
* [Google (Web Client Credentials)](https://console.developers.google.com/apis) **_Optional_**
* Alebmic 
* SQLAlchemy
* APScheduler


#### Instructions:
1. Clone Repo
`git clone <template_url>`
2. Rename cloned repo folder to the name of your new project
3. Create new project repo in Github
4. Remove remotes from cloned repo
`git remote rm <template_remote>`
5. Add the remotes for your newly created Github repo
`git remote add origin <new_proj_url>`
6. Add .env to project root using provided .env.example
7. Start container
`run docker compose -f docker-compose-dev.yml up`

#### API Documentation

* <a href=http://localhost:3000/redoc target="_blank">Standard Docs</a>
* <a href=http://localhost:3000/docs target="_blank">Interactive Docs</a>

#### FAQ

1. Why isn't Alembic recognizing changes in my model?
> Navigate to migrations -> env.py make sure that all your models are imported. Add the model's metadata to SQLAlchemy's target metadata i.e 
`target_metadata = [Model.metadata]`

2. Why didn't my router/routes appear in the open api documentation?
> In main.py import your router and include using `app.include_router()`

3. How to autogenerate alembic migrations
> `alemic revision --autogenerate -m <message>`

4. How do I install a new package?
> * Install the package `pipenv install <package>`
> * Remove the existing requirements.txt `rm requirements.txt`
> * Regenerate an updated requirements.txt `  pipenv requirements >> requirements.txt`
> * Delete running api container
> * Delete the existing api project image
> * Start container `run docker compose -f docker-compose-dev.yml up`

6. Why do I get an "Unauthorized error" when attempting to hit a protected route in postman?

>In the request headers make sure to add an Authorization key with the value "bearer"