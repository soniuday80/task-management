'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types';
import TaskPopup from '@/component/taskpopup';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showPopup, setShowPopup] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);

  useEffect(() => {
    setCurrentUserId(localStorage.getItem('user_id'));
    loadTasks();
  }, []);

  function loadTasks() {
    setLoading(true);
    api('/tasks')
      .then((res) => res.json())
      .then(setTasks)
      .finally(() => setLoading(false));
  }

  async function handleComplete(taskId: string) {
    
    const res = await api(`/tasks/${taskId}/complete`, { method: 'PATCH' });

    if (res.ok) {
      loadTasks()
    }
    else{
      const data = await res.json()
      setError(data.error || 'failed to complete task');
    }
    
  
  }

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Tasks</h1>
        <button onClick={() => setShowPopup(true)} className="bg-black text-white px-3 py-1 rounded">
          New Task
        </button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b">
              <th className="py-2">Title</th>
              <th>Status</th>
              <th>Created by</th>
              <th>Assigned to</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((t) => (
              <tr key={t.id} className="border-b">
                <td className="py-2">{t.title}</td>
                <td>{t.status}</td>
                <td>{t.creator_name}</td>
                <td>{t.assignee_name}</td>
                <td>
                  {t.assignee_id === currentUserId && t.status !== 'completed' && (
                    <button onClick={() => handleComplete(t.id)} className="text-sm underline">
                      Complete
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showPopup && (
        <TaskPopup onClose={() => setShowPopup(false)} onCreated={loadTasks} />
      )}
    </main>
  );
}