import requests
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plot

AWS_URL = "http://serve-sentiment-env.eba-yuybw6m2.us-east-2.elasticbeanstalk.com/predict"
NUM_RUNS = 100
CSV_FILE = 'results.csv'

testcases = {
    "fake_1": "Cure for cancer found in an unlikely place: unglazed fired clay",
    "real_1": "MLB voters decide the Blue Jays’ John Schneider isn’t AL manager of the year. But he won something better",
    "fake_2": "New hero arises as a 'Tyrant of the night', is this an evil Batman?",
    "real_2": "Toronto Hydro was asked to fix a wire sticking out of the middle of a sidewalk. Here’s what it did instead"
}

latency = {name: [] for name in testcases.keys()}

for news_type, headliner in testcases.items():
    print("Running test on " + news_type + "...")
    for _ in range(NUM_RUNS):
        current = datetime.now().isoformat()
        start = time.time()
        response = requests.post(AWS_URL, json={"message": headliner})
        end = time.time()
        latency_data = (end - start)*1000
        latency[news_type].append(latency_data)

        with open(CSV_FILE, 'a', newline="") as c:
            input_data = csv.writer(c)
            input_data.writerow([news_type, current, latency])

with open(CSV_FILE, 'w', newline="") as c:
    input_data = csv.writer(c)
    input_data.writerow(["testcase", "timestamp", "latency (ms)"])

    for name, value in latency.items():
        for i, l in enumerate(value):
            timestamp = datetime.now().isoformat()
            input_data.writerow([name, timestamp, l])

plot.figure(figsize=(12, 8))
plot.boxplot(latency.values(), labels=latency.keys())
plot.ylim(50, 250)
plot.ylabel("Latency (ms)")
plot.title("Response Time / Testcase")
plot.tight_layout()  # automatically adjusts spacing to prevent overlap
plot.show()

for name, value in latency.items():
    average = sum(value) / len(value)
    print(name + ": Average latency is " + str(average) + " ms")