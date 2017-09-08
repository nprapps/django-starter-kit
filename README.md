nprviz's Django Starter Kit
=========================

* [About this template](#about-this-template)
* [Assumptions](#assumptions)
* [Copy the template](#copy-the-template)

About this template
-------------------

This is a barebones starter kit for making lightweight Django applications. It includes some basic configuration for the Django project and app, configuration for uWSGI and nginx, and Fabric commands for bootstrapping and deployment to servers.

This codebase is licensed under the [MIT open source license](http://opensource.org/licenses/MIT). See the ``LICENSE`` file for the complete license.

Please note: logos, fonts and other media referenced via url from this template are **not** covered by this license. Do not republish NPR media assets without written permission. Open source libraries in this repository are redistributed for convenience and are each governed by their own license.

Also note: Though open source, This project is not intended to be a generic solution. We strongly encourage those who love the app-template to use it as a basis for their own project template. We have no plans to remove NPR-specific code from this project.

Assumptions
-----------

The following things are assumed to be true in this documentation.

* You are running OSX.
* You are using Python 3. (Probably the version that came with OSX.)
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.
* You have PostgreSQL installed and working.
* You have NPR's AWS credentials stored as environment variables locally.

For more details on the technology stack used with the app-template, see our [development environment blog post](http://blog.apps.npr.org/2013/06/06/how-to-setup-a-developers-environment.html).

Copy the template
-----------------

Create a new repository on Github. Everywhere you see ``$NEW_PROJECT_NAME`` in the following script, replace it with the name of the repository you just created.

```
git clone git@github.com:nprapps/django-starter-kit.git $NEW_PROJECT_NAME
cd $NEW_PROJECT_NAME

mkvirtualenv -p `which python3` $NEW_PROJECT_NAME
pip install -r requirements.txt

fab bootstrap
```
This will setup the new repo and will replace `README.md` (this file) with `PROJECT_README.md`. See that file for usage documentation.

By default `bootstrap` will use `nprapps` as the Github username, and the current directory name as the repository name. **This is a best practice**, but you can override these defaults if you need to:

```
fab bootstrap:$GITHUB_USERNAME,$REPOSITORY_NAME
```

The end of the `fab bootstrap` printout will give you a secret key. You must put this in your environment before you try to setup the Django app. (If you're at NPR, store this in our shared env file.)

Then, setup the Django app.

```
fab django.setup_django
```

