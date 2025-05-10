import { StrictMode } from 'react'
import { Routes, Route } from 'react-router'
import { BrowserRouter } from 'react-router'
import Cart from '@/components/Cart.tsx'
import Payments from '@/components/Payment'
import Layout from '@/components/Layout.tsx'
import ProductList from '@/components/ProductList.tsx'
import { CartProvider } from '@/context/CartContext'

export default function App() {
  return (
    <BrowserRouter>
      <StrictMode>
        <Layout>
          <CartProvider>
            <Routes>
              <Route path={'/'} element={<ProductList />} />
              <Route path={'/products'} element={<ProductList />} />
              <Route path={'/cart'} element={<Cart />} />
              <Route path={'/payments'} element={<Payments />} />
            </Routes>
          </CartProvider>
        </Layout>
      </StrictMode>,
    </BrowserRouter>
  )
}
