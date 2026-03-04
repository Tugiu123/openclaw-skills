interface Props {
  title: string;
  value: number;
  icon: string;
  color: string;
}

export default function StatsCard({ title, value, icon, color }: Props) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <h3>{title}</h3>
        <div className="stat-value" style={{ color }}>{value}</div>
      </div>
    </div>
  );
}
