# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IndividualDevelopmentPlan(Document):

    def after_save(self):
        self.update_nominee()

    def update_nominee(self):
        if not self.succession_plan:
            return

        sp = frappe.get_doc("Succession Plan", self.succession_plan)

        for nominee in sp.nominees:
            if nominee.nominee_employee == self.employee:
                nominee.idp_created = 1
                nominee.idp_reference = self.name

        sp.save(ignore_permissions=True)