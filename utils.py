
import apiai
import json
import requests
from pymongo import MongoClient



def getRECORDS(user_id):
    records = News_Records.find({"sender_id":user_id})
    return records

def pushRECORD(record):
    News_Records.insert_one(record)

MONGODB_URI = "mongodb://Aditya:Aditya@ds013599.mlab.com:13599/newsbot"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
db = client.get_default_database()
News_Records=db.News_Records


record = {
	"sender_id": "1234",
	"news_type": "sports",
	"language":"hindi",
	"geo-country":"india"
		}
pushRECORD(record)
APIAI_ACCESS_TOKEN = "af34399a8fd6411780f2b326a8983b57"
ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)


GNEWS_API_ENDPOINT = "https://gnewsapi.herokuapp.com"


def get_news(params):
	params['news'] = params['news_type']
	resp = requests.get(GNEWS_API_ENDPOINT, params = params)
	return resp.json()

def apiai_response(query, session_id):
	"""
	function to fetch api.ai response
	"""
	request = ai.text_request()
	request.lang='en'
	request.session_id=session_id
	request.query = query
	response = request.getresponse()
	return json.loads(response.read().decode('utf8'))


def parse_response(response):
	"""
	function to parse response and 
	return intent and its parameters
	"""
	result = response['result']
	params = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, params

	
def fetch_reply(query, session_id):
	"""
	main function to fetch reply for chatbot and 
	return a reply dict with reply 'type' and 'data'
	"""
	response = apiai_response(query, session_id)
	intent, params = parse_response(response)

	reply = {}

	if intent == None:
		reply['type'] = 'none'
		reply['data'] = "I didn't understand"

	elif intent == "news":
		reply['type'] = 'news'
		print(params)
		params['sender_id']=session_id
		pushRECORD(params)
		articles = get_news(params)
		news_elements = []

		for article in articles:
			element = {}
			element['title'] = article['title']
			element['item_url'] = article['link']
			element['image_url'] = article['img']
			element['buttons'] = [{
				"type":"web_url",
				"title":"Read more",
				"url":article['link']}]
			news_elements.append(element)

		reply['data'] = news_elements

	elif intent.startswith('smalltalk'):
		reply['type'] = 'smalltalk'
		reply['data'] = response['result']['fulfillment']['speech']

	return reply