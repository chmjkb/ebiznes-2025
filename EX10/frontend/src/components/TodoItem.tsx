import React, { useState } from 'react';
import type { Todo } from '../types';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: number, updates: { title?: string; description?: string; completed?: boolean }) => void;
  onDelete: (id: number) => void;
}

export const TodoItem: React.FC<TodoItemProps> = ({ todo, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-checkbox">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={(e) => onUpdate(todo.id, { completed: e.target.checked })}
        />
      </div>
      
      {isEditing ? (
        <div className="todo-edit">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="todo-edit-title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="todo-edit-description"
            placeholder="Description (optional)"
          />
          <div className="todo-edit-actions">
            <button onClick={handleSave} className="btn-save">Save</button>
            <button onClick={handleCancel} className="btn-cancel">Cancel</button>
          </div>
        </div>
      ) : (
        <div className="todo-content">
          <h3 className="todo-title">{todo.title}</h3>
          {todo.description && <p className="todo-description">{todo.description}</p>}
          <div className="todo-meta">
            <span className="todo-date">Created: {new Date(todo.created_at).toLocaleDateString()}</span>
            {todo.updated_at !== todo.created_at && (
              <span className="todo-date">Updated: {new Date(todo.updated_at).toLocaleDateString()}</span>
            )}
          </div>
          <div className="todo-actions">
            <button onClick={() => setIsEditing(true)} className="btn-edit">Edit</button>
            <button onClick={() => onDelete(todo.id)} className="btn-delete">Delete</button>
          </div>
        </div>
      )}
    </div>
  );
};
