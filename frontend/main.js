let currentStrategy = 'smart_balance';
const API_BASE = 'http://127.0.0.1:8000/api/tasks';

async function addTask(e) {
    e.preventDefault();
    const btn = document.getElementById('addBtn');
    btn.innerText = "Processing...";
    
    try {
        const response = await fetch(`${API_BASE}/create/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: document.getElementById('title').value,
                due_date: document.getElementById('date').value,
                importance: parseInt(document.getElementById('imp').value),
                estimated_hours: parseInt(document.getElementById('hours').value),
                dependencies: [] 
            })
        });

        if(response.ok) {
            document.getElementById('taskForm').reset();
            loadTasks();
        } else { alert("Error saving task"); }
    } catch (err) { alert("Backend Offline"); }
    btn.innerText = "Add Task";
}

function setStrategy(strat) {
    currentStrategy = strat;
    document.querySelectorAll('.strat-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    loadTasks();
}

async function loadTasks() {
    try {
        const res = await fetch(`${API_BASE}/analyze/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ strategy: currentStrategy })
        });
        const tasks = await res.json();
        render(tasks);
    } catch(e) {
        document.getElementById('results').innerHTML = `<p style="color:#ef4444">Connection Error: Ensure Django is running.</p>`;
    }
}

function render(tasks) {
    const container = document.getElementById('results');
    if (tasks.length === 0) {
        container.innerHTML = '<p style="padding:20px; color:#555;">No tasks found. Create one on the left.</p>';
        return;
    }

    container.innerHTML = tasks.map(t => {
        const color = getColor(t.score);
        return `
        <div class="task-card" style="border-left-color: ${color}">
            <div>
                <h4 style="margin:0 0 5px 0; font-size:1.1rem;">${t.title}</h4>
                <div style="font-size:0.85rem; color:#94a3b8;">
                    📅 ${t.due_date} • ⏱ ${t.estimated_hours}h • ⭐ ${t.importance}
                </div>
                <div style="margin-top:8px; font-size:0.9rem; color:${color};">
                    ${t.explanation}
                </div>
            </div>
            <div class="score-circle" style="color:${color}; box-shadow: 0 0 15px ${color}40;">
                ${Math.round(t.score)}
            </div>
        </div>
    `}).join('');
}

function getColor(score) {
    if(score >= 80) return '#ef4444'; // Red
    if(score >= 50) return '#f59e0b'; // Orange
    return '#10b981'; // Green
}

window.onload = loadTasks;
