from entity.Payment import Payment
from dao.interfaces.AllInterfaces import IPaymentService
from util.DBConnUtil import DBConnUtil
from util.DBPropertyUtil import DBPropertyUtil
from util.DBConnUtil import DBConnUtil
from exception.CustomExceptions import PaymentValidationException, StudentNotFoundException
from datetime import date


class PaymentDAO(IPaymentService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(DBPropertyUtil.get_connection_string('resources/db.properties'))

    def get_payment_by_id(self, payment_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Payments WHERE payment_id = %s", (payment_id,))
            payment_data = cursor.fetchone()

            if not payment_data:
                return None

            payment = Payment(
                payment_data['payment_id'],
                payment_data['student_id'],
                payment_data['amount'],
                payment_data['payment_date']
            )
            return payment
        except Exception as e:
            print(f"Error getting payment by ID: {e}")
            raise
        finally:
            cursor.close()

    def get_payments_by_student(self, student_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Payments WHERE student_id = %s", (student_id,))
            payments = []

            for payment_data in cursor.fetchall():
                payment = Payment(
                    payment_data['payment_id'],
                    payment_data['student_id'],
                    payment_data['amount'],
                    payment_data['payment_date']
                )
                payments.append(payment)

            return payments
        except Exception as e:
            print(f"Error getting payments by student: {e}")
            raise
        finally:
            cursor.close()

    def get_all_payments(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Payments")
            payments = []

            for payment_data in cursor.fetchall():
                payment = Payment(
                    payment_data['payment_id'],
                    payment_data['student_id'],
                    payment_data['amount'],
                    payment_data['payment_date']
                )
                payments.append(payment)

            return payments
        except Exception as e:
            print(f"Error getting all payments: {e}")
            raise
        finally:
            cursor.close()

    def record_payment(self, payment):
        try:
            cursor = self.connection.cursor()

            # Validate payment data
            if not all([payment.student_id, payment.amount, payment.payment_date]):
                raise PaymentValidationException("Student ID, amount, and payment date are required")

            if payment.amount <= 0:
                raise PaymentValidationException("Payment amount must be positive")

            # Check if student exists
            student_dao = StudentDAO()
            if not student_dao.get_student_by_id(payment.student_id):
                raise StudentNotFoundException(f"Student with ID {payment.student_id} not found")

            cursor.execute(
                "INSERT INTO Payments (student_id, amount, payment_date) VALUES (%s, %s, %s)",
                (payment.student_id, payment.amount, payment.payment_date)
            )
            self.connection.commit()
            payment.payment_id = cursor.lastrowid
            return payment
        except Exception as e:
            self.connection.rollback()
            print(f"Error recording payment: {e}")
            raise
        finally:
            cursor.close()

    def update_payment(self, payment):
        try:
            cursor = self.connection.cursor()

            # Check if payment exists
            if not self.get_payment_by_id(payment.payment_id):
                return None

            cursor.execute(
                "UPDATE Payments SET student_id = %s, amount = %s, payment_date = %s WHERE payment_id = %s",
                (payment.student_id, payment.amount, payment.payment_date, payment.payment_id)
            )
            self.connection.commit()
            return payment
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating payment: {e}")
            raise
        finally:
            cursor.close()

    def delete_payment(self, payment_id):
        try:
            cursor = self.connection.cursor()

            # Check if payment exists
            if not self.get_payment_by_id(payment_id):
                return False

            cursor.execute("DELETE FROM Payments WHERE payment_id = %s", (payment_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting payment: {e}")
            raise
        finally:
            cursor.close()