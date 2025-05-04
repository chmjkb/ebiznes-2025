package controllers

import (
	"gorm.io/gorm"
	"src/models"
)

func GetAllProducts(db *gorm.DB) ([]models.Product, error) {
	var products []models.Product
	result := db.Find(&products)
	return products, result.Error
}

func GetProductByID(db *gorm.DB, id uint) (*models.Product, error) {
	var product models.Product
	result := db.First(&product, id)
	if result.Error != nil {
		return nil, result.Error
	}
	return &product, nil
}

func CreateProduct(db *gorm.DB, product *models.Product) error {
	return db.Create(product).Error
}

func UpdateProduct(db *gorm.DB, id uint, updated models.Product) error {
	var product models.Product
	if err := db.First(&product, id).Error; err != nil {
		return err
	}
	product.Name = updated.Name
	product.Price = updated.Price
	return db.Save(&product).Error
}
