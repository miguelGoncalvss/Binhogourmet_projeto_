import { useEffect, useState } from 'react';
import api from '../services/api';
import styles from '../styles/App.module.css';

export function DashboardPage() {
  const [income, setIncome] = useState(0);
  useEffect(() => {
    api.get('/transactions?days=30').then(({ data }) => {
      const total = data.filter((t: any) => t.type === 'income').reduce((acc: number, t: any) => acc + t.amount, 0);
      setIncome(total);
    });
  }, []);

  return <div className={styles.container}><div className={styles.card}><h2>Dashboard</h2><p>Entradas últimos 30 dias: R$ {income.toFixed(2)}</p></div></div>;
}
