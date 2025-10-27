import pandas as pd
import numpy as np
from collections import defaultdict
import os
import csv
import json

PREFIX = "../"

def get_points_from_ritem(rubric, r_item):
    assert len(r_item) == 2

    r_number = int(r_item[0])-1 #index from 0
    sub_item = ord(r_item[1])-ord('a')

    return rubric[r_number]["subitems"][sub_item]["points"]


def calculate_score(rubric, r_deducted):
    totals = []
    points = []
    for rubric_item in rubric:
        totals += [rubric_item["points"]]
        points += [rubric_item["points"]]

    if r_deducted:
        for rubric_item_deducted in r_deducted.split(","):
            #print(rubric_item_deducted)
            r_number = int(rubric_item_deducted[0])-1 #index from 0

            points[r_number] -= get_points_from_ritem(rubric, rubric_item_deducted)

    score = 0
    for total, point in zip(totals, points):
        score += float(point) / float(total)

    return score / len(totals)

def get_size_from_csv(csv_path):
    """
    Returns:
      scores_lang: np.ndarray shape (20, 5) 
    """
    df = pd.read_csv(csv_path)
    # Extract the 'Value' column which contains the cost data
    costs = df['Size'].values
    models = df['Model'].values
    return costs, models


def get_all_scores():
    all_lang_scores = defaultdict(list)
    col_labels = []
    for LANG in ["java", "py", "cpp"]:
        all_q_scores = defaultdict(list)

        for SAMPLE_NUM in range(1,6):
            col_labels += [LANG.capitalize() + " " + str(SAMPLE_NUM)]
            f_csv = f"{LANG}{SAMPLE_NUM}.csv"
            f_results = PREFIX + f"results/rubric-applications/{f_csv}"
            f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

            if not os.path.exists(f_results):
                continue

            rubric = json.load(open(f_rubrics))

            all_scores = defaultdict(list)

            with open(f_results) as f:
                reader = csv.reader(f)

                next(reader)

                for row in reader:
                    model = row[0]
                    trial_num = row[1]
                    r_deducted = row[2]

                    all_scores[model].append(calculate_score(rubric, r_deducted))

            for k, v in all_scores.items():
                average = sum(v) / len(v)
                all_q_scores[k].append(average)
                all_lang_scores[k].append(average*100)

    return all_lang_scores


def get_costs_from_csv(csv_path):
    """
    Returns:
      scores_lang: np.ndarray shape (20, 5) 
    """
    df = pd.read_csv(csv_path)
    # Extract the 'Value' column which contains the cost data
    costs = df['Cost'].values
    models = df['Model'].values
    return costs, models



total_costs, techniques = get_costs_from_csv("costs.csv")
data = get_all_scores()
#print(data)

values = list(data.values())
averages = [sum(v)/len(v) for k, v in data.items() if k in techniques]
keys = list(data.keys())

scores = averages
costs = total_costs #mean_costs


#Cost results
results = []
for model, cost, score in zip(techniques, costs, scores):
    if np.isnan(cost): 
        continue
    cost_ratio = (cost / score) * 100
    results.append((model, cost, score, cost_ratio))

# Sort by cost ratio (ascending - best value first)
results.sort(key=lambda x: x[3])


print("======================================================")
print("============= Proprietary Models =====================")
print("======================================================")
print()
for model, cost, score, cost_ratio in results:
    print(model)
    print("Cost:", cost, f"Score: {score:.2f}%")
    print(f"Ratio: {cost_ratio:.3f}")
    print("----------------------------------------------------------")
    print()

print()
print()

sizes, techniques = get_size_from_csv("sizes.csv") 
averages = [sum(v)/len(v) for k, v in data.items() if k in techniques]
scores = averages

#Size results
results = []
for model, size, score in zip(techniques, sizes, scores):
    if np.isnan(size): 
        continue
    size_ratio = (size / score) * 100
    results.append((model, size, score, size_ratio))

# Sort by cost ratio (ascending - best value first)
results.sort(key=lambda x: x[3])

print("======================================================")
print("============= Open Source Models =====================")
print("======================================================")
print()

for model, size, score, size_ratio in results:
    print(model)
    print("Number of Parameters:", size, f"Score: {score:.2f}%")
    print(f"Ratio: {size_ratio:.3f}")
    print("----------------------------------------------------------")
    print()





