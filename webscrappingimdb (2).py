# -*- coding: utf-8 -*-
"""WebScrappingIMDB

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uTWmCivC0CSQ-32OJzAjpjuMpzVcBMxw
"""

from requests import get
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from warnings import warn
import pandas as pd

pages = np.arange(1,5,50)
headers = {'Accept-Language':'pt-BR,pt;q=0.8'}
titles = []
years = []
genres = []
runtimes = []
imdb_ratings = []
votes = []
ratings = []

for page in pages:
  response = get("https://www.imdb.com/search/title?genres=sci-fi&" + "start=" + str(page) + "&explore=title_type,genres&ref_=adv_prv", headers=headers)
  sleep(randint(5,10))

  if response.status_code != 200:
    warn("O pedido:{}; retornou o codigo:{}".format(requests, response.status_code))

  page_html = BeautifulSoup(response.text, 'html.parser')  
  movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
  for container in movie_containers:
    if container.find('div', class_ = 'ratings-metascore') is not None:
      title = container.h3.a.text
      titles.append(title) 
      
      #captura o ano
      if container.h3.find('span', class_ = 'lister-item-year text-muted unbold') is not None:
        year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
        years.append(year)
      else:
        years.append(None)

      #captura as avaliações
      if container.p.find('span', class_ = 'certificate') is not None:
        rating = container.p.find('span', class_ = 'certificate').text
        ratings.append(rating)
      else: 
        rating.append("")

      #Captura os generos
      if container.p.find('span', class_ = 'genre') is not None:
         genre = container.p.find('span', class_ = 'genre').text.replace("\n","").rstrip().split(',')
         genres.append(genre) 
      else:    
          genres.append("")

      #captura a duração do filme
      if container.p.find('span', class_ = 'runtime') is not None:
        time = int(container.p.find('span', class_ = 'runtime').text.replace("min", ""))
        runtimes.append(time)
      else:
        runtimes.append(None)

      #cptura a avaliação do imdb
      if container.strong.text is not None:
        imdb = float(container.strong.text.replace(",","."))
        imdb_ratings.append(imdb)
      else:
        imdb_ratings.append(None)

      #captura os votos dos usuarios
      if container.find('span', attrs = {'name':'nv'})['data-value'] is not None:  
        vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
        votes.append(vote)
      else:
        votes.append(None)

sci_fi_df = pd.DataFrame({'Filmes':titles,'Ano':years,'Genero':genres,'Tempo':runtimes,'IMDB':imdb_ratings,'Votos':votes, 'NOta Usuario':ratings})
sci_fi_df

import seaborn as sns
import matplotlib.pyplot as plt

plt.scatter(sci_fi_df["Tempo"],sci_fi_df["IMDB"])
plt.xlabel("Duração (min)")
plt.ylabel("Nota IMDB)")
plt.show()