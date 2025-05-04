package main

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo/v4"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"src/controllers"
	"src/models"
)

func connectToDb() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("app.db"), &gorm.Config{})
	if err != nil {
		panic("Error while establishing connection to database")
	}
	db.AutoMigrate(&models.Product{})
	return db
}

func setupProductRoutes(e *echo.Echo, db *gorm.DB) {
	e.GET("/products", getAllProducts(db))
	e.GET("/products/:id", getProductByID(db))
	e.POST("/products", createProduct(db))
	e.PUT("/products/:id", updateProduct(db))
}

// GET /products
func getAllProducts(db *gorm.DB) echo.HandlerFunc {
	return func(c echo.Context) error {
		products, err := controllers.GetAllProducts(db)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}
		return c.JSON(http.StatusOK, products)
	}
}

// GET /products/:id
func getProductByID(db *gorm.DB) echo.HandlerFunc {
	return func(c echo.Context) error {
		id, err := strconv.Atoi(c.Param("id"))
		if err != nil {
			return c.String(http.StatusBadRequest, "Invalid ID")
		}
		product, err := controllers.GetProductByID(db, uint(id))
		if err != nil {
			return c.String(http.StatusNotFound, "Product not found")
		}
		return c.JSON(http.StatusOK, product)
	}
}

// POST /products
func createProduct(db *gorm.DB) echo.HandlerFunc {
	return func(c echo.Context) error {
		var newProduct models.Product
		if err := c.Bind(&newProduct); err != nil {
			return c.String(http.StatusBadRequest, "Invalid input")
		}
		if err := controllers.CreateProduct(db, &newProduct); err != nil {
			return c.String(http.StatusInternalServerError, "Failed to create product")
		}
		return c.JSON(http.StatusCreated, newProduct)
	}
}

// PUT /products/:id
func updateProduct(db *gorm.DB) echo.HandlerFunc {
	return func(c echo.Context) error {
		id, err := strconv.Atoi(c.Param("id"))
		if err != nil {
			return c.String(http.StatusBadRequest, "Invalid ID")
		}

		var updatedProduct models.Product
		if err := c.Bind(&updatedProduct); err != nil {
			return c.String(http.StatusBadRequest, "Invalid input")
		}

		if err := controllers.UpdateProduct(db, uint(id), updatedProduct); err != nil {
			return c.String(http.StatusNotFound, "Product not found or failed to update")
		}
		return c.JSON(http.StatusOK, updatedProduct)
	}
}

func main() {
	e := echo.New()
	db := connectToDb()
	setupProductRoutes(e, db)

	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})

	e.Logger.Fatal(e.Start(":1323"))
}
