package controllers

import models._
import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._
import scala.collection.mutable

@Singleton
class CartController @Inject() (
    val controllerComponents: ControllerComponents
) extends BaseController {

  // Mutable collection to hold carts
  var carts: mutable.ListBuffer[Cart] = mutable.ListBuffer(
    Cart(
      1,
      "Shopping Cart",
      List(Product(1, "Laptop", 1200), Product(2, "Smartphone", 800))
    ),
    Cart(
      2,
      "Grocery Cart",
      List(Product(3, "Apple", 1), Product(4, "Banana", 1))
    )
  )

  def readAll() = Action { implicit request: Request[AnyContent] =>
    Ok(Json.toJson(carts))
  }

  def readById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(cartId) =>
        carts.find(_.id == cartId) match {
          case Some(cart) => Ok(Json.toJson(cart))
          case None =>
            NotFound(Json.obj("error" -> s"Cart with id: $id was not found!"))
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }

  def create() = Action(parse.json) { implicit request: Request[JsValue] =>
    request.body
      .validate[Cart]
      .fold(
        errors => {
          BadRequest(
            Json.obj(
              "error" -> "Invalid cart data",
              "details" -> JsError.toJson(errors)
            )
          )
        },
        cart => {
          // Check if cart with the same ID already exists
          if (carts.exists(_.id == cart.id)) {
            Conflict(
              Json.obj("error" -> s"Cart with id: ${cart.id} already exists!")
            )
          } else {
            // Add the new cart
            carts += cart
            Created(Json.toJson(cart)) // Return the created cart
          }
        }
      )
  }

  def update(id: String) = Action(parse.json) {
    implicit request: Request[JsValue] =>
      id.toIntOption match {
        case Some(cartId) =>
          // Find the existing cart by ID
          carts.find(_.id == cartId) match {
            case Some(existingCart) =>
              // Update the name if provided
              (request.body \ "name")
                .asOpt[String]
                .foreach(existingCart.name = _)

              // Update the content if provided
              (request.body \ "content")
                .asOpt[List[Product]]
                .foreach(existingCart.content = _)

              Ok(
                Json.obj(
                  "message" -> "Cart updated",
                  "cart" -> Json.toJson(existingCart)
                )
              )

            case None =>
              NotFound(Json.obj("error" -> s"Cart with id: $id was not found!"))
          }
        case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
      }
  }

  def deleteById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(cartId) =>
        if (carts.exists(_.id == cartId)) {
          carts = carts.filterNot(_.id == cartId)
          Ok(
            Json.obj(
              "message" -> s"Cart with id: $id has been deleted successfully."
            )
          )
        } else {
          NotFound(Json.obj("error" -> s"Cart with id: $id was not found!"))
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }
}
