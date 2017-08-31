from flask import Flask, request
import json
from pymessenger import Bot
from utils import apiai_response

app=Flask(__name__)

FB_ACCESS_TOKEN="EAATV9pNU1MgBAPFYX3xAM6TBlytMHPtjZCLTWWoVhp4lHj48l0GeVCdqrDPGotJBFCzPxcm5ReT7eLSZBsZCRgPOdlro1MhOt67GKeoaKpFnY8sDOPjHhimMMXCcAjTHZC1Azw7ZA7ZBZCCL36Nq5gvZC7buje71q7uk6BPjZBajSegZDZD"
bot=Bot(FB_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	print (data)
	if data['object'] == "page":
		entries=data['entry']
		for entry in entries:
			messaging = entry['messaging']
			for messaging_event in messaging:
				sender_id=messaging_event['sender']['id']
				recipient_id=messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if messaging_event['message'].get('text'):
						query=messaging_event['message']['text']
						'''
						reply =fetch_reply(query, sender_id)
						bot.send_text_message(sender_id, reply['data'])
						'''
						#bot.send_image_url(sender_id, "http://www.hotel-r.net/im/hotel/it/blue-beach-21.jpg")
						'''
						buttons=[{"type":"web_url", "url":"https://www.google.com", "title":"visit our page"}]
						bot.send_button_message(sender_id, "check out this website", buttons)
'''

						buttons=[{"type":"postback", "payload":"SHOW_HELP", "title":"visit our page"}]
						bot.send_button_message(sender_id, "check out this website", buttons)

				elif messaging_event.get('postback'):
					if messaging_event['postback']['payload'] == 'SHOW_HELP':
						bot.send_text_message(sender_id, "Check this you")


	return "ok", 200

#use_reloader=True
if __name__=='__main__':
	app.run(debug=True, port=5000)