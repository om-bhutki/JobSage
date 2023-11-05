#contains the API functions that the API will invoke.
import jwt
from .models import Job, User
from app import create_app, db
from flask import jsonify, redirect, request, abort, render_template, url_for
import requests
from functools import wraps
#from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = create_app()

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def index1():
    
    return render_template("index1.html")



def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)

        if not token:
           return redirect(url_for('error_page', message='Token is missing'))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('error_page', message='Token has expired'))
        except jwt.InvalidTokenError:
            return redirect(url_for('error_page', message='Invalid token'))

        return func(*args, **kwargs)

    return decorated


# Render the register page
@app.route('/register_page')
def register_page():
    return render_template('register.html')

# Handle registration form submission
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
       return redirect(url_for('error_page', message='User already exists, Try another username'))
        #return redirect(url_for('login_page'))
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_page'))

# Render the login page
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# Handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    #print(username)

    if user and user.password == password:
       # print(username)
        u1=username
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        print(u1)
        return redirect(url_for('index1',token=token))
    else:
        return redirect(url_for('error_page', message='Invalid credentials'))
    
@app.route('/error_page')
def error_page():
    message = request.args.get('message', 'An error occurred.')
    return render_template('error_page.html', message=message)


@app.route('/welcome_page1')
def welcome_page1():
    token = request.args.get('token', '')
    if not token:
        return redirect(url_for('error_page', message='Please login '))
    
    return render_template('welcome1.html', token=token)

@app.route('/logout')
def logout():
    token = None
    return redirect(url_for('index'))

@app.route("/joblist")
def joblist():
    jobs = Job.query.all()
    return render_template("joblist.html", jobs=jobs)

