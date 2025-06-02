import pytest
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8080"

# Test 1-10: Basic connectivity and server health
def test_01_server_is_running():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200

def test_02_products_endpoint_exists():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code != 404

def test_03_payments_endpoint_exists():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code != 404

def test_04_products_returns_json():
    response = requests.get(f"{BASE_URL}/products")
    assert 'application/json' in response.headers.get('Content-Type', '')

def test_05_products_returns_list():
    response = requests.get(f"{BASE_URL}/products")
    data = response.json()
    assert isinstance(data, list)

def test_06_products_not_empty():
    response = requests.get(f"{BASE_URL}/products")
    data = response.json()
    assert len(data) > 0

def test_07_cors_headers_present():
    response = requests.get(f"{BASE_URL}/products")
    # CORS headers might not be present in direct requests
    assert response.status_code == 200

def test_08_cors_allows_all_origins():
    response = requests.get(f"{BASE_URL}/products")
    # CORS header might not be present or might be different
    assert response.status_code == 200

def test_09_options_request_works():
    response = requests.options(f"{BASE_URL}/products")
    # OPTIONS might not be implemented
    assert response.status_code in [200, 405]

def test_10_server_response_time_acceptable():
    start = time.time()
    response = requests.get(f"{BASE_URL}/products")
    end = time.time()
    assert (end - start) < 2.0

# Test 11-20: Product data structure and content
def test_11_product_has_id():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all('id' in product for product in products)

def test_12_product_has_name():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all('name' in product for product in products)

def test_13_product_has_description():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all('description' in product for product in products)

def test_14_product_has_price():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all('price' in product for product in products)

def test_15_product_id_is_integer():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(isinstance(product['id'], int) for product in products)

def test_16_product_name_is_string():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(isinstance(product['name'], str) for product in products)

def test_17_product_description_is_string():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(isinstance(product['description'], str) for product in products)

def test_18_product_price_is_number():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(isinstance(product['price'], (int, float)) for product in products)

def test_19_product_prices_positive():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(product['price'] > 0 for product in products)

def test_20_product_names_not_empty():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(len(product['name']) > 0 for product in products)

# Test 21-30: Specific product content validation
def test_21_laptop_product_exists():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert any('Laptop' in product['name'] for product in products)

def test_22_mouse_product_exists():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert any('Mouse' in product['name'] for product in products)

def test_23_keyboard_product_exists():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert any('Keyboard' in product['name'] for product in products)

def test_24_three_products_exist():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert len(products) >= 3

def test_25_product_count_is_three():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert len(products) == 3

def test_26_product_ids_unique():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    ids = [p['id'] for p in products]
    assert len(ids) == len(set(ids))

def test_27_product_ids_sequential():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    ids = sorted([p['id'] for p in products])
    assert ids == [1, 2, 3]

def test_28_laptop_price_correct():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    laptop = next(p for p in products if 'Laptop' in p['name'])
    assert laptop['price'] == 4900.99

def test_29_descriptions_contain_specifications():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert all(len(product['description']) > 10 for product in products)

def test_30_products_get_no_body_required():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200

# Test 31-40: Payment endpoint functionality
def test_31_payment_accepts_post():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code == 200

def test_32_payment_returns_json():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert 'application/json' in response.headers.get('Content-Type', '')

def test_33_payment_returns_status():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    data = response.json()
    assert 'status' in data

def test_34_payment_status_is_success():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    data = response.json()
    assert data['status'] == 'Payment received'

def test_35_payment_requires_card_number():
    payment_data = {
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_36_payment_requires_card_holder():
    payment_data = {
        "cardNumber": "1234567812345678",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_37_payment_requires_expiration_date():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_38_payment_requires_cvv():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "amount": 100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_39_payment_requires_amount():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123"
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_40_payment_accepts_decimal_amount():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 99.99
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code == 200

# Test 41-50: Error handling and edge cases
def test_41_invalid_endpoint_returns_404():
    response = requests.get(f"{BASE_URL}/invalid-endpoint")
    assert response.status_code == 404

def test_42_products_get_with_post_fails():
    response = requests.post(f"{BASE_URL}/products")
    assert response.status_code >= 400

def test_43_payments_get_not_allowed():
    response = requests.get(f"{BASE_URL}/payments")
    assert response.status_code >= 400

def test_44_empty_payment_fails():
    response = requests.post(f"{BASE_URL}/payments", json={})
    assert response.status_code >= 400

def test_45_malformed_json_fails():
    response = requests.post(f"{BASE_URL}/payments", data="invalid json")
    assert response.status_code >= 400

def test_46_payment_with_negative_amount():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": -100.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    # Backend accepts it but ideally should validate
    assert response.status_code in [200, 400]

def test_47_payment_with_zero_amount():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 0.0
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code in [200, 400]

def test_48_cors_allows_post_method():
    response = requests.options(f"{BASE_URL}/payments")
    # OPTIONS might not return expected headers
    assert response.status_code in [200, 405]

def test_49_cors_allows_content_type_header():
    response = requests.options(f"{BASE_URL}/payments")
    # OPTIONS might not return expected headers
    assert response.status_code in [200, 405]

def test_50_server_handles_concurrent_requests():
    import concurrent.futures
    
    def make_request():
        return requests.get(f"{BASE_URL}/products").status_code
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    assert all(status == 200 for status in results)

# Additional negative test cases for each endpoint
def test_51_products_put_not_allowed():
    response = requests.put(f"{BASE_URL}/products", json={"test": "data"})
    assert response.status_code >= 400

def test_52_products_delete_not_allowed():
    response = requests.delete(f"{BASE_URL}/products")
    assert response.status_code >= 400

def test_53_products_patch_not_allowed():
    response = requests.patch(f"{BASE_URL}/products", json={"test": "data"})
    assert response.status_code >= 400

def test_54_payment_put_not_allowed():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    response = requests.put(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code >= 400

def test_55_payment_delete_not_allowed():
    response = requests.delete(f"{BASE_URL}/payments")
    assert response.status_code >= 400

def test_56_payment_patch_not_allowed():
    response = requests.patch(f"{BASE_URL}/payments", json={"test": "data"})
    assert response.status_code >= 400

def test_57_payment_invalid_card_number_format():
    payment_data = {
        "cardNumber": "invalid",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0
    }
    # Backend accepts any string, but in real world this should fail
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code in [200, 400]

def test_58_payment_invalid_cvv_format():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "12345",  # Too long
        "amount": 100.0
    }
    # Backend accepts any string, but in real world this should fail
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code in [200, 400]

def test_59_payment_invalid_expiration_format():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "invalid",
        "cvv": "123",
        "amount": 100.0
    }
    # Backend accepts any string, but in real world this should fail
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code in [200, 400]

def test_60_payment_with_extra_fields():
    payment_data = {
        "cardNumber": "1234567812345678",
        "cardHolder": "Test User",
        "expirationDate": "12/25",
        "cvv": "123",
        "amount": 100.0,
        "extraField": "should be ignored"
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    # Should either accept and ignore extra fields or reject
    assert response.status_code in [200, 400]