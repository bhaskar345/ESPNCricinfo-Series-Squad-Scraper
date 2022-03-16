import requests
from bs4 import BeautifulSoup
import re

from espnapp.models import Players, Squads
from espnapp.serializers import SquadSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class Scrape_Squads(GenericAPIView):
    serializer_class = SquadSerializer

    def post(self, request):
        try:
            data = request.data
            Url = data['url']
            x = re.match('/', Url)
            if x is not None:
                url = Url
            else:
                url = Url+'/'
            url = url+"squads"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html5lib')
            anchors = soup.find_all('a', attrs={
                'class': 'black-link d-none d-md-inline-block pl-2'
                })
            series = soup.find('h5', class_='header-title label')
            for i in anchors:
                new_url = "https://www.espncricinfo.com"+i['href']
                rr = requests.get(new_url)
                soup = BeautifulSoup(rr.content, 'html5lib')
                names = soup.find_all('a', attrs={
                    'class': 'h3 benton-bold name black-link d-inline'
                    })
                roles = soup.find_all('div', attrs={
                    'class': 'mb-2 mt-1 playing-role benton-normal'
                    })
                age = soup.find_all('div', attrs={
                    'class': 'gray-700 benton-normal meta-info'
                })
                player_names = []
                player_role = []
                player_age = []
                for name in names:
                    player_names.append(name.text)
                for role in roles:
                    player_role.append(role.text)
                for ag in age:
                    player_age.append(ag.text)
                squad_obj, created = Squads.objects.get_or_create(
                        name=i.text, series=series.text
                        )
                players = zip(player_names, player_role, player_age)
                for name, role, age in players:
                    got, _ = Players.objects.get_or_create(
                        name=name,
                        role=role,
                        age=age
                        )
                    squad_obj.squad.add(got)
            queryset = Squads.objects.filter(series=series.text)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({
                "ok": False,
                "message": "Internal Server Error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_Squads(GenericAPIView):
    queryset = Squads.objects.all()
    serializer_class = SquadSerializer

    def get(self, request):
        queryset = Squads.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        by_name = data['series']
        queryset = Squads.objects.filter(series=by_name)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
