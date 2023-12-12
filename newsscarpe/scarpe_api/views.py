from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import News
from .serializers import NewsSerializer
import requests
from bs4 import BeautifulSoup

@api_view(['GET'])
def scrape_and_fetch_news(request):
    try:
        base_url = "https://www.onlinekhabar.com/"
        category = request.query_params.get('category')
        url = f"{base_url}{category}"
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        scraped_news = []  # Initialize the list here

        if category == "content/news":
            headlines = soup.select('.ok-news-post')
            for headline in headlines:
                link_element = headline.find('a')
                title_element = headline.find('h2', class_='ok-news-title-txt')
                if link_element and title_element:
                    link = link_element.get('href')
                    title = title_element.text.strip()
                    image = title_element.get('src')
                    # contents = []  # You may want to improve this

                    # Use Django ORM to save data
                    news_instance = News.objects.create(title=title, link=link)

                    # Serialize the news data
                    serializer = NewsSerializer(news_instance)

                    # Convert the serialized data to a JSON-serializable format
                    serialized_data = serializer.data

                    scraped_news.append(serialized_data)
        
        if category == "sports":
            headlines = soup.select('.ok-post-ltr')
            print(headlines)
            for headline in headlines:
                print(headline)
                link_element = headline.find('a')
                title_element = headline.find('h2', class_='ok-news-title-txt')
                if link_element and title_element:
                    link = link_element.get('href')
                    title = title_element.text.strip()
                    image = title_element.get('src')
                    # contents = []

                    # Use Django ORM to save data
                    news_instance = News.objects.create(title=title, link=link)

                    # Serialize the news data
                    serializer = NewsSerializer(news_instance)

                    # Convert the serialized data to a JSON-serializable format
                    serialized_data = serializer.data

                    scraped_news.append(serialized_data)

        if category == "business":
            headlines = soup.select('.ok-post-ltr')
            print(headlines)
            for headline in headlines:
                print(headline)
                link_element = headline.find('a')
                title_element = headline.find('h2', class_='ok-news-title-txt')
                if link_element and title_element:
                    link = link_element.get('href')
                    title = title_element.text.strip()
                    # contents = []

                    # Use Django ORM to save data
                    news_instance = News.objects.create(title=title, link=link)

                    # Serialize the news data
                    serializer = NewsSerializer(news_instance)

                    # Convert the serialized data to a JSON-serializable format
                    serialized_data = serializer.data

                    scraped_news.append(serialized_data)

        # Add similar blocks for other categories if needed

        return Response({'news': scraped_news}, status=200)

    except requests.exceptions.RequestException as e:
        return Response({'error': f"Error: {e}"}, status=500)

    except Exception as e:
        return Response({'error': f"An unexpected error occurred: {e}", 'news': []}, status=500)

@api_view(['GET'])
def fetch_News(request):
    try:
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f"An unexpected error occurred: {e}"}, status=500)
