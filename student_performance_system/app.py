import os
import json
from datetime import datetime, date, timedelta
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, desc

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


# ---------------------------------------------------------
# DATABASE MODELS
# ---------------------------------------------------------

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # 'student' or 'admin'
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=True)
    language_pref = db.Column(db.String(10), nullable=False, default="en")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    academic_records = db.relationship("AcademicRecord", backref="student", cascade="all, delete-orphan", lazy=True)
    predictions = db.relationship("Prediction", backref="student", cascade="all, delete-orphan", lazy=True)
    study_plans = db.relationship("StudyPlan", backref="student", cascade="all, delete-orphan", lazy=True)
    exam_schedules = db.relationship("ExamSchedule", backref="student", cascade="all, delete-orphan", lazy=True)


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class AcademicRecord(db.Model):
    __tablename__ = "academic_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    attendance = db.Column(db.Float, nullable=False, default=80.0)  # Kept in academic record for analysis
    internal_marks = db.Column(db.Float, nullable=False)
    assignment_marks = db.Column(db.Float, nullable=False)
    previous_marks = db.Column(db.Float, nullable=False)
    study_hours = db.Column(db.Float, nullable=False, default=2.0)

    subject = db.relationship("Subject", backref="academic_records", lazy=True)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    predicted_marks = db.Column(db.Float, nullable=False)
    performance_category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject", backref="predictions", lazy=True)


class StudyPlan(db.Model):
    __tablename__ = "study_plans"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False, default="Personalized Academic Improvement Plan")
    daily_study_hours = db.Column(db.Float, nullable=False, default=3.0)
    preferred_timing = db.Column(db.String(50), nullable=False, default="Evening")  # Morning, Afternoon, Evening, Night
    start_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=False)    # YYYY-MM-DD
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="active")  # active, completed, archived
    ai_summary = db.Column(db.Text, nullable=True)

    tasks = db.relationship("StudyTask", backref="plan", cascade="all, delete-orphan", lazy=True, order_by="StudyTask.scheduled_date, StudyTask.start_time")


class StudyTask(db.Model):
    __tablename__ = "study_tasks"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("study_plans.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    subject_name = db.Column(db.String(100), nullable=False)
    task_title = db.Column(db.String(200), nullable=False)
    topic_name = db.Column(db.String(150), nullable=True)
    scheduled_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    start_time = db.Column(db.String(20), nullable=True)       # e.g. "18:00"
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    priority = db.Column(db.String(20), nullable=False, default="Medium")  # High, Medium, Low
    task_type = db.Column(db.String(30), nullable=False, default="study")  # study, revision, practice_test, personal
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)


class StudyProgress(db.Model):
    __tablename__ = "study_progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    completed_minutes = db.Column(db.Integer, nullable=False, default=0)
    target_minutes = db.Column(db.Integer, nullable=False, default=0)
    completed_tasks_count = db.Column(db.Integer, nullable=False, default=0)
    total_tasks_count = db.Column(db.Integer, nullable=False, default=0)


class ExamSchedule(db.Model):
    __tablename__ = "exam_schedules"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    subject_name = db.Column(db.String(100), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)  # e.g. "Final Semester Exam"
    exam_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    syllabus_coverage = db.Column(db.String(100), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def role_required(role):
    def decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("dashboard"))
            return function(*args, **kwargs)
        return wrapped
    return decorator


# ---------------------------------------------------------
# PREDICTION MODEL (ATTENDANCE EXCLUDED)
# ---------------------------------------------------------

PREDICTION_MODEL_DATA = None


def load_prediction_model():
    global PREDICTION_MODEL_DATA
    if PREDICTION_MODEL_DATA is not None:
        return PREDICTION_MODEL_DATA

    base_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "models", "performance_model.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                PREDICTION_MODEL_DATA = json.load(f)
                return PREDICTION_MODEL_DATA
        except Exception as e:
            print("Error loading json model:", e)

    # Fallback weights if json is not yet created
    PREDICTION_MODEL_DATA = {
        "model_name": "Multi-Variable Linear Regression (Attendance Excluded)",
        "features": ["internal_marks", "assignment_marks", "previous_marks", "study_hours"],
        "intercept": 1.0,
        "weights": {
            "internal_marks": 0.3148,
            "assignment_marks": 0.2161,
            "previous_marks": 0.3545,
            "study_hours": 1.9625,
        },
        "metrics": {"MAE": 2.64, "RMSE": 3.40, "R2": 0.9335},
    }
    return PREDICTION_MODEL_DATA


def predict_final_marks(internal_marks, assignment_marks, previous_marks, study_hours):
    """
    Predict expected final examination marks without using attendance as an input feature.
    """
    model_data = load_prediction_model()
    intercept = model_data.get("intercept", 1.0)
    weights = model_data.get("weights", {})

    pred = (
        intercept
        + weights.get("internal_marks", 0.31) * float(internal_marks)
        + weights.get("assignment_marks", 0.21) * float(assignment_marks)
        + weights.get("previous_marks", 0.35) * float(previous_marks)
        + weights.get("study_hours", 1.96) * float(study_hours)
    )
    predicted_score = max(0.0, min(100.0, round(pred, 1)))

    if predicted_score >= 85:
        category = "Outstanding (Grade A+)"
    elif predicted_score >= 70:
        category = "Good (Grade A)"
    elif predicted_score >= 55:
        category = "Average (Grade B)"
    elif predicted_score >= 40:
        category = "Needs Improvement (Grade C)"
    else:
        category = "Academic Risk (Grade F)"

    return predicted_score, category


