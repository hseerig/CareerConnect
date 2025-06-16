from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# Load job listings from jobs.json
def load_jobs():
    with open("jobs.json", "r") as f:
        return json.load(f)

# Load all submitted applications
def load_applications():
    if not os.path.exists("applications.json"):
        return []
    with open("applications.json", "r") as f:
        return json.load(f)

# Save a new application
def save_application(application):
    applications = load_applications()
    applications.append(application)
    with open("applications.json", "w") as f:
        json.dump(applications, f, indent=2)

@app.route("/")
def home():
    jobs = load_jobs()
    return render_template("home.html", jobs=jobs)

@app.route("/job/<job_id>")
def job_detail(job_id):
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id:
            return render_template("job_detail.html", job=job)
    return "Job not found", 404

@app.route("/apply/<job_id>", methods=["GET", "POST"])
def apply(job_id):
    jobs = load_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        return "Job not found", 404

    if request.method == "POST":
        application = {
            "job_id": job_id,
            "name": request.form["name"],
            "email": request.form["email"],
            "linkedin": request.form["linkedin"],
            "resume": request.form["resume"]
        }
        save_application(application)
        return render_template("application_submitted.html", applicant=application, job=job)

    return render_template("apply_form.html", job=job)

@app.route("/admin")
def admin_dashboard():
    applications = load_applications()
    return render_template("admin.html", applications=applications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
