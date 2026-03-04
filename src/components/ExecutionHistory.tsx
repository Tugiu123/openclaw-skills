import { ExecutionLog } from '../types';

interface Props {
  logs: ExecutionLog[];
}

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default function ExecutionHistory({ logs }: Props) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      default: return 'ℹ️';
    }
  };

  return (
    <div>
      <h2>Execution History</h2>
      <div className="execution-history">
        {logs.length === 0 ? (
          <div className="empty-state">No execution logs</div>
        ) : (
          logs.map(log => (
            <div key={log.id} className="log-item">
              <div className="log-icon">{getStatusIcon(log.status)}</div>
              <div className="log-content">
                <div className="log-header">
                  <span className="log-bot">{log.botName}</span>
                  <span className="log-time">{formatTimeAgo(log.timestamp)}</span>
                </div>
                <div className="log-message">
                  <strong>{log.action}:</strong> {log.message}
                </div>
              </div>
              <span className={`log-status ${log.status}`}>
                {log.status}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
