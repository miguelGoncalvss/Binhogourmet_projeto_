import { useEffect, useState } from 'react';
import api from '../services/api';
import { Ingredient } from '../services/types';
import styles from '../styles/App.module.css';

export function InventoryPage() {
  const [items, setItems] = useState<Ingredient[]>([]);
  const [name, setName] = useState('');
  const [unit, setUnit] = useState('kg');
  const [quantity, setQuantity] = useState(1);
  const [unitCost, setUnitCost] = useState(1);

  const load = () => api.get('/ingredients').then((r) => setItems(r.data));
  useEffect(() => { load(); }, []);

  const create = async () => {
    await api.post('/ingredients', { name, unit, quantity, unit_cost: unitCost });
    setName(''); setQuantity(1); setUnitCost(1); load();
  };

  return <div className={styles.container}><div className={styles.card}><h2>Estoque</h2><input placeholder='Nome' value={name} onChange={(e)=>setName(e.target.value)} /><select value={unit} onChange={(e)=>setUnit(e.target.value)}><option>kg</option><option>g</option><option>L</option><option>ml</option><option>un</option></select><input type='number' value={quantity} onChange={(e)=>setQuantity(Number(e.target.value))} /><input type='number' value={unitCost} onChange={(e)=>setUnitCost(Number(e.target.value))} /><button onClick={create}>Adicionar</button></div><div className={styles.card}>{items.map(i => <div key={i.id}>{i.name} - {i.quantity}{i.unit} - R$ {i.unit_cost}</div>)}</div></div>;
}
