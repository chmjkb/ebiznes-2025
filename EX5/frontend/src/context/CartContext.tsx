import { ProductI } from '@/types/products';
import { createContext, PropsWithChildren, useContext, useState } from 'react';

type CartContextType = {
  cart: ProductI[];
  cartValue: number;
  addToCart: (item: ProductI) => void;
  removeFromCart: (idx: number) => void 
  clearCart: () => void;
};

const CartContext = createContext<CartContextType | null>(null);

export const useCartContext = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useListContext must be used within a ListProvider');
  }
  return context;
};


export const CartProvider = ({ children }: PropsWithChildren) => {
  // For sake of simplicity we are just using a list to store the cart, 
  // we're not storing it on the backend
  const [cart, setCart] = useState<ProductI[]>([]);
  const [cartValue, setCartValue] = useState<number>(0);

  const addToCart = (item: ProductI) => {
    setCart((prev) => [...prev, item]);
    setCartValue((prev) => parseFloat((prev + item.price).toFixed(2)));
  };

  const removeFromCart = (idx: number) => {
    setCartValue((prev) => parseFloat((prev - cart[idx].price).toFixed(2)));
    setCart((prev) => prev.filter((_, index) => index !== idx));
  };

  const clearCart = () => {
    setCart([]);
    setCartValue(0);
  }

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, cartValue, clearCart }}>
      {children}
    </CartContext.Provider>
  );
};