@app.route("/find")
def find_a_job():

    import requests
    import random

    url = "https://jsearch.p.rapidapi.com/search"

    titles = ["Python developer","Data Scientist","Software Engineer","Fullstack Developer"]
    cities = ["Mumbai","Pune","Bangalore","Hyderabad","Noida"]

    querystring = {"query":f"{random.choice(titles)} in {random.choice(cities)}, India","page":"1","num_pages":"1"}

    headers = {
	    "X-RapidAPI-Key": "2eaba7b4a2mshe3ac5c2a68074c7p1ea566jsn959368265014",
	    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    jobs = response.json()
    return render_template("find-a-job.html",jobs=jobs['data'])


@app.route("/displayjobs")
def displayjobs():
    jobs = Job.query.all()
    return render_template("displayjobs.html", jobs=jobs)

@app.route("/job/list", methods = ["GET"])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([job.to_json() for job in jobs])

@app.route("/job/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job= Job.query.get(job_id)
    if job is None:
       abort(400,'Job not found')
    return render_template("job.html", job_id = job_id)

@app.route("/delete_job/<int:job_id>", methods = ["POST"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('displayjobs'))

@app.route('/add_job', methods=['POST'])
def add_job():
    if not request.form:
        abort(400)
    job = Job(
        job_id=request.form.get('job_id'),
        job_Title=request.form.get('job_Title'),
        comp_name=request.form.get('comp_name'),
        Job_desc=request.form.get('Job_desc'),
        salary=request.form.get('salary'),
        city=request.form.get('city'),  
        address=request.form.get('address'),  
        linkedin_company_url=request.form.get('linkedin_company_url')
    )
    db.session.add(job)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/post_job', methods=['GET'])
def render_post_job_form():
    return render_template('post_job.html', success=False)

@app.route('/find_job', methods=['GET'])
def find_job_form():
    
    return render_template('find_job_form.html', jobs=None)

# Handle the job posting form submission
@app.route('/post_job_process', methods=['POST'])
def post_job_process():
    if request.method == 'POST':
        # Get form data and create a new job record in the database
        job = Job(
            job_Title=request.form.get('job_Title'),
            comp_name=request.form.get('comp_name'),
            Job_desc=request.form.get('Job_desc'),
            salary=request.form.get('salary'),
            city=request.form.get('city'),
            address=request.form.get('address'),
            linkedin_company_url=request.form.get('linkedin_company_url')
        )
        db.session.add(job)
        db.session.commit()
        # Redirect to the form with a success flag
        return render_template('post_job.html', success=True)
    # Handle other HTTP methods
    return redirect(url_for('render_post_job_form'))

# Route to process search form data and display search results
@app.route('/find_job_results', methods=['POST'])
def find_job_results():
    # Get the search criteria from the form
    job_Title = request.form.get('job_Title')
    comp_name = request.form.get('comp_name')
    #salary = request.form.get('salary')
    city = request.form.get('city')

    # Query the database to find jobs that match the criteria
    jobs = Job.query.filter_by(
        job_Title=job_Title,
        comp_name=comp_name,
        city=city
    ).all()

    return render_template('find_job_form.html', jobs=jobs)


@app.route('/create_job', methods=['POST'])
def create_job():
    if not request.json:
        abort(400)
    job = Job(
        job_id=request.json.get('job_id'),
        job_Title=request.json.get('job_Title'),
        comp_name=request.json.get('comp_name'),
        Job_desc=request.json.get('Job_desc'),
        salary=request.json.get('salary')
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_json()), 201

@app.route('/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    job.job_Title = request.form.get('job_Title', job.job_Title)
    job.comp_name = request.form.get('comp_name', job.comp_name)
    job.Job_desc = request.form.get('Job_desc', job.Job_desc)
    job.salary = request.form.get('salary', job.salary)
    job.city=request.form.get('city', job.city)  
    job.address=request.form.get('address', job.address)
    job.linkedin_company_url=request.form.get('linkedin_company_url', job.linkedin_company_url)
    db.session.commit()
    return redirect(url_for('displayjobs'))
    #return jsonify(job.to_json())


@app.route('/latest_jobs')
def latest_joblist():
   url = "https://linkedin-jobs-search.p.rapidapi.com/"

   payload = {
        "search_terms": "Web Developer",
        "location": "Pune, IN",
        "page": "1"
    }
   headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4110b8035fmsh91b96aa1f14068fp135075jsnbf4d5b9360fa",
        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
    }

   response = requests.post(url, json=payload, headers=headers)
   jobs_data = response.json()
   print(jobs_data)
   return render_template('index2.html', jobs_data=jobs_data)

@app.route("/others_job")
def others_job():

 return render_template("om.html")

@app.route("/compare", methods=["GET","POST"])
def compare():
    
    from bs4 import BeautifulSoup

    if request.method == "POST":
    
        company_1 = request.form['company1'].lower()
        company_2 = request.form['company2'].lower()
        
        headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language":"en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        response = requests.get(f"https://www.ambitionbox.com/compare/{company_1}-vs-{company_2}",headers=headers)

        ambition_webpage = response.text
        soup = BeautifulSoup(ambition_webpage,'lxml')

        mytds = soup.find_all("td", {"class": "row__content"})
        myths = soup.find_all("th",{"class": "row__title"})
        infos = []
        for div in mytds:
            infos.append(div.text.replace("\n\t","").replace("\t","").strip())
        heads = []
        for head in myths:
            heads.append(head.text)
        heads = list(filter(None,heads))

        company2 = infos[1::2]
        company1 = infos[::2]

        return render_template("compare.html",man="man",company1=company1,company2=company2,company_1=company_1.upper(),company_2=company_2.upper(),heads=heads,infos=infos)

    return render_template("compare.html")

RAPIDAPI_KEY = "cd8ab388b9mshae264f8b24d4c13p1d991ejsn9d8db93fec8b"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
RAPIDAPI_URL = "https://jsearch.p.rapidapi.com/search"

@app.route("/searchjob")
def searchjob():
    return render_template("index.html", "index1.html")

@app.route("/search_jobs", methods=["POST"])
def search_jobs():
    query = request.form.get("query")

    querystring = {"query": query, "page": "1", "num_pages": "1"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(RAPIDAPI_URL, headers=headers, params=querystring)

    if response.status_code == 200:
        jobs = response.json()
        print(jobs)
        return render_template("job_results.html", jobs=jobs.get("data", []))
    else:
        return "Error fetching job data"





