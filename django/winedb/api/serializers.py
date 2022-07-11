from django.core import serializers
import json

class Serializer:

    @staticmethod
    def serialize(obj_list):
        pass


class WineSerializer(Serializer):

    @staticmethod
    def serialize(wine_list):
        wine_json = json.loads(serializers.serialize('json', wine_list))
        wine_list = []

        for wine in wine_json:
            # Serialize wine here
            wine_data = dict()
            wine_data['id'] = wine['pk']
            wine_data.update(wine['fields'])

            wine_data['varieties'] = wine_data['varieties'].split(',') if wine_data['varieties'] != '' else None
            wine_data['style']     = wine_data['style'].split(',')     if wine_data['style'] != ''     else None
            wine_data['mouth']     = wine_data['mouth'].split(',')     if wine_data['mouth'] != ''     else None
            wine_data['color']     = wine_data['color'].split(',')     if wine_data['color'] != ''     else None
            wine_data['smell']     = wine_data['smell'].split(',')     if wine_data['smell'] != ''     else None

            # wine_data['$link'] = resolve_url('api-wine-detail', wine_id=wine_data["id"])

            wine_list += [wine_data]

        return wine_list
