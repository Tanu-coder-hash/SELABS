
# Lab 5 – Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding errors and formatting issues. It improves software quality by detecting problems early in development. It also makes programs easier to maintain, understand and secure.

## 2. What is the difference between Pylint, Bandit and Flake8?

Pylint focuses on code quality, naming conventions, documentation and potential programming errors. Bandit identifies security vulnerabilities such as SQL injection, unsafe code execution and insecure file handling. Flake8 checks Python code formatting and compliance with PEP 8 guidelines. Using all three tools provides a more complete analysis of the program.

## 3. What were the major issues identified in your program, and how did you fix them?

The original car rental program contained SQL injection vulnerabilities, unsafe use of exec(), weak SHA-1 hashing, insecure temporary-file handling and hardcoded administrator credentials. It also contained mutable default arguments, broad exception handling and formatting issues. I fixed these by using parameterized SQL queries, removing unsafe code execution, implementing SHA-256 hashing, using secure temporary files, and storing administrator credentials in environment variables. I also improved input validation, function naming and code documentation.

## 4. How did static analysis improve your program?

Static analysis helped identify issues that were difficult to notice through normal program execution. Bandit helped improve security, Pylint improved code quality, and Flake8 helped maintain consistent formatting. After fixing the reported issues, the program achieved a Pylint score of 10.00/10, zero Bandit findings and zero Flake8 violations. This experiment demonstrated the importance of regularly using static analysis tools during software development.
