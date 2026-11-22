import os
from decimal import Decimal

from cart import ShoppingCart
from checkout import CheckoutService
from payments import FakePaymentGateway
from repository import StoreRepository
from setup_db import initialize


def test_seed_product(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    assert StoreRepository(str(db)).get_product('MOU-01').name == 'Wireless mouse'

def test_cart_adds_valid_item(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    assert cart.add_item('USB-01', 2)
    assert len(cart.lines) == 1

def test_currency_precision(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.add_item("USB-01", 2)
    assert cart.total() == Decimal("19.98")

def test_cart_add_rejects_negative(tmp_path):
    db = tmp_path /'test.db'
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.add_item("USB-01", -2) == False

def test_cart_add_rejects_zero(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.add_item("USB-01", 0) == False

def test_cart_remove_rejects_negative(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.remove_item("USB-01", -2) == False

def test_cart_add_rejects_invalid(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.add_item("Foo", -2) == False
    assert len(cart.lines) == 0

def test_cart_remove_rejects_invalid(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    cart = ShoppingCart("student", StoreRepository(str(db)))
    assert cart.remove_item("Foo", -2) == False
    assert len(cart.lines) == 0

def test_checkout_decline_delay(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart("student", repo)
    cart.add_item("MOU-01", 2)
    CheckoutService(repo, FakePaymentGateway(False, 1)).checkout(
        cart, "TEST_TOKEN", "decline_test-1"
    )
    assert repo.get_product('MOU-01').stock == 20

def test_checkout_decline_empty(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart("student", repo)
    result = CheckoutService(repo, FakePaymentGateway()).checkout(
        cart, "TEST_TOKEN", "decline_test-2"
    )
    assert result.status == 'empty'

def test_checkout_decline_card(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart("student", repo)
    cart.add_item("MOU-01", 2)
    result = CheckoutService(repo, FakePaymentGateway(False)).checkout(
        cart, "TEST_TOKEN", "decline_test-3"
    )
    assert result.status == "declined"

def test_checkout_decline_limit(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart("student", repo)
    cart.add_item("LAP-01", 2)
    result = CheckoutService(repo, FakePaymentGateway()).checkout(
        cart, "TEST_TOKEN", "decline_test-4"
    )
    assert result.status == "Large Order"

def test_checkout_decline_null_cart(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart(None, repo)
    cart.add_item("USB-01", 2)
    result = CheckoutService(repo, FakePaymentGateway()).checkout(
        cart, "TEST_TOKEN", "decline_test-5"
    )
    assert result.status == "No cart id"

def test_cart_add_when_no_stock(tmp_path):
    db = tmp_path / "test.db"
    initialize(str(db))
    repo = StoreRepository(str(db))
    cart = ShoppingCart("student", repo)
    cart.add_item("MOU-01", 20)
    CheckoutService(repo, FakePaymentGateway()).checkout(
        cart, "TEST_TOKEN", "decline_test-5"
    )
    assert cart.add_item("MOU-01", 1) == False