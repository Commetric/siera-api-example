"""Process Articles through Commetric's Siera API

This script is demo of how to send a list of articles to the
Siera API endpoint and check the resulting Siera tags.
The list of articles is currently static and should be
replaced by a database call.
"""

import os
import json
from itertools import islice
import requests
import dotenv

# Load up .env file to allow to update Token if necessary
dotenv_file = dotenv.find_dotenv()

TOKEN = os.getenv('TOKEN', 'Not_Found')
X_API_KEY = os.getenv('X_API_Key', 'Not_Found')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN', 'Not_Found')

BATCH_SIZE = 10  # Limit of Public Siera API

url_version = "https://siera.commetric.cloud/api/v1/version"
url_new_token = "https://siera.commetric.cloud/api/v1/new_token"
url_tag = "https://siera.commetric.cloud/api/v1/tag"


def get_articles() -> list[dict]:
    """Prepare a collection of articles

    Change this function to get articles from a real database

    Returns:
        list: a list of articles (id, title, text)
    """

    return [
        {
            "id": "108201_2793502",
            "title": "Bill to give AZ troopers body cameras would also restrict video release",
            "text": "A proposal to buy body cameras for every Arizona state trooper would also prevent the Department of Public Safety from releasing most of the video to the public.\nWE'LL TAKE A LOOK AT YOURSEVEN DAY COMING UP.",
        },
        {
            "id": "298972_1402",
            "title": "JPMorgan Joins Net Zero Banking Alliance, Committing to Align Lending & Investments with Global Climate Goals",
            "text": "JPMorgan Chase announced that it has joined the Net Zero Banking Alliance, joining its Wall Street peers Bank of America, Citi and Morgan Stanley in signing on to the coalition of banks dedicated to advancing global net zero goals through their financing activities.\nMarisa Buchanan, Managing Director, Global Head of Sustainability at JPMorgan Chase & Co., said in a statement: “We are joining the Net-Zero Banking Alliance because we support the",
        },
        {
            "id": "108201_2793503",
            "title": "Bill to give AZ troopers body cameras would also restrict video release",
            "text": "A proposal to buy body cameras for every Arizona state trooper would also prevent the Department of Public Safety from releasing most of the video to the public.\nWE'LL TAKE A LOOK AT YOURSEVEN DAY COMING UP."
        }
    ]


def get_batches(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, size))
        if not chunk:
            return
        yield chunk


def _call_siera_api(method: str, url: str, data: str) -> dict:
    """Call Siera API function

    Args:
        method (str): HTTP method
        url (str): endpoint url
        headers (str): HTTP headers
        data (str): the request payload

    Returns:
        dict: a json response
    """

    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': X_API_KEY,
            'Token': TOKEN
        }
        response = requests.request(method, url, headers=headers, data=data)
        # response.raise_for_status()
        # print(response.status_code)
        if response.status_code == 200:
            print('Success')
            return response.json()
        elif response.status_code == 401:
            print('Unauthorised. Attempting to generate a new token')
            generate_new_token()
            return _call_siera_api(method, url, data)
            # "Unauthorized"
            # "The incoming token has expired"
        else:
            print(response, response.text)
            raise Exception('Unexpected error', response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        raise Exception('Requests error', e)


def generate_new_token() -> str:
    """Generate New Token

    A new access token is created using the Refresh Token.
    A token has a short lifespan of 24 hours. After that it expires
    and generating a new one is necessary

    Returns:
        str: New token
    """

    global TOKEN

    # Prepare a call to the New Token API endpoint
    print('Renewing Token...')
    payload = json.dumps({"refresh_token": REFRESH_TOKEN})
    response = requests.request("POST", url_new_token, data=payload)

    if response.status_code == 200:
        TOKEN = response.json()['token']
        # Update .env with newly generated token
        dotenv.set_key(dotenv_file, "TOKEN", TOKEN)
    else:
        raise Exception('Failed to generate new token: ', response.text)



def get_version() -> str:
    """Get Siera Rules version

    Returns:
        str: Siera rules version"""

    # Prepare a call to the Siera version API endpoint
    version = _call_siera_api('GET', url_version, None)['version']
    return version


def get_siera_tags(articles: list[dict]) -> dict:
    """Tag articles with Siera

    Args:
        articles (list): List of articles

    Returns:
        dict: a json response (article_id, siera tags)
    """

    # Prepare a call to the Tag API endpoint
    return _call_siera_api('POST', url_tag, json.dumps(articles))


def main():
    # Prepare a collection of Articles
    articles = get_articles()

    # generate_new_token()
    version = get_version()
    print('version', version)

    # Tag using Siera
    # Work in batches (as big as the Siera API would permit)
    for batch in get_batches(articles, BATCH_SIZE):
        print(get_siera_tags(batch))


if __name__ == "__main__":
    main()
