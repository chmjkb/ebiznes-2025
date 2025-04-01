package controllers

import models._
import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._
import scala.collection.mutable

@Singleton
class ProductController @Inject() (
    val controllerComponents: ControllerComponents
) extends BaseController {

  var products: mutable.ListBuffer[Product] = mutable.ListBuffer(
    Product(1, "Laptop", 1200),
    Product(2, "Smartphone", 800),
    Product(3, "Headphones", 150),
    Product(4, "Monitor", 300),
    Product(5, "Keyboard", 100)
  )

  def readAll() = Action { implicit request: Request[AnyContent] =>
    Ok(Json.toJson(products))
  }

  /** Get product by ID */
  def readById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(productId) =>
        products.find(_.id == productId) match {
          case Some(product) => Ok(Json.toJson(product))
          case None =>
            NotFound(
              Json.obj("error" -> s"Product with id: $id was not found!")
            )
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }

  def deleteById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(productId) =>
        products.find(_.id == productId) match {
          case Some(_) =>
            products =
              products.filterNot(_.id == productId) // Remove the product
            Ok(
              Json.obj(
                "message" -> s"Product with id: $id has been deleted successfully."
              )
            )
          case None =>
            NotFound(
              Json.obj("error" -> s"Product with id: $id was not found!")
            )
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }

  def create() = Action { implicit request: Request[AnyContent] =>
    request.body.asJson match {
      case Some(json) =>
        json.validate[Product] match {
          case JsSuccess(product, _) =>
            if (products.exists(_.id == product.id)) {
              Conflict(
                Json.obj(
                  "error" -> s"Product with id: ${product.id} already exists!"
                )
              )
            } else {
              products.addOne(product)
              Created(
                Json.toJson(product)
              ) // Return the created product as JSON
            }
          case JsError(errors) =>
            BadRequest(
              Json.obj(
                "error" -> "Invalid JSON format",
                "details" -> errors.toString()
              )
            )
        }
      case None =>
        NotAcceptable(Json.obj("error" -> "The request body was invalid!"))
    }
  }

  def update(id: String) = Action(parse.json) {
    implicit request: Request[JsValue] =>
      id.toIntOption match {
        case Some(productId) =>
          products.find(_.id == productId) match {
            case Some(product) =>
              (request.body \ "name").asOpt[String].foreach(product.name = _)
              (request.body \ "price").asOpt[Int].foreach(product.price = _)

              Ok(
                Json.obj(
                  "message" -> "Product updated",
                  "product" -> Json.toJson(product)
                )
              )

            case None =>
              NotFound(Json.obj("error" -> s"Product with id: $id not found!"))
          }
        case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
      }
  }

}
