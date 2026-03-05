export interface Nanobot {
  id: string;
  name: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  currentTask?: string;
  progress: number;
  role?: string;
  uptime: number;
  lastUpdate: Date;
}

export interface Task {
  id: string;
  name: string;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  assignedBot?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  createdAt: Date;
  completedAt?: Date;
  duration?: number;
}

export interface ExecutionLog {
  id: string;
  botId: string;
  botName: string;
  action: string;
  status: 'success' | 'error' | 'warning';
  message: string;
  timestamp: Date;
}
