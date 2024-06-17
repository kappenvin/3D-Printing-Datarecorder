import requests

def get_cotoprint_response(api_key="EA53ADC39AD34E9B969E49D9DD82CD99",octoprint_server="http://192.168.2.108/api/job"):
    headers = {'X-Api-Key': api_key}

    response = requests.get(octoprint_server, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return True,data
    else:
        print('Error:', response.status_code)
        return False ,None 
    
if __name__ == "__main__":
    response,data=get_cotoprint_response()

    print(data)