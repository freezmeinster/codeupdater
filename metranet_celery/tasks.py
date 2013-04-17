from __future__ import absolute_import 

import os 
from metranet_celery.celery import celery

OE_APP_DIR = "/opt/openerp-addons/metranet2"
WEB_APP_DIR = "/var/www"
TARGET_DB = "v7_metranet_frontend"
SOURCE_DB_PATH = "/opt/openerp-addons/metranet2/metranet.backup"


@celery.task
def pull_oe_module():
    os.chdir(OE_APP_DIR)
    os.popen("sudo git pull origin master")
    return "oe-pulled"

@celery.task
def start_oe_server():
    os.popen("sudo service openerp start")
    return "server-oe-started"

@celery.task
def stop_oe_server():
    os.popen("sudo service openerp stop")
    return "server-oe-stoped"

@celery.task    
def restart_oe_server():
    os.popen("sudo service openerp restart")
    return "server-oe-restarted"

@celery.task
def pull_web_module():
    os.chdir(WEB_APP_DIR)
    os.popen("sudo git pull origin master")
    os.popen("sudo chown -R www-data:www-data .")
    return "web-pulled"

@celery.task
def restart_web_server():
    os.popen("sudo service apache2 restart")
    return "server-web-restarted"

@celery.task
def drop_db():
    os.popen("sudo su office -c 'dropdb %s'" % TARGET_DB)
    return "database-droped"

@celery.task
def create_db():
    os.popen("sudo su office -c 'createdb %s'" % TARGET_DB)
    return "database-created"

@celery.task
def restore_db():    
    os.popen("sudo su office -c 'pg_restore -d %s %s'" % (TARGET_DB, SOURCE_DB_PATH))
    return "db-updated"

@celery.task
def test_user():
    return os.popen("whomai").read()

