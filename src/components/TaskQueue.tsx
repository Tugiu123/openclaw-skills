import { Task } from '../types';

interface Props {
  tasks: Task[];
}

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default function TaskQueue({ tasks }: Props) {
  const sortedTasks = [...tasks].sort((a, b) => {
    const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  return (
    <div>
      <h2>Task Queue</h2>
      <div className="task-queue">
        {sortedTasks.length === 0 ? (
          <div className="empty-state">No tasks in queue</div>
        ) : (
          sortedTasks.map(task => (
            <div key={task.id} className="task-item">
              <div className={`task-priority ${task.priority}`} />
              <div className="task-info">
                <div className="task-name-text">{task.name}</div>
                <div className="task-meta">
                  {task.assignedBot ? `Bot: ${task.assignedBot}` : 'Unassigned'} • {formatTimeAgo(task.createdAt)}
                </div>
              </div>
              <span className={`task-status ${task.status}`}>
                {task.status.replace('-', ' ')}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