# ---------------------------------------------------------
# AI STUDY PLAN GENERATION ENGINE
# ---------------------------------------------------------

SUBJECT_TOPICS = {
    "Mathematics": [
        "Differential Calculus & Applications",
        "Linear Algebra & Matrix Operations",
        "Probability Distributions & Bayes Theorem",
        "Numerical Integration & Interpolation",
        "Multiple Integrals & Vector Calculus",
        "Fourier Series & Boundary Problems",
    ],
    "Java Programming": [
        "Object-Oriented Programming & Inheritance",
        "Collections Framework (List, Map, Set)",
        "Exception Handling & Custom Exceptions",
        "Multithreading & Concurrency",
        "File I/O Streams & Serialization",
        "JDBC & Database Connectivity",
    ],
    "Database Management Systems": [
        "Relational Algebra & Normalization (1NF, 2NF, 3NF, BCNF)",
        "Complex SQL Queries, Subqueries & Joins",
        "Transactions, ACID Properties & Concurrency Control",
        "ER Modeling & Schema Mapping",
        "Indexing, B-Trees & Query Optimization",
        "NoSQL Basics & MongoDB",
    ],
    "Data Structures & Algorithms": [
        "Binary Trees, BST & AVL Trees",
        "Graph Traversal (BFS & DFS) & Shortest Path",
        "Sorting Algorithms & Time Complexity",
        "Stacks, Queues & Priority Queues",
        "Dynamic Programming & Greedy Algorithms",
        "Hashing & Collision Resolution",
    ],
    "Operating Systems": [
        "CPU Scheduling Algorithms (FCFS, SJF, RR)",
        "Memory Management & Virtual Memory Paging",
        "Process Synchronization, Semaphores & Mutex",
        "Deadlock Prevention & Banker's Algorithm",
        "File System Architecture & Directory Implementation",
        "Disk Scheduling Algorithms (SCAN, C-SCAN)",
    ],
    "Computer Networks": [
        "OSI 7-Layer & TCP/IP Protocol Suite",
        "IP Addressing, Subnetting & CIDR",
        "Routing Protocols (OSPF, BGP, Distance Vector)",
        "TCP vs UDP, Flow Control & Congestion Control",
        "DNS, HTTP, HTTPS & Application Layer Protocols",
        "Network Security, Firewalls & Cryptography",
    ],
}

DEFAULT_TOPICS = [
    "Core Concept Foundations & Theory",
    "Application Examples & Numerical Problems",
    "Advanced Topics & Key Definitions",
    "Summary Notes & Formula Sheet Revision",
    "Previous Years Exam Questions Practice",
    "Mock Test Assessment & Gap Analysis",
]


