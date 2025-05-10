import axios from 'axios'
import { useEffect, useState } from 'react'
import { ProductI } from '@/types/products'
import Product from '@/components/Product'

export default function ProductList() {
  const [products, setProducts] = useState<ProductI[]>([])

  useEffect(() => {
    // If products are not passed as props, fetch them from the backend
    const getProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8080/products")
        setProducts(response.data)
      } catch (e) {
        console.error("Error when fetching products!", e)
      }
    }
    getProducts()
  }, [])

  return (
    <>
      {products.map(product => (
        <Product
          key={product.id}
          id={product.id}
          name={product.name}
          description={product.description}
          price={product.price}
        />
      ))}
    </>
  )
}
