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

            wine_data['varieties'] = sorted(wine_data['varieties'].split(',')) if wine_data['varieties'] != '' else []
            wine_data['style']     = sorted(wine_data['style'].split(','))     if wine_data['style'] != ''     else []
            wine_data['mouth']     = sorted(wine_data['mouth'].split(','))     if wine_data['mouth'] != ''     else []
            wine_data['color']     = sorted(wine_data['color'].split(','))     if wine_data['color'] != ''     else []
            wine_data['smell']     = sorted(wine_data['smell'].split(','))     if wine_data['smell'] != ''     else []

            # wine_data['$link'] = resolve_url('api-wine-detail', wine_id=wine_data["id"])

            wine_list += [wine_data]

        return wine_list
