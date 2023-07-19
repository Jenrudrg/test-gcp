import urllib.request
import json
import time
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.request import urlopen
from test_gcp.credentials import API_KEY
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ArticuloListAPIView(APIView):
    
    """
        Listado de articulos
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description="Buscar por título o contenido", type=openapi.TYPE_STRING, default='Example'),
            openapi.Parameter('fecha_desde', openapi.IN_QUERY, description="Fecha mínima de publicación", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('fecha_hasta', openapi.IN_QUERY, description="Fecha máxima de publicación", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('orden', openapi.IN_QUERY, description="Ordenar por fecha de publicación ('asc' o 'desc')", type=openapi.TYPE_STRING),
        ]
    )

    
    def get(self, request):

        # Agrega un retraso de 0.7 para asegurar que la api externa siempre responda
        time.sleep(0.7)

        base_url = "https://gnews.io/api/v4/search"
        api_key = API_KEY


        # Obtener los parámetros de consulta de la solicitud
        keywords = request.GET.get('keywords', '')  # Palabras clave para buscar artículos
        language = request.GET.get('language', 'en')  # Idioma de los artículos
        country = request.GET.get('country', 'us')  # País de publicación de los artículos
        max_results = int(request.GET.get('max_results', 10))  # Número máximo de artículos a devolver
        sorting = request.GET.get('sorting', 'publishedAt')  # Orden de los artículos (por fecha de publicación)
        date_from = request.GET.get('date_from', '')  # Fecha de inicio del rango
        date_to = request.GET.get('date_to', '')  # Fecha de fin del rango

        # Construir los parámetros de consulta
        query_params = {
            "q": keywords,
            "lang": language,
            "country": country,
            "max": max_results,
            "sortby": sorting,
            "from": date_from,
            "to": date_to
        }

        # Agregar la API Key al diccionario de parámetros
        query_params["apikey"] = api_key

        # Codificar los parámetros de consulta en la URL
        encoded_params = urllib.parse.urlencode(query_params)

        # Construir la URL completa
        url = f"{base_url}?{encoded_params}"
        # print(url)
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))

                articles = data["articles"]
                
                results = []
                for article in articles:
                    result = {
                        "title": article["title"],
                        "description": article["description"],
                        # Puedes agregar más propiedades del artículo según las necesidades
                    }
                    results.append(result)

        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al realizar la solicitud
            return Response({"error": str(e)}, status=400)
        
        print(results)
        return Response(results)



class BreakingNewsAPIView(APIView):
    """
        Obtener el artículo más relevante de cada país
    """
    def get(self, request):

        # Agrega un retraso de 0.7 para asegurar que la api externa siempre responda
        time.sleep(0.7)

        # Definir los países de interés
        countries = ["us", "ru", "ua", "ca", "gb"]
        
        # Crear una lista para almacenar los artículos
        articles = []

        # Obtener el artículo más relevante de cada país
        for country in countries:
            api_key = API_KEY
            url = f"https://gnews.io/api/v4/search?q=example&lang=en&country={country}&max=1&sortby=relevance&apikey={api_key}"
            print(url)
            try:
                # Realizar la solicitud a la API externa
                with urlopen(url) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    article = data["articles"][0]  # Obtener el primer artículo
                    
                    # Agregar el artículo a la lista
                    articles.append(article)
            
            except Exception as e:
                # Manejar cualquier error que pueda ocurrir al realizar la solicitud
                return Response({"error": str(e)}, status=400)

        # Ordenar los artículos por fecha de publicación descendente (más reciente primero)
        articles.sort(key=lambda x: x["publishedAt"], reverse=True)

        return Response(articles)