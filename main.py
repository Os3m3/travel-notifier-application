import config
import requests
import json
from dotenv import load_dotenv
import os
import database

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_MINTOR-MIND_WEBHOOK")


url = "https://routes.googleapis.com/directions/v2:computeRoutes"

payload = json.dumps({
  "origin": {
    "address": config.SOURCE
  },
  "destination": {
    "address": config.DESTI
  },
  "travelMode": config.mode,
  "routingPreference": "TRAFFIC_AWARE"
})
headers = {
  'Content-Type': 'application/json',
  'X-Goog-Api-Key': GOOGLE_API_KEY,
  'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
}

response = requests.request("POST", url, headers=headers, data=payload)
json_format = response.json()

arival_destance = json_format["routes"][0]["distanceMeters"]
arival_destance_km = arival_destance / 1000

arival_time = json_format["routes"][0]["duration"]
arival_time_to_int = int(arival_time.replace("s", ""))
arival_time_min = arival_time_to_int // 60


# Database Insert

database.cur.execute("INSERT INTO travel_data VALUES(?, ?, ?, ?)", 
(config.SOURCE, config.DESTI, arival_destance_km, arival_time_min)
)
database.con.commit()



# Slack Notification

message = (
    f"🧭 *Travel Notification*\n"
    f"*From:* {config.SOURCE}\n"
    f"*To:* {config.DESTI}\n"
    f"*Distance:* {arival_destance_km:.2f} km\n"
    f"*Estimated Duration:* {arival_time_min} minutes"
)


slack_notification_push = requests.post(
    SLACK_WEBHOOK, 
    json={"text": message}
)