from __future__ import absolute_import 

import os 
from metranet_celery.celery import celery

OE_APP_DIR = "/opt/openerp-addons/metranet2"
WEB_APP_DIR = "/var/www"


@celery.task
def pull_oe_module():
    os.chdir(OE_APP_DIR)
    os.popen("git pull origin master")
    return "oe-pulled"

@celery.task    
def restart_oe_server():
    os.popen("service openerp restart")
    os.chdir(WEB_APP_DIR)
    return "server-oe-restarted"

@celery.task
def pull_web_module():
    os.popen("git pull origin master")
    os.popen("chown -R www-data:www-data .")
    return "web-pulled"

@celery.task
def restart_web_server():
    os.popen("service apache2 restart")
    return "server-web-restarted"
