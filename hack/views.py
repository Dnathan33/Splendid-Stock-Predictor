from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import pandas as pd
import numpy as np
import io
import json
from bson import json_util, objectid
from pymongo import MongoClient
from .query import connect_monogo
from .query import add_document

# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")

def predict_req(request):
    stock = request.GET.get('stock','')
    db = connect_monogo()
    collection = db["Prediction"]
    data = json.loads(json_util.dumps(collection.find_one({stock:{ '$exists': True}})))
    return JsonResponse(data, safe=False)

def add(request):
    url = request.GET.get('url', '')
    add_document(url)
    return HttpResponse("Added to Collection.")