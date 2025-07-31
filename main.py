from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Simple in-memory session
session = {}

# ---------------- Sample Data ----------------
booking_requests = [
    {"id": 1, "user": "anto", "hall": "Seminar Hall", "date": "2025-07-03", "time": "10:00 AM", "status": "pending"},
    {"id": 2, "user": "ravi", "hall": "Main Hall", "date": "2025-07-05", "time": "02:00 PM", "status": "approved"}
]

users = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "admin"},
    {"id": 2, "username": "anto", "password": "1234", "role": "user"}
]

def refresh_auth_users():
    return {user["username"]: user for user in users}

# ---------------- Auth Routes ----------------
@app.get("/")
def index():
    return RedirectResponse(url="/login")

@app.get("/login")
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    auth_users = refresh_auth_users()
    user = auth_users.get(username)
    if user and user["password"] == password:
        session["user"] = username
        session["role"] = user["role"]
        return RedirectResponse(url="/admin-home" if user["role"] == "admin" else "/user-home", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin-home")
def admin_home(request: Request):
    if session.get("role") != "admin":
        return RedirectResponse("/login")
    return templates.TemplateResponse("admin_home.html", {"request": request, "user": session["user"]})

@app.get("/user-home")
def user_home(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    return templates.TemplateResponse("user_home.html", {"request": request, "user": session["user"]})

# ---------------- Hall CRUD (Admin) ----------------
@app.get("/admin/halls")
def show_halls(request: Request):
    if session.get("role") != "admin":
        return RedirectResponse("/login")
    return templates.TemplateResponse("admin_halls.html", {"request": request, "requests": booking_requests})

@app.post("/admin/halls/add")
def add_booking(user: str = Form(...), hall: str = Form(...), date: str = Form(...), time: str = Form(...), status: str = Form(...)):
    new_id = max([req["id"] for req in booking_requests], default=0) + 1
    booking_requests.append({"id": new_id, "user": user, "hall": hall, "date": date, "time": time, "status": status})
    return RedirectResponse("/admin/halls", status_code=302)

@app.post("/admin/halls/update/{booking_id}")
def update_booking(booking_id: int, user: str = Form(...), hall: str = Form(...), date: str = Form(...), time: str = Form(...), status: str = Form(...)):
    for req in booking_requests:
        if req["id"] == booking_id:
            req.update({"user": user, "hall": hall, "date": date, "time": time, "status": status})
            break
    return RedirectResponse("/admin/halls", status_code=302)

@app.get("/admin/halls/delete/{booking_id}")
def delete_booking(booking_id: int):
    global booking_requests
    booking_requests = [req for req in booking_requests if req["id"] != booking_id]
    return RedirectResponse("/admin/halls", status_code=302)

# ---------------- User CRUD (Admin) ----------------
@app.get("/admin/users")
def list_users(request: Request):
    if session.get("role") != "admin":
        return RedirectResponse("/login")
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

@app.post("/admin/users/add")
def create_user(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    new_id = max([user["id"] for user in users], default=0) + 1
    users.append({"id": new_id, "username": username, "password": password, "role": role})
    return RedirectResponse("/admin/users", status_code=302)

@app.post("/admin/users/update/{user_id}")
def update_user(user_id: int, username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    for user in users:
        if user["id"] == user_id:
            user.update({"username": username, "password": password, "role": role})
            break
    return RedirectResponse("/admin/users", status_code=302)

@app.get("/admin/users/delete/{user_id}")
def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return RedirectResponse("/admin/users", status_code=302)

# ---------------- User Hall Request (CRUD) ----------------
@app.get("/user/request-booking")
def show_request_form(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    return templates.TemplateResponse("request_booking.html", {"request": request, "user": session["user"]})

@app.post("/user/request-booking")
def submit_request(user: str = Form(...), hall: str = Form(...), date: str = Form(...), time: str = Form(...)):
    new_id = max([req["id"] for req in booking_requests], default=0) + 1
    booking_requests.append({
        "id": new_id,
        "user": user,
        "hall": hall,
        "date": date,
        "time": time,
        "status": "pending"
    })
    return RedirectResponse("/user/my-bookings", status_code=302)

@app.get("/user/my-bookings")
def view_user_bookings(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    user_requests = [req for req in booking_requests if req["user"] == session["user"]]
    return templates.TemplateResponse("view_bookings.html", {"request": request, "requests": user_requests})

# ---------------- Additional User Pages ----------------
@app.get("/user/feedback")
def show_feedback_page(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    return templates.TemplateResponse("give_feedback.html", {"request": request, "user": session["user"]})

@app.get("/user/profile")
def show_profile_page(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    return templates.TemplateResponse("profile_settings.html", {"request": request, "user": session["user"]})
# ---------------- Feedback ----------------
@app.get("/user/feedback")
def show_feedback_form(request: Request):
    if session.get("role") != "user":
        return RedirectResponse("/login")
    return templates.TemplateResponse("give_feedback.html", {"request": request, "user": session["user"]})

@app.post("/user/feedback")
def submit_feedback(user: str = Form(...), message: str = Form(...)):
    feedbacks.append({"user": user, "message": message})
    return RedirectResponse("/user-home", status_code=302)