def generate_ai_study_plan(student, daily_study_hours=3.0, preferred_timing="Evening", plan_days=7):
    """
    Intelligently generates a personalized daily & weekly study timetable
    based on student's actual performance, weak subjects, and upcoming exams.
    """
    records = AcademicRecord.query.filter_by(student_id=student.id).all()
    exams = ExamSchedule.query.filter_by(student_id=student.id).all()

    today = date.today()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=plan_days - 1)).strftime("%Y-%m-%d")

    # Deactivate or archive previous active plans for this student
    previous_plans = StudyPlan.query.filter_by(student_id=student.id, status="active").all()
    for p in previous_plans:
        p.status = "archived"

    # Analyze performance per subject
    subject_stats = []
    if records:
        for r in records:
            sub_name = r.subject.name if r.subject else "General Studies"
            # Calculate composite academic score (Internal 35%, Previous 35%, Assignment 30%)
            composite_score = (0.35 * r.internal_marks) + (0.35 * r.previous_marks) + (0.30 * r.assignment_marks)
            
            # Check exam proximity
            days_to_exam = 999
            matched_exam = None
            for ex in exams:
                if ex.subject_name.lower() == sub_name.lower() or (r.subject_id and ex.subject_id == r.subject_id):
                    try:
                        ex_date = datetime.strptime(ex.exam_date, "%Y-%m-%d").date()
                        delta = (ex_date - today).days
                        if 0 <= delta < days_to_exam:
                            days_to_exam = delta
                            matched_exam = ex
                    except Exception:
                        pass

            # Urgency & Priority calculation:
            # Low scores (<60) or upcoming exams within 7 days increase priority
            is_weak = composite_score < 60
            is_urgent_exam = days_to_exam <= 7

            if is_urgent_exam or composite_score < 55:
                priority = "High"
                weight = 3.0
            elif composite_score < 72 or days_to_exam <= 14:
                priority = "Medium"
                weight = 2.0
            else:
                priority = "Low"
                weight = 1.0

            subject_stats.append({
                "subject_id": r.subject_id,
                "subject_name": sub_name,
                "composite_score": round(composite_score, 1),
                "is_weak": is_weak,
                "days_to_exam": days_to_exam,
                "exam": matched_exam,
                "priority": priority,
                "weight": weight,
            })
    else:
        # Fallback if no records exist yet
        subject_stats = [
            {"subject_id": None, "subject_name": "Mathematics", "composite_score": 52.0, "is_weak": True, "days_to_exam": 10, "exam": None, "priority": "High", "weight": 3.0},
            {"subject_id": None, "subject_name": "Java Programming", "composite_score": 84.0, "is_weak": False, "days_to_exam": 16, "exam": None, "priority": "Low", "weight": 1.0},
            {"subject_id": None, "subject_name": "Database Management Systems", "composite_score": 60.0, "is_weak": False, "days_to_exam": 5, "exam": None, "priority": "High", "weight": 3.0},
        ]

    # Calculate proportional time allocation
    total_weight = sum(s["weight"] for s in subject_stats) or 1.0
    for s in subject_stats:
        s["allocated_fraction"] = s["weight"] / total_weight

    # Preferred timing base hour
    timing_hours = {
        "Morning": ["06:30", "07:30", "08:30"],
        "Afternoon": ["14:00", "15:00", "16:00"],
        "Evening": ["18:00", "19:00", "20:00"],
        "Night": ["21:00", "22:00", "23:00"],
    }
    base_slots = timing_hours.get(preferred_timing, timing_hours["Evening"])

    # Create new StudyPlan
    weak_sub_names = [s["subject_name"] for s in subject_stats if s["is_weak"]]
    weak_str = ", ".join(weak_sub_names) if weak_sub_names else "all core subjects"

    summary_text = (
        f"AI personalized schedule generated for {student.name}. "
        f"Focusing extra study hours on {weak_str} while reserving regular revision for strong subjects. "
        f"Optimized for {daily_study_hours} daily study hours during {preferred_timing} hours."
    )

    study_plan = StudyPlan(
        student_id=student.id,
        title=f"AI Study Plan ({plan_days} Days) - Focus on {weak_str}",
        daily_study_hours=daily_study_hours,
        preferred_timing=preferred_timing,
        start_date=start_date,
        end_date=end_date,
        status="active",
        ai_summary=summary_text,
    )
    db.session.add(study_plan)
    db.session.flush()

    # Generate daily tasks across the plan duration
    num_slots_per_day = max(1, int(round(daily_study_hours)))
    session_duration = int(round((daily_study_hours * 60) / num_slots_per_day))

    # Round-robin selection weighted by priority
    weighted_subjects_pool = []
    for s in subject_stats:
        multiplier = 3 if s["priority"] == "High" else (2 if s["priority"] == "Medium" else 1)
        weighted_subjects_pool.extend([s] * multiplier)

    pool_index = 0
    topic_pointers = {s["subject_name"]: 0 for s in subject_stats}

    for day_offset in range(plan_days):
        current_day = today + timedelta(days=day_offset)
        day_str = current_day.strftime("%Y-%m-%d")

        for slot_idx in range(num_slots_per_day):
            subj_info = weighted_subjects_pool[pool_index % len(weighted_subjects_pool)]
            pool_index += 1

            sub_name = subj_info["subject_name"]
            topics_list = SUBJECT_TOPICS.get(sub_name, DEFAULT_TOPICS)
            t_idx = topic_pointers[sub_name] % len(topics_list)
            topic = topics_list[t_idx]
            topic_pointers[sub_name] += 1

            # Determine task type
            days_to_exam = subj_info["days_to_exam"] - day_offset
            if 0 <= days_to_exam <= 2:
                task_type = "practice_test"
                task_title = f"{sub_name}: Mock Exam & High-Yield Questions"
            elif 3 <= days_to_exam <= 5:
                task_type = "revision"
                task_title = f"{sub_name}: Intensive Exam Revision ({topic})"
            elif subj_info["is_weak"]:
                task_type = "study"
                task_title = f"{sub_name}: Deep Study & Problem Practice ({topic})"
            else:
                task_type = "revision" if slot_idx % 2 == 1 else "study"
                task_title = f"{sub_name}: Concept Study ({topic})"

            start_time = base_slots[slot_idx % len(base_slots)]

            task = StudyTask(
                plan_id=study_plan.id,
                student_id=student.id,
                subject_id=subj_info["subject_id"],
                subject_name=sub_name,
                task_title=task_title,
                topic_name=topic,
                scheduled_date=day_str,
                start_time=start_time,
                duration_minutes=session_duration,
                priority=subj_info["priority"],
                task_type=task_type,
                is_completed=False,
                notes=f"Target: Complete {topic} thoroughly. Focus on core formulas and practice exercises.",
            )
            db.session.add(task)

    db.session.commit()
    return study_plan


