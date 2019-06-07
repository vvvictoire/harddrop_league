# Harddrop League site and Discord bot

## How to install

Create a virtualenv with the `virtualenv` command. `venv` will **NOT** work.

Then run `pip install -r requirements.txt`.

## How to build

### First run

1.Execute `manage.py createsuperuser`.

2.Create a `secret` file in the parent directory of this file, containing the
Django secret key.

3.Create a `_discord_token` file in the parent directory of this file,
containing the Discord bot token.

### Building

1.Execute `manage.py collectstatic`

2.Execute `manage.py migrate`

#### `post-receive` hook example
```
#!/bin/bash
GIT_WORK_TREE=$path/league_site git checkout -f
source $path/bin/activate
python $path/league_site/manage.py collectstatic --noinput
python $path/league_site/manage.py migrate
touch $path/league_site/league_site/wsgi.py
# So that mod_wsgi in apache knows to update its files
```

## Apache configuration
$path is the path to the virtualenv

```
<VirtualHost *:port>

    Alias /static $path/league_site/read_only_site/static
    <Directory $path/league_site/read_only_site/static>
        Require all granted
    </Directory>
    <Directory $path/league_site/league_site>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIProcessGroup league_site
    WSGIDaemonProcess league_site python-home=$path python-path=$path/league_site
    WSGIScriptAlias / $path/league_site/league_site/wsgi.py

</VirtualHost>
```
