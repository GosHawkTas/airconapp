#!/usr/bin/env bash

# Quit when errors happen
set -e

# Helper to run a command as another user
function as () {
	local user="$1"
	shift
	sudo -iu "$user" "$@"
}
function heading() {
	echo ' '
	echo "$@"
	echo '--------------------------------------------'
}
function subheading() {
	echo " -> $@"
}

v_home=~vagrant
p_name="airconapp"
p_root="/srv/$p_name"  # Path to the code
p_venv="${v_home}/venv"  # Where to put the venv
p_django=$p_name  # The name of the django directory

export PIP_DOWNLOAD_CACHE=/tmp/pip-download-cache
mkdir -p "$PIP_DOWNLOAD_CACHE"


# Set up the source directory
mkdir -p /srv
chown vagrant:vagrant /srv
ln -sfn /vagrant "$p_root"
cd "${p_root}"


heading "Built in 'STRAYA!"
cat > /var/lib/locales/supported.d/en_AU <<<"en_AU.UTF-8 UTF-8"
locale-gen
cat > /etc/timezone <<<"Australia/Hobart"
dpkg-reconfigure -f noninteractive tzdata


heading 'Installing system packages'
subheading 'Using internode mirrors'
sed -i 's/^deb.*archive/# \0/' /etc/apt/sources.list
cat >> /etc/apt/sources.list <<<"
deb http://au.archive.ubuntu.com/ubuntu/ trusty main universe
deb-src http://au.archive.ubuntu.com/ubuntu/ trusty main universe
deb http://au.archive.ubuntu.com/ubuntu/ trusty-updates main universe
deb-src http://au.archive.ubuntu.com/ubuntu/ trusty-updates main universe
"

subheading 'Adding Elasticsearch package repository'
# Add the ElasticSearch repos
if ! apt-key list | grep -q 'Elasticsearch' ; then
	wget -qO- http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -
fi
cat > /etc/apt/sources.list.d/elasticsearch.list <<<"deb http://packages.elasticsearch.org/elasticsearch/1.3/debian stable main"

subheading 'Adding nodesource package repository'
if ! apt-key list | grep -q 'NodeSource' ; then
	wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
fi
cat > /etc/apt/sources.list.d/nodesource.list <<<"deb https://deb.nodesource.com/node/ trusty main"

subheading 'Stopping and removing puppet and chef'
service puppet stop
service chef-client stop
apt-get remove -y --auto-remove chef chef-zero puppet puppet-common

# Update package listing
subheading 'Installing packages'
apt-get update -y
# Install packages required for deployment
apt-get install -y $( cat "$p_root"/setup/apt-requirements.txt )
# Install packages required for developing
apt-get install -y git vim nano ncurses-term nfs-kernel-server nfs-common ipython nodejs htop


# Set up postgres
heading 'Adding postgres roles and databases'
db_name="${p_name}"
db_user="vagrant"
db_pass="ballroom"
subheading "Database name: $db_name"
as postgres psql <<<"CREATE USER ${db_name} NOCREATEDB NOCREATEUSER PASSWORD '${db_pass}'"
as postgres psql <<<"CREATE USER ${db_user} CREATEDB NOCREATEUSER PASSWORD '${db_pass}'"
as postgres psql <<<"GRANT ${db_name} TO ${db_user}"
as postgres psql <<<"CREATE DATABASE ${db_name} ENCODING='UTF8' LC_CTYPE='en_AU.utf8' LC_COLLATE='en_AU.utf8' TEMPLATE=template0"


# Set up elasticsearch
heading 'Setting up ElasticSearch'
cat > /etc/default/elasticsearch <<<"
ES_MAX_MEM=256M
ES_MIN_MEM=256M"
if ! [ -d "/usr/share/elasticsearch/plugins/marvel" ] ; then
	~elasticsearch/bin/plugin -i elasticsearch/marvel/latest
fi
# Stop elasticsearch, as it will be killed in an OOM situation
# Bloody memory hog...
service elasticsearch stop
subheading 'Elasticsearch accessible at 127.0.0.1:8125'
subheading 'Marvel accessible at http://127.0.0.1:8125/_plugin/marvel/'


# Set up bash to automatically activate the virtualenv
# This is handy when logging in
# Only needed in development
heading 'Installing magic'
if ! grep -qxF 'source ~/.bashrc.vagrant' < "${v_home}/.bashrc" ; then
	cat >>"${v_home}/.bashrc" <<<"
source '${v_home}/.bashrc.vagrant'"
fi

cat >"${v_home}/.bashrc.vagrant" <<<"
cd '$p_root'
source '$p_venv/bin/activate'
PATH=\"$p_root/node_modules/.bin:\$PATH\"
PS1='\\W \\$ '

function reset-db() {
    sudo -u postgres psql <<<\"DROP DATABASE ${db_name}; CREATE DATABASE ${db_name} ENCODING='UTF8' LC_CTYPE='en_AU.UTF-8' LC_COLLATE='en_AU.UTF-8' TEMPLATE=template0\"
    ./manage.py migrate --noinput
    ./manage.py siteskeleton
    ./manage.py testdata
}
"

chown vagrant:vagrant "${v_home}/.bashrc" "${v_home}/.bashrc.vagrant"

heading 'Setting up python environment'

subheading 'Adding ~/.pip/pip.conf'
mkdir -p "${v_home}/.pip"
cat >"${v_home}/.pip/pip.conf" <<<"
[global]
extra-index-url = https://packages.takeflight.net.au/
"
chown -R vagrant:vagrant "${v_home}/.pip"

subheading 'Installing virtualenv'
# virtualenv global setup
pip install virtualenv

# The virtualenv can be placed anywhere when installing in production
subheading "Creating virtualenv at ${p_venv}"
as vagrant virtualenv "${p_venv}"

subheading "Installing python dependencies"
as vagrant "${p_venv}/bin/pip" install -e "${p_root}"

heading 'Setting up node environment'
subheading 'Updating npm'
npm install -g npm

subheading "Installing node dependencies"
# The `node_modules` directory is kept in ~vagrant,
# so it is created and destroyed along with the vagrant box
node_modules="${v_home}/node_modules"
rm -rf "${p_root}/node_modules"
ln -s "${node_modules}" "${p_root}/node_modules"
mkdir -p "${node_modules}"
( cd "${p_root}" && npm install )
chown -R vagrant:vagrant "${node_modules}"

heading 'Starting elasticsearch'
service elasticsearch start
sleep 5s

# Set up the python environment
heading 'Finalising the Django install'

subheading "Making local settings files"
local_py="${p_root}/settings.py"
if ! [[ -e "$local_py" ]] ; then
	subheading "Making $local_py"
	cat > "$local_py" <<<"
import os

from airconapp.settings.develop import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': 'vagrant',
        'PASSWORD': 'ballroom',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []

SECRET_KEY = '$(head -c36 /dev/urandom | base64 )'

VAR_ROOT = os.path.dirname(__file__)
ASSETS_ROOT = os.path.join(VAR_ROOT, 'assets')     # ./var/assets
MEDIA_ROOT = os.path.join(ASSETS_ROOT, 'media')    # ./var/assets/media
STATIC_ROOT = os.path.join(ASSETS_ROOT, 'static')  # ./var/assets/static
"
fi


# Django project setup
subheading "Adding database tables and contents"
as vagrant bash -c "
set -e;
source '${v_home}/.bashrc.vagrant';
reset-db;
"

subheading 'Compiling assets'
as vagrant bash -c "
set -e;
source '${v_home}/.bashrc.vagrant';
gulp build;
"
