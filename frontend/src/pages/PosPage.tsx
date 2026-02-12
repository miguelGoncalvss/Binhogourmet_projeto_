import { useEffect, useState } from 'react';
import api from '../services/api';
import { Recipe } from '../services/types';
import styles from '../styles/App.module.css';

export function PosPage() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [recipeId, setRecipeId] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [unitPrice, setUnitPrice] = useState(10);
  const [message, setMessage] = useState('');

  useEffect(() => {
    api.get('/recipes').then((r) => {
      setRecipes(r.data);
      if (r.data.length) setRecipeId(r.data[0].id);
    });
  }, []);

  const finalize = async () => {
    try {
      const { data } = await api.post('/orders', { items: [{ recipe_id: recipeId, quantity, unit_price: unitPrice }] });
      setMessage(`Pedido #${data.id} finalizado. Total R$ ${data.total_amount}`);
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || 'Falha ao finalizar pedido');
    }
  };

  return <div className={styles.container}><div className={styles.card}><h2>PDV</h2><select value={recipeId} onChange={(e)=>setRecipeId(Number(e.target.value))}>{recipes.map(r => <option value={r.id} key={r.id}>{r.product_name}</option>)}</select><input type='number' value={quantity} onChange={(e)=>setQuantity(Number(e.target.value))} /><input type='number' value={unitPrice} onChange={(e)=>setUnitPrice(Number(e.target.value))} /><button onClick={finalize}>Finalizar venda</button>{message && <p>{message}</p>}</div></div>;
}
