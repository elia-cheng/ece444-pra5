import requests

AWS_URL = "http://serve-sentiment-env.eba-yuybw6m2.us-east-2.elasticbeanstalk.com/predict"

testcases = {
    "fake_1": "Cure for cancer found in an unlikely place: unglazed fired clay",
    "real_1": "MLB voters decide the Blue Jays’ John Schneider isn’t AL manager of the year. But he won something better",
    "fake_2": "New hero arises as a 'Tyrant of the night', is this an evil Batman?",
    "real_2": "Toronto Hydro was asked to fix a wire sticking out of the middle of a sidewalk. Here’s what it did instead"
}

for news_type, headliner in testcases.items():
    response = requests.post(AWS_URL, json={"message": headliner})
    if response.status_code == 200:
        print(news_type + ": Predition ==> " + response.json()['label'])
    else:
        print(news_type + ": Predition ==> " + response.json().get('error'))