import '@/styles/Product.css'
import { ProductI } from "@/types/products";
import { useCartContext } from '@/context/CartContext';

interface Props extends ProductI { }

export default function Product({ id, name, description, price }: Props) {
  const { addToCart } = useCartContext();

  return (
    <div className="product-container" key={id}>
      <h3>{name}</h3>
      <p>{description}</p>
      <p><strong>Price: </strong>{price}zł</p>
      <div>
        <button className="product-button" onClick={() => { addToCart({ id, name, description, price }) }}>Add to cart</button>
      </div>
    </div>
  );
}