def get_intelligent_recommendations(student):
    """
    Generate dynamic, data-driven recommendations based on the student's actual performance,
    identified weaknesses, upcoming exam countdowns, and study progress.
    """
    records = AcademicRecord.query.filter_by(student_id=student.id).all()
    exams = ExamSchedule.query.filter_by(student_id=student.id).all()
    active_plan = StudyPlan.query.filter_by(student_id=student.id, status="active").first()

    recommendations = []
    today = date.today()

    # 1. Performance-based recommendations
    if records:
        weakest = min(records, key=lambda r: (r.internal_marks + r.previous_marks + r.assignment_marks) / 3)
        strongest = max(records, key=lambda r: (r.internal_marks + r.previous_marks + r.assignment_marks) / 3)

        weak_avg = (weakest.internal_marks + weakest.previous_marks + weakest.assignment_marks) / 3
        strong_avg = (strongest.internal_marks + strongest.previous_marks + strongest.assignment_marks) / 3

        if weakest.subject and strongest.subject and weakest.id != strongest.id:
            recommendations.append({
                "type": "performance",
                "badge": "Subject Optimization",
                "color": "primary",
                "text": f"Your internal score in {weakest.subject.name} is currently {weak_avg:.1f}%, while {strongest.subject.name} is {strong_avg:.1f}%. Allocate extra dedicated practice to {weakest.subject.name} and maintain regular revision in {strongest.subject.name}."
            })

    # 2. Upcoming Examination Urgency
    if exams:
        for ex in exams:
            try:
                ex_date = datetime.strptime(ex.exam_date, "%Y-%m-%d").date()
                delta = (ex_date - today).days
                if 0 <= delta <= 7:
                    recommendations.append({
                        "type": "exam",
                        "badge": "Urgent Exam Prep",
                        "color": "danger",
                        "text": f"Upcoming examination: {ex.exam_name} for {ex.subject_name} is in {delta} days! Prioritize revision and schedule practice mock tests immediately."
                    })
                elif 8 <= delta <= 14:
                    recommendations.append({
                        "type": "exam",
                        "badge": "Exam Approaching",
                        "color": "warning",
                        "text": f"{ex.subject_name} examination is scheduled in {delta} days ({ex.exam_date}). Begin chapter summaries and formula reviews."
                    })
            except Exception:
                pass

    # 3. Task Progress & Consistency
    if active_plan:
        all_tasks = StudyTask.query.filter_by(plan_id=active_plan.id).all()
        completed_tasks = [t for t in all_tasks if t.is_completed]
        today_str = today.strftime("%Y-%m-%d")
        today_pending = [t for t in all_tasks if t.scheduled_date == today_str and not t.is_completed]

        if today_pending:
            recommendations.append({
                "type": "progress",
                "badge": "Today's Agenda",
                "color": "info",
                "text": f"You have {len(today_pending)} study task(s) scheduled for today. Complete them during your preferred {active_plan.preferred_timing} timing to stay on track."
            })
        elif completed_tasks and len(completed_tasks) == len(all_tasks):
            recommendations.append({
                "type": "progress",
                "badge": "Goal Achieved",
                "color": "success",
                "text": "Excellent discipline! You have completed all scheduled tasks in your current study plan. You can now generate your next study sprint."
            })

    # Fallback generic recommendation if empty
    if not recommendations:
        recommendations.append({
            "type": "general",
            "badge": "Smart Study Tip",
            "color": "primary",
            "text": "Consistency is key to higher grades. Study in focused 45-50 minute intervals followed by 10-minute active recall breaks."
        })

    return recommendations


def get_student_reminders(student):
    """
    Collect notifications & reminders:
    - Upcoming study sessions
    - Pending study tasks
    - Upcoming examinations
    - Weekly study goal progress
    """
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    reminders = []

    # 1. Exams countdown
    exams = ExamSchedule.query.filter_by(student_id=student.id).all()
    for ex in exams:
        try:
            ex_date = datetime.strptime(ex.exam_date, "%Y-%m-%d").date()
            delta = (ex_date - today).days
            if 0 <= delta <= 14:
                reminders.append({
                    "icon": "bi-exclamation-diamond-fill",
                    "color": "danger" if delta <= 5 else "warning",
                    "title": f"Exam Countdown: {ex.subject_name}",
                    "message": f"{ex.exam_name} in {delta} days ({ex.exam_date}).",
                })
        except Exception:
            pass

    # 2. Pending tasks for today
    today_tasks = StudyTask.query.filter_by(student_id=student.id, scheduled_date=today_str).all()
    pending_today = [t for t in today_tasks if not t.is_completed]
    if pending_today:
        reminders.append({
            "icon": "bi-clock-history",
            "color": "primary",
            "title": f"{len(pending_today)} Pending Tasks Today",
            "message": f"Next task: {pending_today[0].task_title} at {pending_today[0].start_time or 'Scheduled time'}.",
        })

    # 3. Overdue tasks from previous days
    overdue_tasks = StudyTask.query.filter(
        StudyTask.student_id == student.id,
        StudyTask.scheduled_date < today_str,
        StudyTask.is_completed == False,
    ).all()
    if overdue_tasks:
        reminders.append({
            "icon": "bi-arrow-repeat",
            "color": "secondary",
            "title": f"{len(overdue_tasks)} Incomplete Tasks Need Rescheduling",
            "message": "Click the Reschedule button on incomplete tasks to adapt your calendar.",
        })

    return reminders


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        usn = request.form.get("usn", "").strip().upper()
        branch = request.form.get("branch", "Computer Science").strip()
        semester = int(request.form.get("semester", 5))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("register"))

        # Find or create Student record
        student = Student.query.filter(or_(Student.email == email, Student.usn == usn)).first()
        if not student:
            if not usn:
                usn = f"1RV21CS{User.query.count() + 100:03d}"
            student = Student(
                name=name,
                email=email,
                usn=usn,
                branch=branch,
                semester=semester,
            )
            db.session.add(student)
            db.session.flush()

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role="student",
            student_id=student.id,
        )
        db.session.add(user)
        db.session.commit()

        # Seed initial academic records and AI study plan for new student
        seed_student_academic_records(student)
        generate_ai_study_plan(student, daily_study_hours=3.0, preferred_timing="Evening", plan_days=7)

        flash("Registration successful. Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Ensure student has a linked Student profile
            if user.role == "student" and not user.student_id:
                student = Student.query.filter_by(email=user.email).first()
                if not student:
                    usn = f"1RV21CS{user.id + 100:03d}"
                    student = Student(name=user.name, email=user.email, usn=usn, branch="Computer Science", semester=5)
                    db.session.add(student)
                    db.session.flush()
                    seed_student_academic_records(student)
                user.student_id = student.id
                db.session.commit()

            flash("Signed in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        students = Student.query.order_by(Student.id.desc()).all()
        records = AcademicRecord.query.all()
        avg_attendance = round(sum(r.attendance for r in records) / len(records), 1) if records else 82.5
        avg_internals = round(sum(r.internal_marks for r in records) / len(records), 1) if records else 68.0
        
        # Students needing support (low composite score or predicted score < 60)
        at_risk_count = 0
        for s in students:
            s_records = AcademicRecord.query.filter_by(student_id=s.id).all()
            if s_records:
                avg_score = sum((r.internal_marks + r.previous_marks) / 2 for r in s_records) / len(s_records)
                if avg_score < 60:
                    at_risk_count += 1

        return render_template(
            "admin_dashboard.html",
            students=students,
            avg_attendance=avg_attendance,
            avg_internals=avg_internals,
            at_risk_count=at_risk_count,
        )

    # Student Dashboard
    student = db.session.get(Student, current_user.student_id) if current_user.student_id else None
    if not student:
        student = Student.query.filter_by(email=current_user.email).first()
        if student:
            current_user.student_id = student.id
            db.session.commit()

    if not student:
        usn = f"1RV21CS{current_user.id + 100:03d}"
        student = Student(name=current_user.name, email=current_user.email, usn=usn, branch="Computer Science", semester=5)
        db.session.add(student)
        db.session.flush()
        current_user.student_id = student.id
        db.session.commit()
        seed_student_academic_records(student)

    records = AcademicRecord.query.filter_by(student_id=student.id).all()
    predictions = Prediction.query.filter_by(student_id=student.id).order_by(Prediction.id.desc()).all()
    latest_prediction = predictions[0] if predictions else None

    # Study planner summary for dashboard
    active_plan = StudyPlan.query.filter_by(student_id=student.id, status="active").first()
    if not active_plan:
        active_plan = generate_ai_study_plan(student)

    tasks = StudyTask.query.filter_by(plan_id=active_plan.id).all() if active_plan else []
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.is_completed])
    progress_pct = int(round((completed_tasks / total_tasks * 100))) if total_tasks else 0

    # Upcoming exam countdown
    today = date.today()
    exams = ExamSchedule.query.filter_by(student_id=student.id).all()
    next_exam = None
    next_exam_days = 999
    for ex in exams:
        try:
            ex_date = datetime.strptime(ex.exam_date, "%Y-%m-%d").date()
            delta = (ex_date - today).days
            if 0 <= delta < next_exam_days:
                next_exam_days = delta
                next_exam = ex
        except Exception:
            pass

    # Weak & strong subjects
    weak_subjects = []
    strong_subjects = []
    for r in records:
        score = (r.internal_marks + r.previous_marks + r.assignment_marks) / 3
        if score < 60:
            weak_subjects.append(r.subject.name if r.subject else "Subject")
        elif score >= 75:
            strong_subjects.append(r.subject.name if r.subject else "Subject")

    avg_attendance = round(sum(r.attendance for r in records) / len(records), 1) if records else 85.0

    return render_template(
        "student_dashboard.html",
        student=student,
        records=records,
        predictions=predictions,
        latest_prediction=latest_prediction,
        active_plan=active_plan,
        progress_pct=progress_pct,
        completed_tasks_count=completed_tasks,
        total_tasks_count=total_tasks,
        next_exam=next_exam,
        next_exam_days=next_exam_days if next_exam else None,
        weak_subjects=weak_subjects,
        strong_subjects=strong_subjects,
        avg_attendance=avg_attendance,
    )


