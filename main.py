from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("JobScrapper")

fake_db = {}

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    from_fake_db = fake_db.get(word)
    if from_fake_db:
      jobs = from_fake_db
    else:
      jobs = get_jobs(word) # scrapper function
      fake_db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = fake_db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv", download_name="searching_result.csv", as_attachment=True)
  except:
    return redirect("/")

app.run(host="0.0.0.0")

