const form = document.querySelector('#task-form');
const input = document.querySelector('#task-title');
const list = document.querySelector('#tasks');
const empty = document.querySelector('#empty-state');
const error = document.querySelector('#error-message');

function showError(message) {
  error.textContent = message || '';
  error.hidden = !message;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Request failed');
  return data;
}

function renderTasks(tasks) {
  list.replaceChildren();
  empty.hidden = tasks.length !== 0;
  document.querySelector('#total-count').textContent = tasks.length;
  const complete = tasks.filter(task => task.completed).length;
  document.querySelector('#complete-count').textContent = complete;
  document.querySelector('#remaining-count').textContent = tasks.length - complete;

  for (const task of tasks) {
    const row = document.createElement('li');
    const title = document.createElement('span');
    title.textContent = task.title; // Text content avoids injecting HTML.
    title.className = `task-title${task.completed ? ' done' : ''}`;
    const button = document.createElement('button');
    button.textContent = task.completed ? 'Completed' : 'Mark complete';
    button.className = 'complete-button';
    button.disabled = task.completed;
    button.addEventListener('click', async () => {
      try {
        showError('');
        await requestJson(`/api/tasks/${task.id}/complete`, { method: 'POST' });
        await loadTasks();
      } catch (err) { showError(err.message); }
    });
    row.append(title, button);
    list.append(row);
  }
}

async function loadTasks() {
  const data = await requestJson('/api/tasks');
  renderTasks(data.tasks);
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  try {
    showError('');
    await requestJson('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: input.value })
    });
    input.value = '';
    await loadTasks();
    input.focus();
  } catch (err) { showError(err.message); }
});

loadTasks().catch(err => showError(err.message));
