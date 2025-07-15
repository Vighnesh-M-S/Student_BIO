const baseUrl = "http://127.0.0.1:5000";

let editMode = false;
let editId = null;

async function fetchStudents() {
  try {
    const res = await fetch(`${baseUrl}/students`);
    const data = await res.json();
    renderStudents(data);
  } catch (err) {
    console.error("Error fetching students:", err);
  }
}

function renderStudents(students) {
  const tbody = document.querySelector("#studentsTable tbody");
  tbody.innerHTML = "";

  students.forEach((stu) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td data-label="ID">${stu.id}</td>
      <td data-label="Name">${stu.name}</td>
      <td data-label="Age">${stu.age}</td>
      <td data-label="Email">${stu.email}</td>
      <td data-label="Actions" class="actions">
        <button data-id="${stu.id}" class="summary">Summary</button>
        <button data-id="${stu.id}" class="edit">Edit</button>
        <button data-id="${stu.id}" class="delete delete">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

document.getElementById("studentForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value.trim();
  const age = +document.getElementById("age").value;
  const email = document.getElementById("email").value.trim();

  if (!name || !email || isNaN(age)) return alert("Please fill all fields correctly.");

  try {
    if (editMode && editId !== null) {
      // Update student
      const res = await fetch(`${baseUrl}/students/${editId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, email }),
      });

      if (!res.ok) throw new Error("Failed to update student");

      editMode = false;
      editId = null;
      document.querySelector("#studentForm button").textContent = "Add";
    } else {
      // Add new student
      const res = await fetch(`${baseUrl}/students`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, email }),
      });

      if (!res.ok) {
        const { error } = await res.json();
        throw new Error(error || "Failed to add student");
      }
    }

    e.target.reset();
    fetchStudents();
  } catch (err) {
    alert(err.message);
  }
});

document.querySelector("#studentsTable").addEventListener("click", async (e) => {
    const id = e.target.dataset.id;
    if (!id) return;

    if (e.target.classList.contains("delete")) {
        if (!confirm("Delete this student?")) return;
        try {
          const res = await fetch(`${baseUrl}/students/${id}`, { method: "DELETE" });
          if (!res.ok) throw new Error("Deletion failed");
          fetchStudents();
        } catch (err) {
          alert(err.message);
        }
      }

    if (e.target.classList.contains("summary")) {
        try {
            const res = await fetch(`${baseUrl}/students/${id}/summary`);
            if (!res.ok) throw new Error("Could not fetch summary");
            const data = await res.json();
            const box = document.getElementById("summaryBox");
            box.style.display = "block";
            box.textContent = `Summary for student ${id}: ${data.summary}`;
          } catch (err) {
            alert(err.message);
          }
      }
      if (e.target.classList.contains("edit")) {
        const row = e.target.closest("tr").children;
        document.getElementById("name").value = row[1].textContent;
        document.getElementById("age").value = row[2].textContent;
        document.getElementById("email").value = row[3].textContent;
    
        editMode = true;
        editId = id;
        document.querySelector("#studentForm button").textContent = "Update";
      }
    });
    
fetchStudents();
    