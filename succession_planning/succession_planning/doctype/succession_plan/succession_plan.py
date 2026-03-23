# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class SuccessionPlan(Document):

#     def validate(self):
#         self.calculate_readiness_counts()

#     def calculate_readiness_counts(self):
#         ready_now = 0
#         one_year = 0
#         two_plus = 0

#         for nominee in self.nominees:
#             if nominee.readiness_level == "Ready Now":
#                 ready_now += 1
#             elif nominee.readiness_level == "1 Year":
#                 one_year += 1
#             elif nominee.readiness_level == "2+ Years":
#                 two_plus += 1

#         # Optional: store in fields (if you created them)
#         self.ready_now_count = ready_now
#         self.one_year_count = one_year
#         self.two_plus_count = two_plus
import frappe
from frappe.model.document import Document


class SuccessionPlan(Document):

    # ---------------- MAIN TRIGGER ---------------- #

    def validate(self):
        self.validate_nominees()
        self.check_duplicate_nominees()
        self.validate_bench_strength()
        self.set_bench_status()

    # ---------------- VALIDATIONS ---------------- #

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
        ) or 0   # 🔥 SAFE

        ready_now = sum(
            1 for n in self.nominees if n.readiness_level == "Ready Now"
        )

        if ready_now < min_strength:
            frappe.msgprint("⚠️ Warning: Bench strength not sufficient")

    # ---------------- BENCH STATUS AUTOMATION ---------------- #

    def set_bench_status(self):

        if not self.nominees:
            self.bench_status = "Critical Gap"
            return

        min_strength = frappe.db.get_value(
            "Critical Role Register",
            self.critical_role,
            "minimum_bench_strength"
        ) or 0   # 🔥 SAFE

        ready_now = sum(
            1 for n in self.nominees if n.readiness_level == "Ready Now"
        )

        # 🔥 FINAL LOGIC
        if ready_now >= min_strength and ready_now > 0:
            self.bench_status = "Adequate"
        elif ready_now > 0:
            self.bench_status = "At Risk"
        else:
            self.bench_status = "Critical Gap"