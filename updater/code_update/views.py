import json
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from metranet_celery.tasks import pull_oe_module, restart_oe_server, pull_web_module, restart_web_server
from django.conf import settings
from django.http import HttpResponse
from collections import defaultdict

temp = []

def index(request):
    return render_to_response("base.html")

def mulai(request):
    del temp[:]
    WR = settings.WORKER
    for work in WR:
        temp.append({
            'name' : work,
            'pull_oe_module' : pull_oe_module.apply_async(queue=work),
            'restart_oe_server' : restart_oe_server.apply_async(queue=work),
            'pull_web_module' : pull_web_module.apply_async(queue=work),
            'restart_web_server' : restart_web_server.apply_async(queue=work),
        })
    return redirect("status")

def status(request):
    data = request.GET.copy()
    if data.get("ajax"):
        dicts_by_name=defaultdict(list)
        for d in temp:
            dicts_by_name[d['name']]=d
        srv = dicts_by_name[data.get("server")]
        s = {
                "style": "width:20%",
                "class" : "progress progress-danger progress-striped",
                "message" : "starting...."
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