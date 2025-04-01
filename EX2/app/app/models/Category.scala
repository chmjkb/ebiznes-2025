package models

import play.api.libs.json._

case class Category(id: Int, var name: String, var description: String)

object Category {
  implicit val categoryFormat: OFormat[Category] = Json.format[Category]
}