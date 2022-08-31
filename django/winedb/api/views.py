import json
import pickle
import os
import sys
import re

from django.shortcuts import render, HttpResponse, resolve_url
from django.templatetags.static import static
from urllib.parse import quote as urlencode

from api.serializers import WineSerializer
from api.models import Wine

from api.ml.predictDO import multiple_autogluonClassifier


PAGE_SIZE = 20

## Util Functions

def get_request_url(request):
    return re.sub(r'\?.*', '',request.build_absolute_uri())


def anotate_resource_links(wine_list, request):
    host = request.scheme + '://' +request.get_host()

    for wine in wine_list:
        wine['$link'] = host + resolve_url('api-wine-detail', wine_id=wine["id"])
        # wine['do_image_route'] = 'web/do_img/' + normalize_do_name(wine['zone']) + '.jpg'
        wine['do_image_url']  = static('web/do_img/' + normalize_do_name(wine['zone']) + '.jpg')

    return wine_list

def json_response(data, status=200):
    return HttpResponse(
        json.dumps(data), status=status, content_type="application/json"
    )

def normalize_do_name(name):
    # lowercase
    name = name.lower()
    # no spacing or dots
    name = name.split('/ ')[0].strip().replace('.','').replace(' ', '_')
    # no special characters
    name = re.sub(r'[^a-zA-Z\d_]', 'x', name)

    return name

def dummy(request, *args, **kwargs):
    return HttpResponse(
        json.dumps({"response": True, "request": kwargs}), "application/json"
    )

# Model APIs

def wine_detail(request, wine_id):
    wine = Wine.objects.get(pk=wine_id)
    wines_serialized = WineSerializer.serialize([wine,])
    wines_serialized = anotate_resource_links(wines_serialized, request)

    return json_response({"data": wines_serialized[0]})

def wine_list(request):
    page = 1
    if 'page' in request.GET:
        page = max(int(request.GET['page']), 1)

    wine_query = Wine.objects.all()[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
    wines_serialized = WineSerializer.serialize(wine_query)

    next_url = None
    if len(wine_query) == PAGE_SIZE:
        next_url = f"{get_request_url(request)}?page={page+1}"

    return json_response({
        "next": next_url,
        "data": anotate_resource_links(wines_serialized, request)
    })

def wine_search(request):
    page = 1
    if 'page' in request.GET:
        page = max(int(request.GET['page']), 1)

    term = request.GET['q']
    
    wine_query = Wine.objects.filter(name__icontains=term)
    wine_query |= Wine.objects.filter(cellar_name__icontains=term)
    wine_query |= Wine.objects.filter(zone__icontains=term)

    wine_query = wine_query[(page-1)*PAGE_SIZE:page*PAGE_SIZE]

    wines_serialized = WineSerializer.serialize(wine_query)

    next_url = None
    if len(wine_query) == PAGE_SIZE:
        next_url = f"{get_request_url(request)}?q={urlencode(term)}&page={page+1}"

    return json_response({
        "next": next_url,
        "data": anotate_resource_links(wines_serialized, request)
    })


# Load ML Predictor pickles

ml_path = os.path.join(os.path.dirname(__file__), "ml")
sys.path.append(ml_path)

filename = os.path.join(ml_path, "CBR.pickle")
with open(filename, 'rb') as f:
    ML_RECOMMEND_SIMILAR = pickle.load(f)

filename = os.path.join(ml_path, "CBRDO.pickle")
with open(filename, 'rb') as f:
    ML_RECOMMEND_STYLE = pickle.load(f)

# filename = os.path.join(ml_path, "predictDO.pickle")
# with open(filename, 'rb') as f:
#    ML_PREDICT_DO = pickle.load(f)
filepath = os.path.join(ml_path, "ag-model")
ML_PREDICT_DO = multiple_autogluonClassifier(filepath)


# ML APIs

def wine_recommender_similarity(request, wine_id):
    # Returns pandas with wine as index, CS as cosine similarity
    predictions = ML_RECOMMEND_SIMILAR.predict(wine_id)

    wines = Wine.objects.filter(pk__in=predictions[:10].index)
    wines = WineSerializer.serialize(wines)
    for wine in wines:
        wine['similar_score'] = predictions.loc[wine['id']].CS


    return json_response({
        "data": anotate_resource_links(wines, request)
    })

def wine_recommender_style_do(request, *args, **kwargs):
    features = request.GET["features"].split(",")

    # Returns pandas
    predictions = ML_RECOMMEND_STYLE.predict(features)

    wines = Wine.objects.filter(pk__in=predictions[:10].index)
    wines = WineSerializer.serialize(wines)
    for wine in wines:
        wine['similar_score'] = predictions.loc[wine['id']].CS

    return json_response({
        "data": anotate_resource_links(wines, request)
    })

def predict_do(request, *args, **kwargs):
    predictions = ML_PREDICT_DO.predict_do(request.GET["style"].split(","))

    return HttpResponse(
        # json.dumps({'response': mock_data}),
        json.dumps({"response": predictions}),
        "application/json",
    )

def do_list(request):
    zones_query = Wine.objects.raw('SELECT slug, max(zone) as zone FROM api_wine GROUP BY zone')
    zones_list = []

    for row in zones_query:
        zones_list += [{
            "slug": normalize_do_name(row.zone),
            "name": row.zone,
        }]

    return json_response({'data': zones_list})