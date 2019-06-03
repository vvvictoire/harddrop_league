# Harddrop League site and Discord bot

## How to install

Create a virtualenv with the `virtualenv` command. `venv` will **NOT** work.

Then run `pip install -r requirements.txt`

## How to build

### First run

Execute `manage.py createsuperuser`.

Create a `secret` file in `league_site`, containing the Django secret key.

Create a `_discord_token` file in `league_site/read_only_site/management/commands`,
containing the Discord bot token.

### Building

Execute `manage.py collectstatic`

## Apache configuration
$path is the path to the virtualenv

```<VirtualHost *:port>

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
    #WGSIApplicationGroup %{GLOBAL}
    WSGIScriptAlias / $path/league_site/league_site/wsgi.py

</VirtualHost>```
