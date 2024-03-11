from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import os

import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Test(APIView):
    def get(self, request):
        # Check PostgreSQL connection
        try:
            # Use a simple query to test the connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row:
                    connected = True
                else:
                    connected = False
        except Exception as e:
            connected = False

        if connected:
            message = 'PostgreSQL server is connected.'
        else:
            message = 'Failed to connect to PostgreSQL server.'

        return Response({'message': message})

    def post(self, request):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        url = request.data.get('url')
        driver.get(url)
        # print(driver.page_source)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # print(soup.prettify())

        # # save the page source to a file
        # with open("ajio.html", "w", encoding="utf-8") as file:
        #     file.write(soup.prettify())

        # close the webdriver
        driver.quit()
        # return the soup as a response
        return Response(soup.prettify())