# ---------------------------------------------------------
# AI STUDY PLANNER (FEATURE INTEGRATION)
# ---------------------------------------------------------

@app.route("/study-planner")
@login_required
def study_planner():
    # If admin wants to view a specific student's planner
    target_student_id = request.args.get("student_id", type=int)
    if current_user.role == "admin" and target_student_id:
        student = Student.query.get(target_student_id)
    else:
        student = db.session.get(Student, current_user.student_id) if current_user.student_id else None

    if not student:
        flash("Student profile not found.", "warning")
        return redirect(url_for("dashboard"))

    # Get active plan or generate initial AI plan
    active_plan = StudyPlan.query.filter_by(student_id=student.id, status="active").first()
    if not active_plan:
        active_plan = generate_ai_study_plan(student)

    tasks = StudyTask.query.filter_by(plan_id=active_plan.id).order_by(StudyTask.scheduled_date, StudyTask.start_time).all() if active_plan else []

    # Calculate hours and completion metrics
    total_minutes = sum(t.duration_minutes for t in tasks)
    completed_minutes = sum(t.duration_minutes for t in tasks if t.is_completed)
    pending_minutes = total_minutes - completed_minutes

    total_hours = round(total_minutes / 60.0, 1)
    completed_hours = round(completed_minutes / 60.0, 1)
    pending_hours = round(pending_minutes / 60.0, 1)
    progress_pct = int(round((completed_minutes / total_minutes * 100))) if total_minutes else 0

    # Today's tasks
    today_str = date.today().strftime("%Y-%m-%d")
    today_tasks = [t for t in tasks if t.scheduled_date == today_str]
    today_completed = len([t for t in today_tasks if t.is_completed])
    today_total = len(today_tasks)
    today_pct = int(round((today_completed / today_total * 100))) if today_total else 0

    # Subject-wise distribution for Chart.js
    subject_hours = {}
    for t in tasks:
        hrs = t.duration_minutes / 60.0
        subject_hours[t.subject_name] = subject_hours.get(t.subject_name, 0.0) + hrs
    subject_chart_data = {
        "labels": list(subject_hours.keys()),
        "hours": [round(h, 1) for h in subject_hours.values()],
    }

    # Priority subjects
    records = AcademicRecord.query.filter_by(student_id=student.id).all()
    priority_subjects = []
    for r in records:
        comp = (r.internal_marks * 0.35) + (r.previous_marks * 0.35) + (r.assignment_marks * 0.30)
        priority_label = "High" if comp < 60 else ("Medium" if comp < 75 else "Low")
        priority_subjects.append({
            "name": r.subject.name if r.subject else "Subject",
            "score": round(comp, 1),
            "priority": priority_label,
            "attendance": r.attendance,
        })
    priority_subjects.sort(key=lambda s: s["score"])

    # Upcoming examinations
    exams = ExamSchedule.query.filter_by(student_id=student.id).order_by(ExamSchedule.exam_date).all()
    exam_countdown_list = []
    today_d = date.today()
    for ex in exams:
        try:
            ex_date = datetime.strptime(ex.exam_date, "%Y-%m-%d").date()
            delta = (ex_date - today_d).days
            exam_countdown_list.append({
                "subject": ex.subject_name,
                "name": ex.exam_name,
                "date": ex.exam_date,
                "days_left": delta,
                "urgency": "danger" if delta <= 5 else ("warning" if delta <= 10 else "info")
            })
        except Exception:
            pass

    # Intelligent Recommendations & Reminders
    recommendations = get_intelligent_recommendations(student)
    reminders = get_student_reminders(student)

    # Student's enrolled subjects for the task modal
    all_subjects = Subject.query.all()
    if not all_subjects and records:
        all_subjects = [r.subject for r in records if r.subject]

    return render_template(
        "study_planner.html",
        student=student,
        active_plan=active_plan,
        tasks=tasks,
        total_hours=total_hours,
        completed_hours=completed_hours,
        pending_hours=pending_hours,
        progress_pct=progress_pct,
        today_tasks=today_tasks,
        today_completed=today_completed,
        today_total=today_total,
        today_pct=today_pct,
        subject_chart_data=subject_chart_data,
        priority_subjects=priority_subjects,
        exam_countdown_list=exam_countdown_list,
        recommendations=recommendations,
        reminders=reminders,
        all_subjects=all_subjects,
        today_date=today_str,
    )


