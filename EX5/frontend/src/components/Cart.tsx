import '@/styles/Cart.css'
import { useCartContext } from "@/context/CartContext";

export default function Cart() {
  const { cart, removeFromCart } = useCartContext()

  return (
    <div className="cart-container">
      {cart.length === 0 ? (
        <div className="empty-cart">Your cart is empty 🛒</div>
      ) : (
        cart.map((product, idx) => (
          <div className="product-container" key={idx}>
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p><strong>Price: </strong>{product.price}zł</p>
            <div>
              <button
                className="product-button"
                onClick={() => removeFromCart(idx)}
              >
                Remove from cart
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}
