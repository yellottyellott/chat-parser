#!/usr/bin/env bash
# This script is used to provision the vagrant box.

sudo apt-get install -y python-dev python-pip libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo pip install virtualenvwrapper

# Create .bash_profile
cat > /home/vagrant/.bash_profile << EOF
if [ -f ~/.bashrc ]; then
  source ~/.bashrc
fi

export PYTHONDONTWRITEBYTECODE=1
source /usr/local/bin/virtualenvwrapper_lazy.sh

cd /vagrant
workon chat_parser

EOF

chown vagrant:vagrant /home/vagrant/.bash_profile

su vagrant -c "
    source /usr/local/bin/virtualenvwrapper_lazy.sh &&
    mkvirtualenv chat_parser -r /vagrant/requirements.txt &&
    cd /vagrant && pip install -e ."
