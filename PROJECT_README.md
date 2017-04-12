Copyright 2017 NPR.  All rights reserved.  No part of these materials may be reproduced, modified, stored in a retrieval system, or retransmitted, in any form or by any means, electronic, mechanical or otherwise, without prior written permission from NPR.

(Want to use this code? Send an email to nprapps@npr.org!)


$NEW_PROJECT_SLUG
========================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [What's in here?](#whats-in-here)
* [Bootstrap the project](#bootstrap-the-project)
* [Hide project secrets](#hide-project-secrets)
* [Run the project](#run-the-project)
* [Deploy to EC2](#deploy-to-ec2)
* [Install cron jobs](#install-cron-jobs)
* [Install web services](#install-web-services)
* [Run a remote fab command](#run-a-remote-fab-command)

What is this?
-------------

**TKTK: Describe $NEW_PROJECT_SLUG here.**

Assumptions
-----------

The following things are assumed to be true in this documentation.

* You are running OSX.
* You are using Python 3.
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.
* You have NPR's AWS credentials stored as environment variables locally.

For more details on the technology stack used with the app-template, see our [development environment blog post](http://blog.apps.npr.org/2013/06/06/how-to-setup-a-developers-environment.html).

What's in here?
---------------

The project contains the following folders and important files:

* ``config`` -- The default Django project
* ``confs`` -- Server configuration files for nginx and uwsgi. Edit the templates then ``fab <ENV> servers.render_confs``, don't edit anything in ``confs/rendered`` directly.
* ``core`` -- The default Django app
* ``fabfile`` -- [Fabric](http://docs.fabfile.org/en/latest/) commands for automating setup, deployment, data processing, etc.
* ``app_config.py`` -- Global project configuration for scripts, deployment, etc.
* ``crontab`` -- Cron jobs to be installed as part of the project.
* ``manage.py`` -- Default Django management command file.
* ``requirements.txt`` -- Python requirements.
* ``run_on_server.sh`` -- Shell script used on the server to invoke environment variables before running commands.

Bootstrap the project
---------------------

```
cd $NEW_PROJECT_SLUG
mkvirtualenv $NEW_PROJECT_SLUG
pip install -r requirements.txt
fab django.setup_django
```

Hide project secrets
--------------------

Project secrets should **never** be stored in ``app_config.py`` or anywhere else in the repository. They will be leaked to the client if you do. Instead, always store passwords, keys, etc. in environment variables and document that they are needed here in the README.

Any environment variable that starts with ``$PROJECT_SLUG_`` will be automatically loaded when ``app_config.get_secrets()`` is called.

Run the project
---------------

A flask app is used to run the project locally. It will automatically recompile templates and assets on demand.

```
workon $PROJECT_SLUG
fab app
```

Visit [localhost:8000](http://localhost:8000) in your browser.

Deploy to EC2
-------------

To deploy this project to EC2, first, make sure the IP addresses or hostnames are configured in `app_config.py` under the variables `PRODUCTION_SERVERS` and `STAGING_SERVERS`. Also ensure that, on the servers you are deploying to, you have installed Python 3, upstart, nginx, uWSGI, and PostgreSQL.

Then, run `fab staging master servers.setup` to deploy to staging. This will setup the clone the repo, setup the virtual environment, and do other miscellaneous housekeeping.

Once the server is correctly setup, you can run `fab staging master deploy_server` to checkout the latest from the repo and restart uWSGI. 

Install web services
---------------------

Web services are configured in the `confs/` folder.

To check that these files are being properly rendered, you can render them locally and see the results in the `confs/rendered/` directory.

```
fab servers.render_confs
```

Deploy the configuration files by running:

```
fab servers.deploy_confs
```

Run a remote fab command
-------------------------

Sometimes it makes sense to run a fabric command on the server, for instance, when you need to render using a production database. You can do this with the `fabcast` fabric command. For example:

```
fab staging master servers.fabcast:deploy
```

If any of the commands you run themselves require executing on the server, the server will SSH into itself to run them.