# ---------------------------------------------------------
# STUDY PLANNER API ENDPOINTS (AJAX/Fetch)
# ---------------------------------------------------------

@app.route("/api/study-plan/generate", methods=["POST"])
@login_required
def api_generate_study_plan():
    student_id = request.json.get("student_id") if (current_user.role == "admin" and request.json.get("student_id")) else current_user.student_id
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    daily_hours = float(request.json.get("daily_study_hours", 3.0))
    preferred_timing = request.json.get("preferred_timing", "Evening")
    plan_days = int(request.json.get("plan_days", 7))

    plan = generate_ai_study_plan(student, daily_study_hours=daily_hours, preferred_timing=preferred_timing, plan_days=plan_days)
    return jsonify({
        "success": True,
        "message": "AI Study Plan generated successfully!",
        "plan_id": plan.id,
        "title": plan.title,
        "summary": plan.ai_summary,
    })


@app.route("/api/study-task/<int:task_id>/toggle", methods=["POST"])
@login_required
def api_toggle_study_task(task_id):
    task = StudyTask.query.get(task_id)
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    # Authorization check
    if current_user.role != "admin" and task.student_id != current_user.student_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    task.is_completed = not task.is_completed
    task.completed_at = datetime.utcnow() if task.is_completed else None
    db.session.commit()

    # Recalculate plan metrics
    all_tasks = StudyTask.query.filter_by(plan_id=task.plan_id).all()
    total_minutes = sum(t.duration_minutes for t in all_tasks)
    completed_minutes = sum(t.duration_minutes for t in all_tasks if t.is_completed)
    progress_pct = int(round((completed_minutes / total_minutes * 100))) if total_minutes else 0

    return jsonify({
        "success": True,
        "task_id": task.id,
        "is_completed": task.is_completed,
        "progress_pct": progress_pct,
        "completed_hours": round(completed_minutes / 60.0, 1),
        "pending_hours": round((total_minutes - completed_minutes) / 60.0, 1),
    })


@app.route("/api/study-task/add", methods=["POST"])
@login_required
def api_add_study_task():
    student_id = current_user.student_id
    if not student_id:
        return jsonify({"success": False, "message": "No student profile"}), 400

    active_plan = StudyPlan.query.filter_by(student_id=student_id, status="active").first()
    if not active_plan:
        active_plan = generate_ai_study_plan(Student.query.get(student_id))

    data = request.json or request.form
    subject_name = data.get("subject_name", "General Studies").strip()
    task_title = data.get("task_title", "").strip()
    topic_name = data.get("topic_name", "").strip()
    scheduled_date = data.get("scheduled_date", date.today().strftime("%Y-%m-%d"))
    start_time = data.get("start_time", "18:00")
    duration_minutes = int(data.get("duration_minutes", 60))
    priority = data.get("priority", "Medium")
    task_type = data.get("task_type", "personal")
    notes = data.get("notes", "")

    if not task_title:
        return jsonify({"success": False, "message": "Task title is required"}), 400

    task = StudyTask(
        plan_id=active_plan.id,
        student_id=student_id,
        subject_name=subject_name,
        task_title=task_title,
        topic_name=topic_name,
        scheduled_date=scheduled_date,
        start_time=start_time,
        duration_minutes=duration_minutes,
        priority=priority,
        task_type=task_type,
        is_completed=False,
        notes=notes,
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({"success": True, "message": "Task added to study calendar", "task_id": task.id})


@app.route("/api/study-task/<int:task_id>/edit", methods=["POST"])
@login_required
def api_edit_study_task(task_id):
    task = StudyTask.query.get(task_id)
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404
    if current_user.role != "admin" and task.student_id != current_user.student_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json or request.form
    if "scheduled_date" in data:
        task.scheduled_date = data["scheduled_date"]
    if "start_time" in data:
        task.start_time = data["start_time"]
    if "duration_minutes" in data:
        task.duration_minutes = int(data["duration_minutes"])
    if "notes" in data:
        task.notes = data["notes"]
    if "task_title" in data:
        task.task_title = data["task_title"]
    if "priority" in data:
        task.priority = data["priority"]

    db.session.commit()
    return jsonify({"success": True, "message": "Task updated successfully"})


@app.route("/api/study-task/<int:task_id>/delete", methods=["POST"])
@login_required
def api_delete_study_task(task_id):
    task = StudyTask.query.get(task_id)
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404
    if current_user.role != "admin" and task.student_id != current_user.student_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True, "message": "Task deleted successfully"})


