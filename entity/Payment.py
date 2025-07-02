from datetime import date

class Payment:
    def __init__(self, payment_id=None, student_id=None, amount=None, payment_date=None):
        self.payment_id = payment_id
        self.student_id = student_id
        self.amount = amount
        self.payment_date = payment_date if payment_date else date.today()

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Student ID: {self.student_id}, Amount: {self.amount}, Date: {self.payment_date}"