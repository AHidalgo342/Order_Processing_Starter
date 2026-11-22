from cart import ShoppingCart
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

# TODO: 1. Prices should be calculated with the correct precision
# TODO: 2. add_item negative quantity should return error
# TODO: 3. add_item 0 quantity should return error
# TODO: 4. remove_item negative quantity should return error
# TODO: 5. cart should not add invalid items
# TODO: 6. cart should not remove invalid items
# TODO: 7. checkout decline with a delay should not affect database
# TODO: 8. checkout should fail with an empty cart
# TODO: 9. checkout should fail when card is declined
# TODO: 10. checkout should fail when over amount limit
# TODO: 11. checkout should fail when cart is null
# TODO: 12. checkout should fail when no stock