@app.route("/api/study-planner/preferences", methods=["POST"])
@login_required
def api_update_study_preferences():
    student_id = current_user.student_id
    plan = StudyPlan.query.filter_by(student_id=student_id, status="active").first()
    data = request.json or {}

    daily_hours = float(data.get("daily_study_hours", 3.0))
    preferred_timing = data.get("preferred_timing", "Evening")

    if plan:
        plan.daily_study_hours = daily_hours
        plan.preferred_timing = preferred_timing
        db.session.commit()

    return jsonify({"success": True, "message": "Preferences updated successfully"})


@app.route("/api/set-language", methods=["POST"])
def api_set_language():
    data = request.json or {}
    lang = data.get("language", "en")
    session["lang"] = lang

    if current_user.is_authenticated:
        current_user.language_pref = lang
        db.session.commit()

    return jsonify({"success": True, "language": lang})


# ---------------------------------------------------------
# PREDICTION ROUTE (ATTENDANCE INPUT REMOVED)
# ---------------------------------------------------------

@app.route("/prediction", methods=["GET", "POST"])
@login_required
def prediction():
    result = None
    student = db.session.get(Student, current_user.student_id) if current_user.student_id else None
    student_records = AcademicRecord.query.filter_by(student_id=student.id).all() if student else []

    if request.method == "POST":
        try:
            # Notice: Attendance is intentionally NOT required nor used as an input feature
            internal_marks = float(request.form.get("internal_marks", 0))
            assignment_marks = float(request.form.get("assignment_marks", 0))
            previous_marks = float(request.form.get("previous_marks", 0))
            study_hours = float(request.form.get("study_hours", 2.0))
            subject_id = request.form.get("subject_id", type=int)

            predicted_marks, category = predict_final_marks(
                internal_marks=internal_marks,
                assignment_marks=assignment_marks,
                previous_marks=previous_marks,
                study_hours=study_hours,
            )

            result = {
                "marks": predicted_marks,
                "category": category,
                "values": {
                    "internal_marks": internal_marks,
                    "assignment_marks": assignment_marks,
                    "previous_marks": previous_marks,
                    "study_hours": study_hours,
                },
            }

            # Save prediction record
            if student:
                pred_record = Prediction(
                    student_id=student.id,
                    subject_id=subject_id if subject_id else None,
                    predicted_marks=predicted_marks,
                    performance_category=category,
                )
                db.session.add(pred_record)
                db.session.commit()
                flash("AI prediction completed and saved to your profile.", "success")
        except Exception as e:
            flash(f"Error computing prediction: {str(e)}", "danger")

    return render_template("prediction.html", result=result, student=student, records=student_records)


# ---------------------------------------------------------
# ADMIN MANAGEMENT ROUTES
# ---------------------------------------------------------

@app.route("/students", methods=["GET", "POST"])
@role_required("admin")
def students():
    if request.method == "POST":
        usn = request.form.get("usn", "").strip().upper()
        name = request.form.get("name", "").strip()
        branch = request.form.get("branch", "").strip()
        semester = int(request.form.get("semester", 1))
        email = request.form.get("email", "").strip().lower()

        if Student.query.filter(or_(Student.usn == usn, Student.email == email)).first():
            flash("Student with this USN or email already exists.", "warning")
        else:
            student = Student(usn=usn, name=name, branch=branch, semester=semester, email=email)
            db.session.add(student)
            db.session.commit()
            seed_student_academic_records(student)
            flash("Student added successfully.", "success")
        return redirect(url_for("students"))

    search = request.args.get("search", "").strip()
    query = Student.query
    if search:
        query = query.filter(or_(Student.usn.ilike(f"%{search}%"), Student.name.ilike(f"%{search}%")))
    student_list = query.order_by(Student.id.desc()).all()

    return render_template("students.html", students=student_list, search=search)


