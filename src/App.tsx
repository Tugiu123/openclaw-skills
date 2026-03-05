import { useState, useEffect } from 'react';
import { Nanobot, Task, ExecutionLog } from './types';
import NanobotCard from './components/NanobotCard';
import TaskQueue from './components/TaskQueue';
import ExecutionHistory from './components/ExecutionHistory';
import StatsCard from './components/StatsCard';

// Mock Data
const initialNanobots: Nanobot[] = [
  {
    id: 'nb-001',
    name: 'Monitor-01',
    status: 'running',
    currentTask: 'Price Monitoring - BTC',
    progress: 75,
    role: 'Market Monitor',
    uptime: 3456000,
    lastUpdate: new Date()
  },
  {
    id: 'nb-002',
    name: 'Collector-Pro',
    status: 'running',
    currentTask: 'Data Collection - News',
    progress: 45,
    role: 'Data Collector',
    uptime: 1728000,
    lastUpdate: new Date()
  },
  {
    id: 'nb-003',
    name: 'Alert-Expert',
    status: 'idle',
    progress: 0,
    role: 'Alert System',
    uptime: 5184000,
    lastUpdate: new Date()
  },
  {
    id: 'nb-004',
    name: 'Analyzer-01',
    status: 'completed',
    currentTask: 'Daily Analysis Report',
    progress: 100,
    role: 'Analysis',
    uptime: 864000,
    lastUpdate: new Date()
  },
  {
    id: 'nb-005',
    name: 'Task-Bot-02',
    status: 'error',
    currentTask: 'API Sync',
    progress: 30,
    role: 'Task Runner',
    uptime: 432000,
    lastUpdate: new Date()
  }
];

const initialTasks: Task[] = [
  {
    id: 't-001',
    name: 'Analyze Polymarket Iran Markets',
    status: 'in-progress',
    assignedBot: 'nb-001',
    priority: 'high',
    createdAt: new Date(Date.now() - 3600000)
  },
  {
    id: 't-002',
    name: 'Generate Morning Report',
    status: 'pending',
    priority: 'medium',
    createdAt: new Date(Date.now() - 1800000)
  },
  {
    id: 't-003',
    name: 'Check System Health',
    status: 'completed',
    assignedBot: 'nb-003',
    priority: 'low',
    createdAt: new Date(Date.now() - 7200000),
    completedAt: new Date(Date.now() - 7000000),
    duration: 200
  },
  {
    id: 't-004',
    name: 'Update Memory Cache',
    status: 'pending',
    priority: 'critical',
    createdAt: new Date(Date.now() - 900000)
  },
  {
    id: 't-005',
    name: 'Sync GitHub Repositories',
    status: 'failed',
    assignedBot: 'nb-005',
    priority: 'medium',
    createdAt: new Date(Date.now() - 5400000),
    duration: 45
  }
];

const initialLogs: ExecutionLog[] = [
  {
    id: 'l-001',
    botId: 'nb-001',
    botName: 'Monitor-01',
    action: 'Task Completed',
    status: 'success',
    message: 'BTC price alert triggered at $67,500',
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: 'l-002',
    botId: 'nb-002',
    botName: 'Collector-Pro',
    action: 'Data Fetch',
    status: 'success',
    message: 'Collected 125 news articles',
    timestamp: new Date(Date.now() - 600000)
  },
  {
    id: 'l-003',
    botId: 'nb-005',
    botName: 'Task-Bot-02',
    action: 'API Call',
    status: 'error',
    message: 'Rate limit exceeded - retry in 60s',
    timestamp: new Date(Date.now() - 900000)
  },
  {
    id: 'l-004',
    botId: 'nb-003',
    botName: 'Alert-Expert',
    action: 'Notification Sent',
    status: 'success',
    message: 'Telegram alert delivered to user',
    timestamp: new Date(Date.now() - 1200000)
  },
  {
    id: 'l-005',
    botId: 'nb-004',
    botName: 'Analyzer-01',
    action: 'Report Generated',
    status: 'success',
    message: 'Daily analysis report - 15 pages',
    timestamp: new Date(Date.now() - 1800000)
  }
];

function App() {
  const [nanobots, setNanobots] = useState<Nanobot[]>(initialNanobots);
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [logs, setLogs] = useState<ExecutionLog[]>(initialLogs);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setNanobots(prev => prev.map(bot => ({
        ...bot,
        progress: bot.status === 'running' 
          ? Math.min(100, bot.progress + Math.random() * 5)
          : bot.progress,
        lastUpdate: new Date()
      })));
      setLastUpdate(new Date());
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const activeBots = nanobots.filter(b => b.status === 'running').length;
  const idleBots = nanobots.filter(b => b.status === 'idle').length;
  const errorBots = nanobots.filter(b => b.status === 'error').length;
  const pendingTasks = tasks.filter(t => t.status === 'pending').length;

  return (
    <div className="dashboard">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🤖</span>
            <h1>Nanobot Task Dashboard</h1>
          </div>
          <div className="header-info">
            <span className="update-time">
              Last Update: {lastUpdate.toLocaleTimeString()}
            </span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="stats-grid">
          <StatsCard 
            title="Active Bots" 
            value={activeBots} 
            icon="⚡" 
            color="#22c55e"
          />
          <StatsCard 
            title="Idle Bots" 
            value={idleBots} 
            icon="💤" 
            color="#6b7280"
          />
          <StatsCard 
            title="Error Bots" 
            value={errorBots} 
            icon="⚠️" 
            color="#ef4444"
          />
          <StatsCard 
            title="Pending Tasks" 
            value={pendingTasks} 
            icon="📋" 
            color="#f59e0b"
          />
        </section>

        <section className="bots-section">
          <h2>Active Nanobots</h2>
          <div className="bots-grid">
            {nanobots.map(bot => (
              <NanobotCard key={bot.id} bot={bot} />
            ))}
          </div>
        </section>

        <div className="bottom-sections">
          <section className="tasks-section">
            <TaskQueue tasks={tasks} />
          </section>
          <section className="logs-section">
            <ExecutionHistory logs={logs} />
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
