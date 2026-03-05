import { Nanobot } from '../types';

interface Props {
  bot: Nanobot;
}

function formatUptime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const days = Math.floor(hours / 24);
  if (days > 0) {
    return `${days}d ${hours % 24}h`;
  }
  return `${hours}h`;
}

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default function NanobotCard({ bot }: Props) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return '#22c55e';
      case 'idle': return '#6b7280';
      case 'completed': return '#3b82f6';
      case 'error': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="nanobot-card">
      <div className="nanobot-header">
        <div>
          <div className="nanobot-name">{bot.name}</div>
          {bot.role && <span className="nanobot-role">{bot.role}</span>}
        </div>
        <span className={`status-badge ${bot.status}`}>
          {bot.status}
        </span>
      </div>

      {bot.currentTask && (
        <div className="nanobot-task">
          <div className="task-label">Current Task</div>
          <div className="task-name">{bot.currentTask}</div>
        </div>
      )}

      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ 
            width: `${bot.progress}%`,
            background: `linear-gradient(90deg, ${getStatusColor(bot.status)}, #a855f7)`
          }}
        />
      </div>

      <div className="nanobot-footer">
        <span>Uptime: {formatUptime(bot.uptime)}</span>
        <span>{formatTimeAgo(bot.lastUpdate)}</span>
      </div>
    </div>
  );
}
