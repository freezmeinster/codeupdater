from __future__ import absolute_import 

import os
import commands
from metranet_celery.celery import celery

OE_APP_DIR = "/opt/openerp-addons/metranet2"
WEB_APP_DIR = "/var/www"
TARGET_DB = "v7_metranet_frontend"
SOURCE_DB_PATH = "/opt/openerp-addons/metranet2/metranet.backup"


@celery.task
def pull_oe_module():
    os.chdir(OE_APP_DIR)
    commands.getoutput("sudo git pull origin master")
    return "oe-pulled"

@celery.task    
def restart_oe_server():
    commands.getoutput("sudo service openerp restart")
    return "server-oe-restarted"

@celery.task
def pull_web_module():
    os.chdir(WEB_APP_DIR)
    commands.getoutput("sudo git pull origin master")
    commands.getoutput("sudo chown -R www-data:www-data .")
    return "web-pulled"

@celery.task
def restart_web_server():
    commands.getoutput("sudo service apache2 restart")
    return "server-web-restarted"


@celery.task
def update_db():    
    commands.getoutput("sudo /opt/metranet_celery/updatedb.sh")
    return "db-updated"

@celery.task
def clean_transaction():
    commands.getoutput("sudo su office -c 'psql -d v7_metranet_frontend < /var/www/cleanup_transaction.sql'")

