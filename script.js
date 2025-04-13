const API_URL = "http://127.0.0.1:8000";
const addBtn = document.querySelector("#addBtn");
const addBtn2 = document.querySelector("#addBtn2");
const main = document.querySelector("#main");

// Load notes from backend
async function loadNotes() {
    const response = await fetch(`${API_URL}/notes`);
    const notes = await response.json();
    main.innerHTML = ""; // Clear previous notes
    notes.forEach((note, index) => addNote(note.content, note.title, index));
}

// Save a new note to the backend
async function saveNotes(title, content) {
    const noteData = { title, content };
    await fetch(`${API_URL}/add_note`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noteData),
    });
    loadNotes(); // Refresh notes
}

// Delete a note from the backend
async function deleteNote(index) {
    await fetch(`${API_URL}/delete_note/${index}`, {
        method: "DELETE",
    });
    loadNotes();
}

// Add a note element to the UI
const addNote = (text = "", title = "", index = null) => {
    const note = document.createElement("div");
    note.classList.add("note");
    note.innerHTML = `
    <div class="icons">
        <i class="save fas fa-save" style="color:red"></i>
        <i class="trash fas fa-trash" style="color:yellow"></i>
    </div>
    <div class="title-div">
        <textarea class="title" placeholder="Write the title ...">${title}</textarea>
    </div>
    <textarea class="content" placeholder="Note down your thoughts ...">${text}</textarea>
    `;

    const delBtn = note.querySelector(".trash");
    const saveButton = note.querySelector(".save");
    const titleInput = note.querySelector(".title");
    const contentInput = note.querySelector(".content");

    // Handle save button click
    saveButton.addEventListener("click", () => {
        saveNotes(titleInput.value, contentInput.value);
    });

    // Handle delete button click
    delBtn.addEventListener("click", async () => {
        if (index !== null) {
            await deleteNote(index);
        }
        note.remove();
    });

    main.appendChild(note);
};

// Add a new blank note on button click
addBtn.addEventListener("click", () => addNote());

addBtn2.addEventListener("click",()=>{
    window.location.href = "game.html"
})

// Load notes on page load
loadNotes();
