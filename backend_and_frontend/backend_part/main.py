from fastapi import FastAPI, HTTPException,Response
from uvicorn import run
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

NOTES = []
NEXT_NOTE_ID = 1

class CreateNote(BaseModel):
    title: str
    text: str



@app.get("/notes")
async def get_notes():
    return NOTES

@app.post("/notes")
async def create_note(note: CreateNote):
    global NEXT_NOTE_ID
    new_note = {
        "id": NEXT_NOTE_ID,
        "title": note.title,
        "text": note.text
    }
    NOTES.append(new_note)
    NEXT_NOTE_ID+=1
    return  new_note

@app.delete("/notes/{note_id}")
async def delete_note(note_id:int):
    for note in NOTES:
        if note["id"] == note_id:
            NOTES.remove(note)
            return Response(status_code=204)
    raise HTTPException(status_code=404,detail="Note not found")

if __name__ == '__main__':
    run(app)


