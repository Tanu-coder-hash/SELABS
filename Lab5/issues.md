
# Lab 5 – Static Code Analysis
## Issue Identification and Resolution

**Program:** car_rental.py

**Tools used:** Pylint, Bandit, Flake8

### Issues identified in the original program

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SQL Injection | Security – Medium | 23, 26 | SQL queries used string formatting and concatenation, allowing malicious input to modify database queries. | Replaced dynamic SQL strings with parameterized queries using placeholders. |
| Unsafe Code Execution | Security – Medium | 52 | The `exec()` function executed dynamically supplied promotional rules, allowing arbitrary code execution. | Removed `exec()` and implemented a validated discount-rate calculation. |
| Weak Hash Algorithm | Security – High | 49 | SHA-1 was used to generate licence hashes and is no longer considered secure for cryptographic use. | Replaced SHA-1 with SHA-256. |
| Insecure Temporary File | Security – Medium | 59 | `tempfile.mktemp()` generated a temporary filename without securely creating the file. | Replaced it with `NamedTemporaryFile()` using secure file creation. |
| Insecure File Permissions | Security – High | 63 | File permissions were set to `0o777`, allowing unrestricted access. | Changed permissions to `0o600`. |
| Hardcoded Admin Credentials | Security – Low | 67 | The administrator password was hardcoded in the source code. | Retrieved the expected password from the `ADMIN_PASSWORD` environment variable. |
| Insecure Random Number Generation | Security – Low | 46 | `random.randint()` was used to generate booking codes. | Replaced it with `secrets.randbelow()`. |
| Mutable Default Argument | Code Quality | 13 | The `features=[]` default argument could be shared between function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Broad Exception Handling | Code Quality | 41–44 | A bare `except` silently ignored all exceptions. | Removed the broad exception handling and explicitly validated car registration and mileage. |
| Missing Input Validation | Logic / Bug | 29–33, 75 | Negative rental rates and invalid date ranges could result in incorrect rental costs. | Added validation for daily rates and rental dates. |
| Naming and Documentation Issues | Code Quality | Multiple | CamelCase function names and missing docstrings reduced readability and maintainability. | Renamed functions using snake_case and added module and function docstrings. |
| Formatting Violations | Style | Multiple | Long lines, missing blank lines and other PEP 8 violations were reported by Flake8. | Reformatted the source code according to PEP 8 conventions. |

### Static Analysis Results

| Tool | Before Fixes | After Fixes |
|---|---|---|
| Pylint | 4.94/10 | 10.00/10 |
| Bandit | 11 findings | 0 findings |
| Flake8 | 24 violations | 0 violations |

### Conclusion

The original car rental program contained security vulnerabilities, code quality issues and formatting violations. The identified problems were corrected using secure coding practices and proper Python conventions. After the modifications, Bandit reported zero security issues, Pylint achieved a score of 10.00/10, and Flake8 reported zero formatting violations.
