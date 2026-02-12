import { useEffect, useState } from 'react';
import api from '../services/api';
import { Ingredient, Recipe } from '../services/types';
import styles from '../styles/App.module.css';

export function RecipesPage() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [productName, setProductName] = useState('');
  const [ingredientId, setIngredientId] = useState<number>(0);
  const [qty, setQty] = useState(100);

  const load = async () => {
    const [r1, r2] = await Promise.all([api.get('/recipes'), api.get('/ingredients')]);
    setRecipes(r1.data);
    setIngredients(r2.data);
    if (r2.data.length && !ingredientId) setIngredientId(r2.data[0].id);
  };

  useEffect(() => { load(); }, []);

  const create = async () => {
    await api.post('/recipes', {
      product_name: productName,
      yield_units: 10,
      packaging_cost_per_unit: 0.5,
      labor_minutes_per_batch: 30,
      labor_rate_per_hour: 20,
      other_cost_per_unit: 0,
      markup_multiplier: 2,
      lines: [{ ingredient_id: ingredientId, qty }]
    });
    setProductName('');
    load();
  };

  return <div className={styles.container}><div className={styles.card}><h2>Receitas</h2><input value={productName} placeholder='Produto' onChange={(e)=>setProductName(e.target.value)} /><select value={ingredientId} onChange={(e)=>setIngredientId(Number(e.target.value))}>{ingredients.map(i => <option key={i.id} value={i.id}>{i.name}</option>)}</select><input type='number' value={qty} onChange={(e)=>setQty(Number(e.target.value))} /><button onClick={create}>Criar receita</button></div><div className={styles.card}>{recipes.map(r => <div key={r.id}>{r.product_name}</div>)}</div></div>;
}
