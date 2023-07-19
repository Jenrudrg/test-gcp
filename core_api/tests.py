from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
import time
from .endpoints import ArticuloListAPIView, BreakingNewsAPIView

class ArticuloListAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ArticuloListAPIView.as_view()
        
    def test_listado_articulos(self):

        # Define los parámetros de prueba
        keywords = "example"
        language = "en"
        country = "us"
        max_results = 5
        sorting = "publishedAt"
        date_from = "2022-01-01"
        date_to = "2022-12-31"

        # Crea una solicitud GET para el endpoint
        url = f'/api/articulos/?keywords={keywords}&language={language}&country={country}&max_results={max_results}&sorting={sorting}&date_from={date_from}&date_to={date_to}'
        request = self.factory.get(url)
        
        # Obtiene la respuesta del endpoint
        response = self.view(request)
        
        # Verifica el código de respuesta esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica que se devuelva una lista de artículos
        self.assertIsInstance(response.data, list)
        
        # Verifica la cantidad de artículos devueltos (máximo 10 según tu requerimiento)
        self.assertLessEqual(len(response.data), 10)


class BreakingNewsAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BreakingNewsAPIView.as_view()
        
        
    
    def test_most_recent_articles(self):

        url = '/api/breaking-news/'

        # Realiza la solicitud GET al endpoint
        request = self.factory.get(url)

        # Obtiene la respuesta del endpoint
        response = self.view(request)

        # Verifica el código de respuesta esperado
        self.assertEqual(response.status_code, 200)

        # Verifica que se devuelva una lista de artículos
        self.assertIsInstance(response.data, list)

        # Verifica que al menos un artículo esté presente
        self.assertGreater(len(response.data), 0)

        # Verifica que los artículos estén ordenados por fecha de publicación descendente
        articles = response.data
        for i in range(len(articles) - 1):
            self.assertGreaterEqual(articles[i]["publishedAt"], articles[i + 1]["publishedAt"])


class APIDocsTestCase(TestCase):
    def setUp(self):
        self.url = '/api/docs/'
    
    def test_api_docs(self):
        # Realiza la solicitud GET al endpoint
        response = self.client.get(self.url)

        # Verifica el código de respuesta esperado
        self.assertEqual(response.status_code, 200)

        # Verifica que el contenido de la respuesta contenga la cadena "swagger-ui"
        self.assertIn("swagger-ui", response.content.decode())

# python manage.py test 