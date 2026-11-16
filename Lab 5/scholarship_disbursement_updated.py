"""
Scholarship disbursement module.
Handles granting and disbursing student scholarships using an in-memory
database.
"""
import sqlite3
import logging

# Set up logging for tracking events and errors
logging.basicConfig(level=logging.INFO)


class ScholarshipManager:
    """Manages scholarship data and disbursement tracking."""

    def __init__(self):
        """Initializes the in-memory database and total tracker."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE awards ("
            "id INTEGER PRIMARY KEY, "
            "student TEXT, "
            "scheme TEXT, "
            "amount INTEGER, "
            "disbursed INTEGER)"
        )
        self.disbursed_total = 0

    def grant(self, student, scheme, amount, audit=None):
        """Grants a scholarship to a student and updates the audit log."""
        if audit is None:
            audit = []

        self.conn.execute(
            "INSERT INTO awards (student, scheme, amount, disbursed) "
            "VALUES (?, ?, ?, 0)",
            (student, scheme, amount)
        )
        audit.append(student)
        return audit

    def disburse(self, award_id):
        """Marks a scholarship as disbursed and updates the total."""
        row = self.conn.execute(
            "SELECT amount FROM awards WHERE id = ?",
            (award_id,)
        ).fetchone()

        if row:
            self.conn.execute(
                "UPDATE awards SET disbursed = 1 WHERE id = ?",
                (award_id,)
            )
            self.disbursed_total += row[0]
            return row[0]

        return None

    def archive(self):
        """Archives the current awards."""
        # Instead of calling the operating system shell to print a message,
        # we use Python's native logging library.
        logging.info("Archiving awards...")

    def by_scheme_count(self, scheme):
        """Returns the total number of awards for a given scheme."""
        if scheme is None:
            return 0
        return self.conn.execute(
            "SELECT COUNT(*) FROM awards WHERE scheme = ?",
            (scheme,)
        ).fetchone()[0]


def main():
    """Main execution block."""
    manager = ScholarshipManager()
    manager.grant("Ishaan", "Merit", 50000)
    manager.grant("Divya", "Need-based", 75000)

    print(manager.disburse(1), manager.disburse(9))
    print(manager.by_scheme_count("Merit"), manager.disbursed_total)

    manager.archive()


if __name__ == "__main__":
    main()
