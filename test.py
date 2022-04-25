# from newsapi import NewsApiClient
# import requests
# import json

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
url = "https://newsdata.io/api/1/news?apikey=pub_6815be6a7b827d46e97ae53a029593da3aea&language=en"
head = requests.get(url)
data = head.json()
print(data['results'])
# print(data['full_description'])
# for a in data['results']:
#     if 'full_description' not  in a:
#         pass
#     else:
#         print(a['full_description']);