@app.route("/academic", methods=["GET", "POST"])
@app.route("/academic_records", methods=["GET", "POST"])
@role_required("admin")
def academic_records():
    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        subject_name = request.form.get("subject_name", "").strip()
        attendance = float(request.form.get("attendance", 80))
        internal_marks = float(request.form.get("internal_marks", 0))
        assignment_marks = float(request.form.get("assignment_marks", 0))
        previous_marks = float(request.form.get("previous_marks", 0))
        study_hours = float(request.form.get("study_hours", 2.0))

        subject = Subject.query.filter_by(name=subject_name).first()
        if not subject:
            subject = Subject(name=subject_name)
            db.session.add(subject)
            db.session.flush()

        record = AcademicRecord(
            student_id=student_id,
            subject_id=subject.id,
            attendance=attendance,
            internal_marks=internal_marks,
            assignment_marks=assignment_marks,
            previous_marks=previous_marks,
            study_hours=study_hours,
        )
        db.session.add(record)
        db.session.commit()
        flash("Academic record saved successfully.", "success")
        return redirect(url_for("academic_records"))

    students_list = Student.query.order_by(Student.name).all()
    records_query = db.session.query(AcademicRecord, Student, Subject).join(Student, AcademicRecord.student_id == Student.id).join(Subject, AcademicRecord.subject_id == Subject.id).order_by(AcademicRecord.id.desc()).all()

    return render_template("academic.html", students=students_list, records=records_query)


@app.route("/admin/study-plans")
@role_required("admin")
def admin_study_plans():
    """Allows teachers and administrators to view student study progress according to their permissions."""
    students_list = Student.query.order_by(Student.name).all()
    overview_data = []

    for s in students_list:
        plan = StudyPlan.query.filter_by(student_id=s.id, status="active").first()
        if plan:
            tasks = StudyTask.query.filter_by(plan_id=plan.id).all()
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.is_completed])
            pct = int(round((completed_tasks / total_tasks * 100))) if total_tasks else 0
            total_hrs = round(sum(t.duration_minutes for t in tasks) / 60.0, 1)
            comp_hrs = round(sum(t.duration_minutes for t in tasks if t.is_completed) / 60.0, 1)
        else:
            pct = 0
            total_hrs = 0.0
            comp_hrs = 0.0
            total_tasks = 0
            completed_tasks = 0

        overview_data.append({
            "student": s,
            "has_plan": plan is not None,
            "progress_pct": pct,
            "completed_hours": comp_hrs,
            "total_hours": total_hrs,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
        })

    return render_template("admin_study_plans.html", overview_data=overview_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# ---------------------------------------------------------
# DATABASE INITIALIZATION & SAMPLE DATA SEEDER
# ---------------------------------------------------------

def seed_student_academic_records(student):
    """Seed realistic academic subjects, marks, and upcoming exams for a student."""
    subjects_seed = [
        {"name": "Mathematics", "attendance": 78.0, "internal": 44.0, "assignment": 56.0, "prev": 46.0, "hrs": 1.5, "exam_days": 10},
        {"name": "Java Programming", "attendance": 92.0, "internal": 86.0, "assignment": 90.0, "prev": 84.0, "hrs": 2.5, "exam_days": 16},
        {"name": "Database Management Systems", "attendance": 84.0, "internal": 62.0, "assignment": 70.0, "prev": 58.0, "hrs": 2.0, "exam_days": 5},
        {"name": "Data Structures & Algorithms", "attendance": 80.0, "internal": 52.0, "assignment": 64.0, "prev": 50.0, "hrs": 2.0, "exam_days": 21},
        {"name": "Operating Systems", "attendance": 88.0, "internal": 75.0, "assignment": 80.0, "prev": 72.0, "hrs": 1.5, "exam_days": 28},
    ]

    today = date.today()

    for s_info in subjects_seed:
        subject = Subject.query.filter_by(name=s_info["name"]).first()
        if not subject:
            subject = Subject(name=s_info["name"])
            db.session.add(subject)
            db.session.flush()

        # Check existing record
        rec = AcademicRecord.query.filter_by(student_id=student.id, subject_id=subject.id).first()
        if not rec:
            rec = AcademicRecord(
                student_id=student.id,
                subject_id=subject.id,
                attendance=s_info["attendance"],
                internal_marks=s_info["internal"],
                assignment_marks=s_info["assignment"],
                previous_marks=s_info["prev"],
                study_hours=s_info["hrs"],
            )
            db.session.add(rec)

        # Exam schedule
        exam_date_str = (today + timedelta(days=s_info["exam_days"])).strftime("%Y-%m-%d")
        exam = ExamSchedule.query.filter_by(student_id=student.id, subject_name=s_info["name"]).first()
        if not exam:
            exam = ExamSchedule(
                student_id=student.id,
                subject_id=subject.id,
                subject_name=s_info["name"],
                exam_name=f"{s_info['name']} Semester Examination",
                exam_date=exam_date_str,
                syllabus_coverage="Units 1 to 5",
            )
            db.session.add(exam)

    db.session.commit()


with app.app_context():
    db.create_all()

    # Development-only administrator account
    if not User.query.filter_by(email="admin@college.edu").first():
        db.session.add(User(
            name="Administrator",
            email="admin@college.edu",
            password_hash=generate_password_hash("Admin@123"),
            role="admin",
        ))
        db.session.commit()

    # Ensure existing student users (e.g. Rakshitha) are linked to Student records with data
    student_users = User.query.filter_by(role="student").all()
    for u in student_users:
        if not u.student_id:
            student = Student.query.filter_by(email=u.email).first()
            if not student:
                student = Student(
                    name=u.name,
                    email=u.email,
                    usn=f"1RV21CS{u.id + 100:03d}",
                    branch="Computer Science",
                    semester=5,
                )
                db.session.add(student)
                db.session.flush()
            u.student_id = student.id
            db.session.commit()

        # Ensure academic records and active study plan exist for student
        st = db.session.get(Student, u.student_id)
        if st:
            seed_student_academic_records(st)
            if not StudyPlan.query.filter_by(student_id=st.id, status="active").first():
                generate_ai_study_plan(st)


if __name__ == "__main__":
    app.run(debug=True)
