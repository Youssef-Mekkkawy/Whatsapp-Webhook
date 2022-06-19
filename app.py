import os
import json
import requests
from flask_ngrok import run_with_ngrok
from dotenv import load_dotenv
from flask import Flask, request

from colorama import Fore

# env

load_dotenv(".env")
Access_Token = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('SECRET_KEY')
Authorization = os.getenv('Authorization')

# Send Message

def Send_Message(phone_number_id:int, From:int, msg_body:str, Message_ID):
    # Base Url 

    #  Your Version -> v13.0 or 14.0 
    Version = "v14.0"

    # To Send Message.
    Method = "messages"
    url = f"https://graph.facebook.com/{Version}/{phone_number_id}/{Method}"

    headers = {
        # Your access Token.
     	'Authorization': f'Bearer {Access_Token}',
     	'Content-Type': 'application/json'
		}

    DATAS = {
        "messaging_product": "whatsapp",
	    "recipient_type": "individual",
        # From is Number You Send Message To.
	    "to": From,
	    "type": "text",
	    "text": {
	    	"preview_url": False,
            # Your Message You need To Sended
	    	"body": msg_body
	    }
    }
    payload = json.dumps(DATAS)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    Make_as_Read(phone_number_id, Message_ID)
    return "", 200

# Make Message Read.
def Make_as_Read(phone_number_id, ID):
        url = f"https://graph.facebook.com/v14.0/{phone_number_id}/messages"
        headers = {
         	'Authorization': f'Bearer {Access_Token}',
         	'Content-Type': 'application/json'
    	}
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": ID   
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        return "", 200

# Flask Start
app = Flask(__name__)
def Ngrok():
    # Ngrok build In
    # Need To Download ngrok from Website -> https://ngrok.com
    # Don't Forget To Auth Your Token by using Command.
    # ngrok config add-authtoken {Your Token}
    run_with_ngrok(app)
app.config["SECRET_KEY"] = VERIFY_TOKEN


# Get 
@app.route('/', methods = ["GET", "POST"])
def home():
    with open("Html_Code/Html.html") as Html_Code:
        html = Html_Code.read()
    return html, 404

@app.route('/webhook', methods = ["GET"])
def Webhook():
    # Challange.
    if request.method == "GET":
    
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            # print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            # print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            # print(challenge)
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print(Fore.GREEN + "webhook VERIFIED"+ Fore.RESET)
                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                print(Fore.RED + "webhook UNVERIFIED "+ Fore.RESET)
                return "ERROR", 400
        return 300

@app.route('/webhook', methods = ["POST"])
def index():

    """ Get request """

    # Response From Server.
    if request.method == "POST":
        
        # Data From Server
        data = request.data

        req = data.decode("utf-8")

        if req == "" or req == None:
            return "No Data Found"

        body = json.loads(req)
        if "messages" in body["entry"][0]["changes"][0]["value"].keys():
            # Id OF Your Phone Number
            phone_number_id = body['entry'][0]['changes'][0]["value"]["metadata"]["phone_number_id"]
            # Number How Send This Message.
            From = body['entry'][0]['changes'][0]["value"]["messages"][0]["from"]
            # Messagge
            msg_body = body['entry'][0]['changes'][0]["value"]["messages"][0]["text"]["body"]
            # Message id To Make Read.
            message_ID = body['entry'][0]['changes'][0]["value"]["messages"][0]["id"]
            # Function.
            Send_Message(phone_number_id, From, msg_body, message_ID)
            return "", 200 
        else:
            return "", 200

# Flask End  
if __name__ == '__main__':
    # Ngrok build In
    # Need To Download ngrok from Website -> https://ngrok.com
    # Don't Forget To Auth Your Token by using Command.
    # ngrok config add-authtoken {Your Token}
    
    # True -> Enable. | False -> Not Enable.
    Enable_Ngrok = True
    
    
    if Enable_Ngrok == True:
        Ngrok()
         
    try:

        app.run() 

    except Exception as e:
        print(f"Error is {e}")
