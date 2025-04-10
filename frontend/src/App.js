import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);

  // Загрузка задач при монтировании компонента
  useEffect(() => {
    fetchTasks();
  }, []);

  // Получение списка задач с API
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/tasks/');
      const data = await response.json();
      setTasks(data);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка при загрузке задач:', error);
      setLoading(false);
    }
  };

  // Обработка изменения в полях ввода
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTask({
      ...newTask,
      [name]: value
    });
  };

  // Добавление новой задачи
  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTask.title) return;

    try {
      const response = await fetch('http://localhost:8000/api/tasks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newTask),
      });

      if (response.ok) {
        const createdTask = await response.json();
        setTasks([...tasks, createdTask]);
        setNewTask({ title: '', description: '' });
      }
    } catch (error) {
      console.error('Ошибка при добавлении задачи:', error);
    }
  };

  // Переключение статуса задачи (выполнено/не выполнено)
  const toggleTaskCompletion = async (taskId, currentStatus) => {
    try {
      const response = await fetch(`http://localhost:8000/api/tasks/${taskId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !currentStatus }),
      });

      if (response.ok) {
        setTasks(tasks.map(task => 
          task.id === taskId ? { ...task, completed: !task.completed } : task
        ));
      }
    } catch (error) {
      console.error('Ошибка при обновлении задачи:', error);
    }
  };

  // Удаление задачи
  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/tasks/${taskId}/`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId));
      }
    } catch (error) {
      console.error('Ошибка при удалении задачи:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AKFADesk Task Manager</h1>
      </header>

      <main className="container">
        <section className="add-task-section">
          <h2>Добавить новую задачу</h2>
          <form onSubmit={handleAddTask}>
            <input
              type="text"
              name="title"
              placeholder="Название задачи"
              value={newTask.title}
              onChange={handleInputChange}
              required
            />
            <textarea
              name="description"
              placeholder="Описание (необязательно)"
              value={newTask.description}
              onChange={handleInputChange}
            />
            <button type="submit">Добавить задачу</button>
          </form>
        </section>

        <section className="tasks-section">
          <h2>Список задач</h2>
          {loading ? (
            <p>Загрузка...</p>
          ) : tasks.length === 0 ? (
            <p>Нет задач. Добавьте первую задачу!</p>
          ) : (
            <ul className="tasks-list">
              {tasks.map((task) => (
                <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <div className="task-content">
                    <h3>{task.title}</h3>
                    {task.description && <p>{task.description}</p>}
                    <p className="task-created">
                      Создано: {new Date(task.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="task-actions">
                    <button
                      onClick={() => toggleTaskCompletion(task.id, task.completed)}
                      className="toggle-btn"
                    >
                      {task.completed ? 'Отметить как невыполненную' : 'Отметить как выполненную'}
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="delete-btn"
                    >
                      Удалить
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
