import { Navigate, Route, Routes, Link } from 'react-router-dom';
import { useState } from 'react';
import styles from './styles/App.module.css';
import { LoginPage } from './pages/LoginPage';
import { InventoryPage } from './pages/InventoryPage';
import { RecipesPage } from './pages/RecipesPage';
import { FinancePage } from './pages/FinancePage';
import { PosPage } from './pages/PosPage';
import { DashboardPage } from './pages/DashboardPage';

const isAuthenticated = () => Boolean(localStorage.getItem('token'));

function Protected({ children }: { children: JSX.Element }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  const [refresh, setRefresh] = useState(0);
  const logout = () => {
    localStorage.removeItem('token');
    setRefresh((v) => v + 1);
  };

  return (
    <div className={styles.app} key={refresh}>
      {isAuthenticated() && (
        <nav className={styles.nav}>
          <Link to="/">Dashboard</Link>
          <Link to="/inventory">Estoque</Link>
          <Link to="/recipes">Receitas</Link>
          <Link to="/finance">Financeiro</Link>
          <Link to="/pos">PDV</Link>
          <button onClick={logout}>Sair</button>
        </nav>
      )}
      <Routes>
        <Route path="/login" element={<LoginPage onSuccess={() => setRefresh((v) => v + 1)} />} />
        <Route path="/" element={<Protected><DashboardPage /></Protected>} />
        <Route path="/inventory" element={<Protected><InventoryPage /></Protected>} />
        <Route path="/recipes" element={<Protected><RecipesPage /></Protected>} />
        <Route path="/finance" element={<Protected><FinancePage /></Protected>} />
        <Route path="/pos" element={<Protected><PosPage /></Protected>} />
      </Routes>
    </div>
  );
}
