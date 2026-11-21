# Found Errors

1. SQL injection vulerability in repository.py lines 16, 26 changed to use parameterized queries.
2. Stock is decremented before payment in checkout.py, changed to attempt payment first, then update stock after a success. Reordered code to fix logic error.
3. Checkout.py does not cancel order on error, applies payment and updates database regardless. Added return statements on errors.
4. Checkout.py checks for cart.user_id but does nothing with result. lines 18-26 now fail early to catch inconsistency.
5. Shipping does nothing? Removed.
6. f
7. g
8. h
