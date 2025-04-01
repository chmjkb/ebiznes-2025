package models

import play.api.libs.json._

case class Cart(id: Int, var name: String, var content: List[Product])

object Cart {
  implicit val productFormat: OFormat[Product] = Json.format[Product]
  implicit val cartFormat: OFormat[Cart] = Json.format[Cart]
}
