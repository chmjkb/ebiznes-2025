import React, { useState, useEffect } from 'react';
import type { Todo, TodoCreate, TodoUpdate } from './types';
import { api } from './api';
import { TodoForm } from './components/TodoForm';
import { TodoItem } from './components/TodoItem';
import './App.css';

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      const todoList = await api.getTodos();
      setTodos(todoList);
      setError(null);
    } catch (err) {
      setError('Failed to load todos');
      console.error('Error loading todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (todoData: TodoCreate) => {
    try {
      const newTodo = await api.createTodo(todoData);
      setTodos([...todos, newTodo]);
      setError(null);
    } catch (err) {
      setError('Failed to create todo');
      console.error('Error creating todo:', err);
    }
  };

  const handleUpdateTodo = async (id: number, updates: TodoUpdate) => {
    try {
      const updatedTodo = await api.updateTodo(id, updates);
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
      setError(null);
    } catch (err) {
      setError('Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await api.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
      setError(null);
    } catch (err) {
      setError('Failed to delete todo');
      console.error('Error deleting todo:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading todos...</div>;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo List</h1>
      </header>
      
      {error && (
        <div className="error-message">
          {error}
          <button onClick={loadTodos} className="btn-retry">Retry</button>
        </div>
      )}
      
      <main className="app-main">
        <section className="todo-form-section">
          <h2>Add New Todo</h2>
          <TodoForm onSubmit={handleCreateTodo} />
        </section>
        
        <section className="todo-list-section">
          <h2>Your Todos ({todos.length})</h2>
          {todos.length === 0 ? (
            <p className="no-todos">No todos yet. Add one above!</p>
          ) : (
            <div className="todo-list">
              {todos.map(todo => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  onUpdate={handleUpdateTodo}
                  onDelete={handleDeleteTodo}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
