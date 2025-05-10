import { PropsWithChildren } from 'react';
import { Link } from 'react-router';
import '@/styles/Layout.css';

export default function Layout({ children }: PropsWithChildren) {
  return (
    <div className="layout">
      <nav className="navbar">
        <Link to={'/products'}><div className="logo">Online store</div></Link>
        <ul className="nav-links">
          <li><Link to="/products">Products</Link></li>
          <li><Link to="/cart">Cart</Link></li>
          <li><Link to="/payments">Payments</Link></li>
        </ul>
      </nav>
      <main className="content">
        {children}
      </main>
    </div>
  );
}
