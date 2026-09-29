'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { User } from '@/types';

interface Props {
  onClose: () => void;
  onCreated: () => void;
}

export default function TaskPopup({ onClose, onCreated }: Props) {
  const [users, setUsers] = useState<User[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api('/users')
      .then((res) => res.json())
      .then(setUsers)
      .catch(() => setError('could not load users'));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('title is required');
      return;
    }
    if (!assignedTo) {
      setError('please select an assignee');
      return;
    }

    setSubmitting(true);

    try {
      const res = await api('/tasks', {
        method: 'POST',
        body: JSON.stringify({ title: trimmedTitle, description, assigned_to: assignedTo }),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.error || 'failed to create task');
        return;
      }

      onCreated();
      onClose();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg w-96 space-y-3">
        <h2 className="text-lg font-semibold">New Task</h2>

        <input
          className="border w-full p-2 rounded"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          className="border w-full p-2 rounded"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <select
          className="border w-full p-2 rounded"
          value={assignedTo}
          onChange={(e) => setAssignedTo(e.target.value)}
        >
          <option value="">Assign to...</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>{u.name}</option>
          ))}
        </select>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <div className="flex justify-end gap-2">
          <button type="button" onClick={onClose} className="px-3 py-1">Cancel</button>
          <button type="submit" disabled={submitting} className="px-3 py-1 bg-black text-white rounded">
            {submitting ? 'Saving...' : 'Create'}
          </button>
        </div>
      </form>
    </div>
  );
}