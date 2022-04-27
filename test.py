# from newsapi import NewsApiClient
# import requests
import json
from textwrap import indent

# # Init
# newsapi = NewsApiClient(api_key='4d05b1bf662540e38cdcb3f04920577f')

# # /v2/top-headlines
# # top_headlines = newsapi.get_top_headlines(q='bitcoin',
# #                                           sources='bbc-news,the-verge',
# #                                           category='business',
# #                                           language='en',
# #                                           country='us')


# # all_articles = newsapi.get_everything(sources='bbc-news,the-verge',
# #                                       domains='bbc.co.uk,techcrunch.com',
# #                                       language='en',
# #                                       sort_by='relevancy',
# #                                       page_size=6, page=1)
# # obj = json.dumps(all_articles)
# # print(obj[0])
# # print(type(all_articles['articles']))
# # for a in all_articles['articles']:
# #     print(a['urlToImage'])
# top_headlines = newsapi.get_everything(q='nation', sort_by='relevancy', page_size=6)
# # for a in top_headlines['articles']:
# #     print(a)
# print(top_headlines)
# # head = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=4d05b1bf662540e38cdcb3f04920577f')
# # data =  head.json()
# # print(data['articles']['content'])

# # print(type(all_articles))

import requests
# https://api.spoonacular.com/recipes/716429/information?apiKey=YOUR-API-KEY&query=pasta&number=4.
# url = "https://api.spoonacular.com/recipes/716429/information?apiKey=8a6ee8966fe247379c25ad712bed89be&query=pasta&number=4"
# head = requests.get(url)
# data = head.json()
# print(data)
# print(data['full_description'])
# for a in data['results']:
#     if 'full_description' not  in a:
#         pass
#     else:
#         print(a['full_description']);


url = 'https://google-image-search1.p.rapidapi.com/v2/'
body = (requests.get(url, headers={'X-RapidAPI-Host': 'google-image-search1.p.rapidapi.com',
                                   'X-RapidAPI-Key': 'b9b819f078msh00513684be592cep108941jsnbab9a046cec7'}, 
             params={'q': 'pasta'})).json()

# print(json.dumps(body, indent=4))
# print(json.dumps(body['value'][1], indent=4))
print(json.dumps(body["response"]["images"][0]["image"]["url"], indent=4))
