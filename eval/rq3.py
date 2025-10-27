from collections import defaultdict
import os
import json
import csv

def get_total_lies(rubric, r_deducted):
    if r_deducted.isspace():
        return 0

    total_lies = 0

    for r_item in r_deducted.split(","):
        if not r_item.strip():
            continue

        r_number = int(r_item[0]) - 1  # rubric index
        sub_item = ord(r_item[1]) - ord('a')  # subitem index

        sub = rubric[r_number]["subitems"][sub_item]
        pts = sub["points"]

        if sub.get("lie", True):
            total_lies += 1


    return total_lies 



PREFIX = "../"

lie_counts = defaultdict(lambda: 0)
lies_per_trial = defaultdict(lambda: 0)
questions_with_lies = defaultdict(lambda: 0)

for LANG in ["java", "py", "cpp"]:
    for SAMPLE_NUM in range(1, 6):
        f_csv = f"{LANG}{SAMPLE_NUM}.csv"
        f_results = PREFIX + f"results/rubric-applications/{f_csv}"
        f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

        if not os.path.exists(f_results):
            continue

        rubric = json.load(open(f_rubrics))

        with open(f_results) as f:
            reader = csv.reader(f)
            next(reader)

            i = 1
            any_lies = False
            for row in reader:
                model = row[0]
                trial_num = row[1]
                r_deducted = row[2]

                total_lies = get_total_lies(rubric, r_deducted)
                lie_counts[model] += total_lies
                if total_lies:
                    lies_per_trial[model] += 1
                    any_lies = True

                #count lie in 1 of the 3 trials
                if i % 3 == 0 and any_lies:
                    questions_with_lies[model] += 1
                    any_lies = False

                i += 1
                

#print(lie_counts)
#print(lies_per_trial)

sorted_lies = sorted(questions_with_lies.items(), key=lambda item: item[1], reverse=True)


print("\nHallucination Analysis:")
print("-" * 70)
print(f"{'Model':<30} | {'Lies/Question':>12} | {'Total Lies':>12}")
print("-" * 70)

# Print sorted results
for model, lies in sorted_lies:
    print(f"{model:<30} | {lies:>12.2f} | {lie_counts[model]:>12}")
print("-" * 70)

print("\nSummary Statistics:")
t = [v for k, v in lies_per_trial.items()]
print(f"  Average lies across all trials:    {sum(t) / len(t):.2f}")

t = [v for k, v in questions_with_lies.items()]
print(f"  Average lies across 15 questions:  {sum(t) / len(t):.2f}")

