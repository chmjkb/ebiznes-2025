package models

import play.api.libs.json._
import play.api.http.Writeable
import org.apache.pekko.util.ByteString

case class Product(id: Int, var name: String, var price: Int) {}

object Product {
  implicit val productFormat: OFormat[Product] = Json.format[Product]
}
