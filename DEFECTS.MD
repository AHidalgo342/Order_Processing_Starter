# Found Errors

1. SQL injection vulerability in repository.py lines 16, 26 changed to use parameterized queries.
2. Stock is decremented before payment in checkout.py, changed to attempt payment first, then update stock after a success. Reordered code to fix logic error.
3. Checkout.py does not cancel order on error, applies payment and updates database regardless. Added return statements on errors.
4. Checkout.py checks for cart.user_id but does nothing with result. lines 18-26 now fail early to catch inconsistency.
5. Monetary calculations should not be done using floating point numbers, but instead with a package that can handle the correct precision needed for currency. Changed to use the Deciaml package for higher precision.
6. cart.py no add_item negative quantity check. possible to grab negative items. Added lines 14-16.
7. cart.py no remove_item negative quantity check. possible to remove negative items. Added lines 32-34.
8. Checkout.py Reorder also fixed timing error where payment delay could cause the repo to incorrectly update quantities before a decline was detected.
