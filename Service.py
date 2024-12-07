import requests
from DataModel import DataModel
import json


class Service:
    def __init__(self):
        self.API_URL = "http://127.0.0.1:9883/api/en"
        self.AUTH_TOKEN = "Token 8e10dc176d185e450bae2f417bfe0ea7dd9501ea"

    def SaveScrappedFaces(self, data: dict):
        try:
            url = f"{self.API_URL}/faces/scrapped/save/"
            payload = json.dumps(data)
            headers = {
                "Authorization": self.AUTH_TOKEN,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return json.loads(response.text)
        except:
            return None

    def UpdatePage(self, indexId, sourcePageUrl, last_page_index, is_indexed=True):
        url = f"{self.API_URL}/page/update/"
        try:
            payload = json.dumps(
                {
                    "index": indexId,
                    "last_page_index": last_page_index,
                    "sourcePageUrl": sourcePageUrl,
                    "is_indexed": is_indexed,
                }
            )
            headers = {
                "Authorization": self.AUTH_TOKEN,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return json.loads(response.text)
        except:
            return None

    def UpdateIndexIndexedStatus(self, indexId, indexUrl, is_indexed=True):
        try:
            url = f"{self.API_URL}/update/indexing/{indexId}/"
            payload = json.dumps(
                {"homeUrl": indexUrl, "is_indexed": is_indexed, "is_disabled": False}
            )
            headers = {
                "Authorization": self.AUTH_TOKEN,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return json.loads(response.text)
        except:
            return None

    def UpdateIndexIndexedStatus(self, indexId, indexUrl, last_page_index=0):
        try:
            url = f"{self.API_URL}/update/indexing/{indexId}/"
            payload = json.dumps(
                {
                    "homeUrl": indexUrl,
                    "last_page_index": last_page_index,
                    "is_indexed": "",
                    "is_disabled": "",
                }
            )
            headers = {
                "Authorization": self.AUTH_TOKEN,
                "Content-Type": "application/json",
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            return json.loads(response.text)
        except:
            return None

    def getAllIndexs(self, page=1, perpage=500):
        try:
            url = f"{self.API_URL}/indexing/?page={page}&perpage={perpage}"
            headers = {"Authorization": self.AUTH_TOKEN}
            response = requests.request("GET", url, headers=headers)
            # print(response.text)
            return json.loads(response.text)
        except:
            return None

    def getFaces(self, page=1, perpage=500):
        try:
            url = f"{self.API_URL}/faces/?page={page}&perpage={perpage}"
            payload = ""
            headers = {"Authorization": self.AUTH_TOKEN}
            response = requests.request("GET", url, headers=headers, data=payload)
            return json.loads(response.text)
        except:
            return None

    def getErrorResponse(self, message, action, clientId, taskId=None):
        response = DataModel()
        response.addProperty("clientId", clientId)
        response.addProperty("taskId", taskId)
        response.addProperty("message", message)
        response.addProperty("action", action)
        response.addProperty("state", "ERROR")
        return response.getAsJsonString()
