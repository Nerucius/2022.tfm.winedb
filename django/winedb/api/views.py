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

    print('ml_path')
    print(ml_path)

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

