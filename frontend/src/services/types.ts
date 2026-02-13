export type Ingredient = { id: number; name: string; unit: string; quantity: number; unit_cost: number };
export type RecipeLine = { ingredient_id: number; qty: number; id?: number };
export type Recipe = {
  id: number;
  product_name: string;
  yield_units: number;
  packaging_cost_per_unit: number;
  labor_minutes_per_batch: number;
  labor_rate_per_hour: number;
  other_cost_per_unit: number;
  markup_multiplier: number;
  lines: RecipeLine[];
};
export type Transaction = { id:number; description:string; amount:number; type:string; date:string };
