import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["공고", "회사명", "지역", "링크"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return