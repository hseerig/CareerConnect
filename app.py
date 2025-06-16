from flask import Flask, render_template, request, redirect
import json
import os
from pymongo import MongoClient

app = Flask(__name__)

# Load MongoDB URI from Replit Secrets
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

# Use a specific database and collection
db = client["careerconnect"]
applications_collection = db["applications"]

# Load job listings from jobs.json
def load_jobs():
    with open("jobs.json", "r") as f:
        return json.load(f)

@app.route("/")
def home():
    jobs = load_jobs()
    return render_template("home.html", jobs=jobs)

@app.route("/job/<job_id>")
def job_detail(job_id):
    jobs = load_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)
    if job:
        return render_template("job_detail.html", job=job)
    return "Job not found", 404

@app.route("/apply/<job_id>", methods=["GET"])
def apply(job_id):
    jobs = load_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        return "Job not found", 404
    return render_template("apply_form.html", job=job)

@app.route("/submit_application", methods=["POST"])
def submit_application():
    name = request.form['name']
    email = request.form['email']
    resume_url = request.form['resume_url']
    linkedin = request.form['linkedin']
    job_id = request.form['job_id']

    application = {
        "job_id": job_id,
        "name": name,
        "email": email,
        "resume_url": resume_url,
        "linkedin": linkedin
    }

    # Save application to MongoDB
    applications_collection.insert_one(application)

    # Load job info for confirmation page
    jobs = load_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)

    return render_template("application_submitted.html", applicant=application, job=job)

@app.route("/admin")
def admin_dashboard():
    # Load all applications from MongoDB
    all_applications = list(applications_collection.find())
    return render_template("admin.html", applications=all_applications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
