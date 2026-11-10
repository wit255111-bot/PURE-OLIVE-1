"""
Verification script for PURE & OLIVE Flask Application
Tests all key routes and APIs
"""
from app import app
import json

def run_tests():
    client = app.test_client()
    passed = 0
    total = 0

    def check(name, res, expected_code=200):
        nonlocal passed, total
        total += 1
        if res.status_code == expected_code:
            print(f"✅ PASS: {name} ({res.status_code})")
            passed += 1
        else:
            print(f"❌ FAIL: {name} (Got {res.status_code}, expected {expected_code})")

    print("--- Starting Route Verification ---")
    
    # 1. Home
    check("Home Page (/)", client.get('/'))

    # 2. Products Catalog
    check("Products Catalog (/products)", client.get('/products'))
    check("Products Skincare Filter (/products?category=skincare)", client.get('/products?category=skincare'))
    check("Products Search (/products?q=serum)", client.get('/products?q=serum'))

    # 3. Product Detail (id=1)
    check("Product Detail (/product/1)", client.get('/product/1'))

    # 4. Skin Quiz
    check("Skin Routine Quiz (/routine-quiz)", client.get('/routine-quiz'))

    # 5. Quiz Recommendation API
    quiz_payload = {
        'skin_type': 'combination',
        'concern': 'acne',
        'style': 'complete'
    }
    res_quiz = client.post('/api/quiz-recommend', json=quiz_payload)
    check("Quiz Recommend API (/api/quiz-recommend)", res_quiz)
    quiz_data = json.loads(res_quiz.data)
    print("   Bundle items returned:", len(quiz_data.get('bundle_items', [])))

    # 6. Cart Page
    check("Cart Page (/cart)", client.get('/cart'))

    # 7. Checkout API
    order_payload = {
        'customer_name': 'ทดสอบ ระบบ',
        'customer_phone': '089-999-9999',
        'customer_email': 'test@pureolive.com',
        'customer_address': '99/9 ถ.สุขุมวิท กรุงเทพฯ 10110',
        'payment_method': 'promptpay',
        'coupon_code': 'CLEAN10',
        'items': [
            {'id': 1, 'name': 'เจลล้างหน้า', 'price': 390.0, 'quantity': 1},
            {'id': 3, 'name': 'เซรั่มสควาเลน', 'price': 690.0, 'quantity': 1}
        ]
    }
    res_checkout = client.post('/api/checkout', json=order_payload)
    check("Checkout API (/api/checkout)", res_checkout)
    checkout_data = json.loads(res_checkout.data)
    order_number = checkout_data.get('order_number')
    print("   Created Order Number:", order_number)

    # 8. Order Success Page
    if order_number:
        check(f"Order Success Page (/order-success/{order_number})", client.get(f'/order-success/{order_number}'))

    # 9. Tips
    check("Tips Page (/tips)", client.get('/tips'))

    # 10. Admin Dashboard
    check("Admin Dashboard (/admin)", client.get('/admin'))

    print(f"\nVerification Results: {passed}/{total} Passed")
    return passed == total

if __name__ == '__main__':
    run_tests()
