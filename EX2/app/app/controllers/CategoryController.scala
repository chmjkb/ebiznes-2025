package controllers

import models._
import javax.inject._
import scala.collection.mutable
import play.api._
import play.api.mvc._
import play.api.libs.json._

@Singleton
class CategoryController @Inject() (
    val controllerComponents: ControllerComponents
) extends BaseController {

  var categories: mutable.ListBuffer[Category] = mutable.ListBuffer(
    Category(1, "groceries", "Edibles")
  )

  def readAll() = Action { implicit request: Request[AnyContent] =>
    Ok(Json.toJson(categories))
  }

  def readById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(categoryId) =>
        categories.find(_.id == categoryId) match {
          case Some(category) => Ok(Json.toJson(category))
          case None =>
            NotFound(
              Json.obj("error" -> s"Category with id: $id was not found!")
            )
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }

  def deleteById(id: String) = Action { implicit request: Request[AnyContent] =>
    id.toIntOption match {
      case Some(categoryId) =>
        if (categories.exists(_.id == categoryId)) {
          categories = categories.filterNot(_.id == categoryId)
          Ok(
            Json.obj(
              "message" -> s"Category with id: $id has been deleted successfully."
            )
          )
        } else {
          NotFound(Json.obj("error" -> s"Category with id: $id was not found!"))
        }
      case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
    }
  }

  def create() = Action(parse.json) { implicit request: Request[JsValue] =>
    request.body
      .validate[Category]
      .fold(
        errors => {
          BadRequest(
            Json.obj(
              "error" -> "Invalid category data",
              "details" -> JsError.toJson(errors)
            )
          )
        },
        category => {
          // Check if category with the same ID already exists
          if (categories.exists(_.id == category.id)) {
            Conflict(
              Json.obj(
                "error" -> s"Category with id: ${category.id} already exists!"
              )
            )
          } else {
            // Add the new category
            categories += category
            Created(Json.toJson(category)) // Return the created category
          }
        }
      )
  }

  def update(id: String) = Action(parse.json) {
    implicit request: Request[JsValue] =>
      id.toIntOption match {
        case Some(categoryId) =>
          categories.find(_.id == categoryId) match {
            case Some(existingCategory) =>
              // Mutate existing category properties based on the JSON request
              (request.body \ "name")
                .asOpt[String]
                .foreach(existingCategory.name = _)
              (request.body \ "description")
                .asOpt[String]
                .foreach(existingCategory.description = _)

              Ok(
                Json.obj(
                  "message" -> "Category updated",
                  "category" -> Json.toJson(existingCategory)
                )
              )

            case None =>
              NotFound(Json.obj("error" -> s"Category with id: $id not found!"))
          }
        case None => BadRequest(Json.obj("error" -> "Invalid ID format!"))
      }
  }

}
