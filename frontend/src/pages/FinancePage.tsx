import { useEffect, useState } from 'react';
import api from '../services/api';
import { Transaction } from '../services/types';
import styles from '../styles/App.module.css';

export function FinancePage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [description, setDescription] = useState('Venda balcão');
  const [amount, setAmount] = useState(10);

  const load = () => api.get('/transactions?days=30').then((r) => setTransactions(r.data));
  useEffect(() => { load(); }, []);

  const create = async () => {
    await api.post('/transactions', { description, amount, type: 'income', date: new Date().toISOString().slice(0, 10) });
    load();
  };

  return <div className={styles.container}><div className={styles.card}><h2>Financeiro</h2><input value={description} onChange={(e)=>setDescription(e.target.value)} /><input type='number' value={amount} onChange={(e)=>setAmount(Number(e.target.value))} /><button onClick={create}>Lançar</button></div><div className={styles.card}>{transactions.map(t => <div key={t.id}>{t.date} - {t.description} - R$ {t.amount}</div>)}</div></div>;
}
