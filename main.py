from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
from docx import Document
import models, os
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.is_deleted == False).order_by(models.Task.due_date).all()
    trash = db.query(models.Task).filter(models.Task.is_deleted == True).all()
    total = len(tasks)
    completed = len([t for t in tasks if t.is_completed])
    progress = int((completed / total) * 100) if total > 0 else 0
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "tasks": tasks, "trash": trash, "progress": progress})

@app.get("/export/word")
async def export_to_word(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.is_deleted == False).all()
    doc = Document()
    doc.add_heading('Мой список задач', 0)
    for task in tasks:
        status = " [V]" if task.is_completed else " [ ]"
        doc.add_paragraph(f"{task.due_date} | {task.title} ({task.category}){status}", style='List Bullet')
    file_path = "tasks.docx"
    doc.save(file_path)
    return FileResponse(path=file_path, filename="My_Tasks.docx")

@app.post("/add")
async def add_task(title: str = Form(...), category: str = Form(...), due_date: str = Form(...), db: Session = Depends(get_db)):
    date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
    db.add(models.Task(title=title, category=category, due_date=date_obj))
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{task_id}")
async def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.is_completed = not task.is_completed
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}")
async def to_trash(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.is_deleted = True
        db.commit()
    return RedirectResponse(url="/", status_code=303)
