import { useState,useEffect } from 'react'

import './App.css'

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [text, setText] = useState("")

  async function addNote(e) {
    e.preventDefault();

    if(!title.trim()||!text.trim()) {
      return;
    }

    await fetch("http://127.0.0.1:8000/notes", {
      method: "POST",
      body:JSON.stringify({title: title, text: text}),
      headers: {"Content-Type": "application/json"}
    });

    await syncNotes();
    setTitle("");
    setText("");
  }
  async function deleteNote(note_id) {
    await fetch ("http://127.0.0.1:8000/notes/"+ note_id,{method:"DELETE"});
    await syncNotes();

  }

  async function syncNotes (){
    let response = await fetch("http://127.0.0.1:8000/notes");
    let data = await response.json();
    setNotes(data)

  }
  useEffect(() => {
    syncNotes();
  }, []);
  
  return (
    <div>
      <ul>
        {notes.map (note => (
          <li key = {note.id}>
            <div className='note-content'>
              <span>{note.title}</span>
              <span >{note.text}</span>
            </div>
            <button  onClick={() =>deleteNote(note.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
      <form onSubmit={addNote}>
        <input 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder='Введите заголовок...'
        
        />
        
        
        <input 
          value={text}
          onChange={(e)=> setText(e.target.value)}
          placeholder='Введите текст...'
        
        />
        <button type='submit'>Add Note</button>
      </form>
    </div>
  );
}

export default App
