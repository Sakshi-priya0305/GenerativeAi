from fastapi import FastAPI
from pydantic import BaseModel
from auth import create_user, authenticate
from notes import save_note, get_notes
from gemini import generate_notes
from fastapi import Path
from notes import get_notes

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

class NotesRequest(BaseModel):
    user_id: int
    text: str

@app.post("/signup")
def signup(data: LoginRequest):
    if create_user(data.username, data.password):
        return {"message": "Account created"}
    return {"error": "User already exists"}

@app.post("/login")
def login(data: LoginRequest):
    user_id = authenticate(data.username, data.password)
    return {"user_id": user_id} if user_id else {"error": "Invalid credentials"}

@app.post("/generate_notes")
def generate(data: NotesRequest):
    notes = generate_notes(data.text)
    save_note(data.user_id, notes)
    return {"notes": notes}

@app.get("/notes/{user_id}")
def fetch_notes(user_id: int = Path(...)):
    notes = get_notes(user_id)
    return {"notes": notes}