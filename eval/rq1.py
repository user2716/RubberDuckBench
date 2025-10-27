from collections import defaultdict
import json
import csv
import os
import numpy as np

'''
    1. Average across all trials ranked leaderboard. 
    2. Average across each language
    3. Deviation per language
    4. Question type breakdown
'''

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

            points_to_deduct = get_points_from_ritem(rubric, rubric_item_deducted)
            #print(r_number+1, "-",points_to_deduct)
            points[r_number] -= points_to_deduct

    score = 0
    for total, point in zip(totals, points):
        #print(point, "/", total)
        score += float(point) / float(total)

    return score / len(totals) 

def get_points_from_ritem(rubric, r_item):
    assert len(r_item) == 2

    r_number = int(r_item[0])-1 #index from 0
    sub_item = ord(r_item[1])-ord('a')

    return rubric[r_number]["subitems"][sub_item]["points"]


#LANG = "cpp"
#SAMPLE_NUM = 5

def default_bin_dict():
    return {"java": 0, "py": 0, "cpp": 0, "total": 0}


all_lang_scores = defaultdict(list)
binary_scores = defaultdict(default_bin_dict)
binary_scores_all_trials = defaultdict(default_bin_dict)
for LANG in ["java", "py", "cpp"]:
    all_q_scores = defaultdict(list)

    for SAMPLE_NUM in range(1,6):
        f_csv = f"{LANG}{SAMPLE_NUM}.csv"
        f_results = f"../results/rubric-applications/{f_csv}"
        f_rubrics = f"../dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

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
                
                #print(model)
                all_scores[model].append(calculate_score(rubric, r_deducted))


        max_key_length = max(len(str(k)) for k in all_scores.keys())

        print("--------------------------------------")
        print("Scores for question:", SAMPLE_NUM)
        '''
        for k, v in all_scores.items():
            average = sum(v) / len(v)
            print(f"{k:<{max_key_length}} : {average:.2%}")

            all_q_scores[k].append(average)
            all_lang_scores[k].append(average)
        '''
        averages = []
        for k, v in all_scores.items():
            average = sum(v) / len(v)
            averages.append((k, average))
            all_q_scores[k].append(average)
            all_lang_scores[k].append(average)


            if any(x == 1.0 for x in v):
                binary_scores[k]["total"] += 1
                binary_scores[k][LANG] += 1
            else:
                binary_scores[k]["total"] += 0
                binary_scores[k][LANG] += 0


            average = sum(v) / len(v)
            if average == 1.0:
                binary_scores_all_trials[k]["total"] += 1
                binary_scores_all_trials[k][LANG] += 1
            else:
                binary_scores_all_trials[k]["total"] += 0
                binary_scores_all_trials[k][LANG] += 0


        averages.sort(key=lambda x: x[1], reverse=True)

        for k, average in averages:
            print(f"{k:<{max_key_length}} : {average:.2%}") 




    print("==================================================")
    print(f"=============== Results for {LANG} ===============")
    max_key_length = max(len(str(k)) for k in all_scores.keys())

    averages = []
    for k, v in all_q_scores.items():
        average = sum(v) / len(v)
        averages.append((k, average))

    averages.sort(key=lambda x: x[1], reverse=True)

    for k, average in averages:
        print(f"{k:<{max_key_length}} : {average:.2%}") 

    print("------------------------------")
    all_model_avg = sum([v for (k,v) in averages]) / len(averages)
    print(f"total : {all_model_avg:.2%}") 


            
print("==================================================")
print(f"=============== Total Results ===============")
max_key_length = max(len(str(k)) for k in all_scores.keys())

averages = []
for k, v in all_lang_scores.items():
    average = sum(v) / len(v)
    averages.append((k, average))

averages.sort(key=lambda x: x[1], reverse=True)

for k, average in averages:
    print(f"{k:<{max_key_length}} : {average:.2%}") 

print("------------------------------")
all_model_avg = sum([v for (k,v) in averages]) / len(averages)
print(f"total : {all_model_avg:.2%}") 


print()
print("--------------------------------------------------------------")
print("-----------------------Binary Correctness---------------------")
print("--Number of Questions Completely Correct in at least 1 Trial--")
print("--------------------------------------------------------------")


b_scores = []
for k, v in binary_scores.items():
    b_scores.append((k, v["total"]))

b_scores.sort(key=lambda x: (x[1], sum(all_lang_scores[x[0]])/len(all_lang_scores[x[0]])), reverse=True)

for k, v in b_scores:
    print(f"{k:<{max_key_length}} : Total Correct: {v}") 

print("--------------------------------------------------------------")
print("-----Number of Questions Completely Correct in All Trials-----")
print("--------------------------------------------------------------")

b_scores = []
for k, v in binary_scores_all_trials.items():
    b_scores.append((k, v["total"]))

b_scores.sort(key=lambda x: (x[1], sum(all_lang_scores[x[0]])/len(all_lang_scores[x[0]])), reverse=True)

for k, v in b_scores:
    print(f"{k:<{max_key_length}} : Total Correct: {v}") 



#for k, v in all_lang_scores.items():
#    print(f"{k:<{max_key_length}}", [f"{avg:.2%}" for avg in v])


print()
print("--------------------------------------------------------------")
print("-------------------Performance By Question Type----------------")
print("--------------------------------------------------------------")

question_categories = {
    "Java 1": "Project Behavior", "Java 2": "Library Behavior", "Java 3": "Value", 
    "Java 4": "Value", "Java 5": "Project Behavior",
    "Py 1": "Library Behavior", "Py 2": "Project Behavior", "Py 3": "Library Behavior", 
    "Py 4": "Library Behavior", "Py 5": "Value",
    "C++ 1": "Performance", "C++ 2": "Value", "C++ 3": "Library Behavior", 
    "C++ 4": "Performance", "C++ 5": "Project Behavior"
}

results = []
for k, v in all_lang_scores.items():
    model = k
    category_scores = defaultdict(list)
    
    for i, q in enumerate(v):
        lang = ""
        start = 0
        if i < 5:
            lang = "Java "
            start = 0
        elif i < 10:
            lang = "Py "
            start = 5
        else:
            lang = "C++ "
            start = 10

        q_name = lang + str(i-start+1)
        if q_name in question_categories:
            category = question_categories[q_name]
            category_scores[category].append(v[i])
        else:
            print(q_name)
            sys.exit(1)
    
    for category, scores in category_scores.items():
        results.append({
            'Model': model,
            'Question Type': category,
            'Score': np.mean(scores)
        })


category_totals = defaultdict(list)
for result in results:
    category_totals[result['Question Type']].append(result['Score'])

category_averages = {category: np.mean(scores) for category, scores in category_totals.items()}
sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)

max_cat_length = max(len(cat) for cat in ["Project Behavior", "Library Behavior", "Value", "Performance"])
print("Category Averages Across All Models (Best to Worst):")
for category, avg_score in sorted_categories:
    print(f"{category:<{max_cat_length}}: {avg_score:.2%}")
