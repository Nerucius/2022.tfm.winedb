from django.shortcuts import render, HttpResponse

import json
import pickle
import os
import sys

# Create your views here.
def dummy(request, *args, **kwargs):
    return HttpResponse(
        json.dumps({'response': True, 'request': kwargs}),
        'application/json'
    )

def wine_recommender_similarity(request, wine_id):
    ml_path = os.path.join(os.path.dirname(__file__), 'ml')
    sys.path.append(ml_path)

    filename = os.path.join(ml_path, 'CBR.pickle')
    file_to_read = open(filename, "rb")
    loaded_predictor = pickle.load(file_to_read)
    file_to_read.close()

    # Returns pandas 
    predictions = loaded_predictor.predict(wine_id)

    return HttpResponse(
        # json.dumps({'response': True, 'request': kwargs}),
        predictions.to_json(index=True),
        'application/json'
    )


def predict_do(request, *args, **kwargs):
    mock_data = {
        'Priorat  D.O.  Ca.  / D.O.P.': 0.55,
        'Tarragona  D.O.  / D.O.P.': 0.55,
        'Catalunya  D.O.  / D.O.P.': 0.55,
    }

    ml_path = os.path.join(os.path.dirname(__file__), 'ml')
    sys.path.append(ml_path)

    filename = os.path.join(ml_path, 'predictDO.pickle')
    file_to_read = open(filename, "rb")
    loaded_predictor = pickle.load(file_to_read)
    file_to_read.close()

    predictions = loaded_predictor.predict_do(request.GET['style'].split(','))

    return HttpResponse(
        # json.dumps({'response': mock_data}),
        json.dumps({'response': predictions}),
        'application/json'
    )