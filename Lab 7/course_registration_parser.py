
def format_course_code(code):
    """Formats a valid course code like 'cs 301' as 'CS301'."""
    if not isinstance(code, str):
        return ""

    parts = code.split()

    if len(parts) != 2:
        return ""

    dept, number = parts

    if not dept.isalpha() or not number.isalnum():
        return ""

    return dept.upper() + number


def total_credits(text):
    """Adds comma-separated whole-number credits safely."""
    if not isinstance(text, str) or not text.strip():
        return 0

    try:
        credits = [int(credit.strip()) for credit in text.split(',')]
        if any(credit < 0 for credit in credits):
            return 0
        return sum(credits)
    except ValueError:
        return 0


def parse_student_record(line):
    """Parses 'SRN|name|status' safely into a dictionary."""
    if not isinstance(line, str):
        return {"srn": "", "name": "", "status": ""}

    parts = line.split('|')

    if len(parts) != 3:
        return {"srn": "", "name": "", "status": ""}

    srn, name, status = [part.strip() for part in parts]

    return {
        "srn": srn.upper(),
        "name": name,
        "status": status.lower()
    }


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", parse_student_record(value))


if __name__ == "__main__":
    main()
