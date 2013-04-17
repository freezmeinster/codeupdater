import json
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from metranet_celery import tasks
from django.conf import settings
from django.http import HttpResponse
from collections import defaultdict

temp = []
temp_db = []
temp_clean = []

def index(request):
    return render_to_response("base.html")

def mulai(request):
    del temp[:]
    WR = settings.WORKER
    for work in WR:
        temp.append({
            'name' : work,
            'pull_oe_module' : tasks.pull_oe_module.apply_async(queue=work),
            'restart_oe_server' : tasks.restart_oe_server.apply_async(queue=work),
            'pull_web_module' : tasks.pull_web_module.apply_async(queue=work),
            'restart_web_server' : tasks.restart_web_server.apply_async(queue=work),
        })
    return redirect("status")

def mulai_db(request):
    del temp_db[:]
    WR = settings.WORKER_DB
    for work in WR:
        temp_db.append({
            'name' : work,
            'update_db' : tasks.update_db.apply_async(queue=work)
        })
    return redirect("status_db")

def mulai_clean(request):
    del temp_clean[:]
    WR = settings.WORKER_DB
    for work in WR:
        temp_clean.append({
            'name' : work,
            'pull_web_module' : tasks.pull_web_module.apply_async(queue=work),
            'clean_transaction' : tasks.clean_transaction.apply_async(queue=work)
        })
    return redirect("status_clean")

def status(request):
    data = request.GET.copy()
    if data.get("ajax"):
        dicts_by_name=defaultdict(list)
        for d in temp:
            dicts_by_name[d['name']]=d
        srv = dicts_by_name[data.get("server")]
        s = {
                "style": "width:20%",
                "class" : "progress progress-danger progress-striped active",
                "message" : "Pulling Module ..."
            }
        
        if srv['pull_oe_module'].ready() and srv['restart_oe_server'].ready() and srv['pull_web_module'].ready() and srv['restart_web_server'].ready():
            s = {
                "style": "width:100%",
                "class" : "progress progress-primary progress-striped",
                "message" : "All app updated" 
                }
        elif srv['pull_oe_module'].ready() and srv['restart_oe_server'].ready() and srv['pull_web_module'].ready():
            s = {
                "style": "width:80%",
                "class" : "progress progress-info progress-striped active",
                "message" : "Pulling web source code ..."
                }
        elif srv['pull_oe_module'].ready() and srv['restart_oe_server'].ready():
            s = {
                "style": "width:60%",
                "class" : "progress progress-success progress-striped active",
                "message" : "Restarting Openerp Server ...."
                }
        elif srv['pull_oe_module'].ready():
            s = {
                "style": "width:40%",
                "class" : "progress progress-warning progress-striped active",
                "message" : "Pullng Openerp module ..."
                }
            
        return HttpResponse(json.dumps(s), mimetype="application/json")
    return render_to_response("hasil.html",{
        "result" : temp    
    })

def status_db(request):
    data = request.GET.copy()
    if data.get("ajax"):
        dicts_by_name=defaultdict(list)
        for d in temp_db:
            dicts_by_name[d['name']]=d
        srv = dicts_by_name[data.get("server")]
        s = {
                "style": "width:60%",
                "class" : "progress progress-warning progress-striped active",
                "message" : "Updating database ..."
            }
        if srv['update_db'].ready() :
            s = {
                "style": "width:100%",
                "class" : "progress progress-primary progress-striped",
                "message" : "Database Updated"
                }

            
        return HttpResponse(json.dumps(s), mimetype="application/json")
    return render_to_response("hasil_db.html",{
        "result" : temp_db    
    })

def status_clean(request):
    data = request.GET.copy()
    if data.get("ajax"):
        dicts_by_name=defaultdict(list)
        for d in temp_clean:
            dicts_by_name[d['name']]=d
        srv = dicts_by_name[data.get("server")]
        s = {
                "style": "width:50%",
                "class" : "progress progress-warning progress-striped active",
                "message" : "Updating SQL ..."
            }
        if srv['pull_web_module'].ready() and srv['clean_transaction'].ready():
            s = {
                "style": "width:100%",
                "class" : "progress progress-primary progress-striped",
                "message" : "Transaction cleaned"
                }
        elif srv['pull_web_module'].ready():
            s = {
                "style": "width:70%",
                "class" : "progress progress-success progress-striped",
                "message" : "Cleaning transaction ..."
                }
        return HttpResponse(json.dumps(s), mimetype="application/json")
    return render_to_response("hasil_clean.html",{
        "result" : temp_clean    
    })
