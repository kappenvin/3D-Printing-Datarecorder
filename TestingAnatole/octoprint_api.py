"""
Convenient functions to communicate with octoprint's api
"""
import requests


def get_octoprint_response(api_key="896D4E06F1454B9CA27511794B2AC7CD",octoprint_server="http://imi-octopi01.imi.kit.edu/api/job"):
    headers = {'X-Api-Key': api_key}

    response = requests.get(octoprint_server, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return True,data
    else:
        print('Error:', response.status_code)
        return False ,None 