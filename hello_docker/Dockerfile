# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NOTE: DO *NOT* EDIT THIS FILE.  IT IS GENERATED.
# PLEASE UPDATE Dockerfile.txt INSTEAD OF THIS FILE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FROM selenium/node-firefox-debug:3.141.59-radium
LABEL author=asayapova 

USER root

RUN apt-get -qqy update \
    && apt-get -qqy --no-install-recommends install apt-utils \
    && apt-get -qqy update \
    && apt-get -qqy --no-install-recommends install systemd net-tools git python-pip python-setuptools python3-pip python3-setuptools

USER seluser

# Scripts to run Selenium Standalone
#====================================
COPY start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY selenium.conf /etc/supervisor/conf.d/

# Install and upgrade python libs
RUN python -m pip install --no-cache-dir --upgrade pip wheel pytest selenium browsermob-proxy mysql-connector-python allure-pytest paramiko \
    && python3 -m pip install --no-cache-dir --upgrade pip wheel pytest selenium browsermob-proxy mysql-connector-python allure-pytest paramiko

# Cloning tests in git repo
RUN mkdir /tmp/git_tests \
    && git clone https://github.com/bronzehat/initial_tests /tmp/git_tests/

WORKDIR /tmp/git_tests/initial_tests/

EXPOSE 4444
EXPOSE 5900
