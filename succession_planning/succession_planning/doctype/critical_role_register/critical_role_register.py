# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class CriticalRoleRegister(Document):

    def validate(self):
        self.validate_bench_strength()
        self.validate_vacancy_date()
        self.validate_incumbent_department()

    def validate_bench_strength(self):
        if self.minimum_bench_strength <= 0:
            frappe.throw("Minimum Bench Strength must be greater than 0")

    def validate_vacancy_date(self):
        if self.retirement_or_vacancy_date:
            if self.retirement_or_vacancy_date < nowdate():
                frappe.throw("Vacancy date cannot be in the past")

    def validate_incumbent_department(self):
        if self.incumbent_employee:
            emp_dept = frappe.db.get_value(
                "Employee",
                self.incumbent_employee,
                "department"
            )

            if emp_dept and emp_dept != self.department:
                frappe.throw("Incumbent employee does not belong to selected department")
