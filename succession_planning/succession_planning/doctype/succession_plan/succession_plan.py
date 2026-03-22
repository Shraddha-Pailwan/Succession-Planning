# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SuccessionPlan(Document):

    def validate(self):
        self.calculate_readiness_counts()

    def calculate_readiness_counts(self):
        ready_now = 0
        one_year = 0
        two_plus = 0

        for nominee in self.nominees:
            if nominee.readiness_level == "Ready Now":
                ready_now += 1
            elif nominee.readiness_level == "1 Year":
                one_year += 1
            elif nominee.readiness_level == "2+ Years":
                two_plus += 1

        # Optional: store in fields (if you created them)
        self.ready_now_count = ready_now
        self.one_year_count = one_year
        self.two_plus_count = two_plus