# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SuccessionPlan(Document):
    def validate(self):
        self.validate_nominees()
        self.check_duplicate_nominees()
        self.validate_bench_strength()
        self.set_bench_status()

    def validate_nominees(self):
        if not self.nominees:
            frappe.throw("At least one nominee is required")

    def check_duplicate_nominees(self):
        employees = []
        for nominee in self.nominees:
            if nominee.nominee_employee in employees:
                frappe.throw(f"Duplicate nominee found: {nominee.nominee_employee}")
            employees.append(nominee.nominee_employee)

    def validate_bench_strength(self):
        if not self.critical_role:
            return
        min_strength = frappe.db.get_value(
            "Critical Role Register",
            self.critical_role,
            "minimum_bench_strength"
        ) or 0   
        ready_now = sum(
            1 for n in self.nominees if n.readiness_level == "Ready Now"
        )
        if ready_now < min_strength:
            frappe.msgprint("⚠️ Warning: Bench strength not sufficient")

    def set_bench_status(self):
        if not self.nominees:
            self.bench_status = "Critical Gap"
            return
        min_strength = frappe.db.get_value(
            "Critical Role Register",
            self.critical_role,
            "minimum_bench_strength"
        ) or 0   
        ready_now = sum(
            1 for n in self.nominees if n.readiness_level == "Ready Now"
        )
        if ready_now >= min_strength and ready_now > 0:
            self.bench_status = "Adequate"
        elif ready_now > 0:
            self.bench_status = "At Risk"
        else:
            self.bench_status = "Critical Gap"