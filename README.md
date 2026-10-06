# Automated Login Test Suite: Sauce Demo

**Internship:** Codecraft Infotech, Quality Assurance
**Task:** 03, Automated Login Test for a Web Application
**Application under test:** Sauce Demo (https://www.saucedemo.com), a public demo site
**Tools:** Python, Selenium WebDriver, pytest

## Objective
Automate login testing with positive cases (valid credentials) and negative cases (invalid credentials, empty fields).

## Test Cases

| ID | Type | Scenario | Expected Result |
|---|---|---|---|
| TC01 | Positive | Login with valid credentials | Inventory page opens with the "Products" heading |
| TC02 | Positive | Log out after login | Returns to the login page |
| TC03 | Negative | Valid username, wrong password | Credentials mismatch error |
| TC04 | Negative | Invalid username, valid password | Credentials mismatch error |
| TC05 | Negative | Invalid username and password | Credentials mismatch error |
| TC06 | Negative | Both fields empty | "Username is required" |
| TC07 | Negative | Empty username, valid password | "Username is required" |
| TC08 | Negative | Valid username, empty password | "Password is required" |
| TC09 | Negative | Locked-out user | "User has been locked out" error |
| TC10 | Negative | Open inventory page without logging in | Access blocked with an error message |

## How to Run
```
pip install -r requirements.txt
pytest -v
```
Chrome must be installed. Selenium downloads the matching driver automatically.

## Approach
- A `driver` fixture starts a clean Chrome session for every test and closes it afterwards, so tests are independent.
- A reusable `login()` helper keeps each test short.
- Negative cases use `pytest.mark.parametrize`, so one test function covers several input combinations.
- Assertions check both the error message and that the user did not reach the inventory page.

## Results
   All 10 tests passed (10 passed in 62.26s).
   Screenshot: pytest_results.png