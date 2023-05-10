import json
with open("filtered_generated.txt", "r") as fp:
    tasks = fp.readlines()

with open("dedup_generated_tasks.json", "w") as fp:
    json.dump(list(set(tasks)), fp, indent=4)