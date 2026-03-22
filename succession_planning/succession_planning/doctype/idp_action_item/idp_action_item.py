# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IDPActionItem(Document):

    def validate(self):
        self.update_status()
        self.update_parent_completion()

    def update_status(self):
        if self.completion_date:
            self.status = "Completed"

    def update_parent_completion(self):
        if not self.parent:
            return

        idp = frappe.get_doc("Individual Development Plan", self.parent)

        total = len(idp.action_items)
        completed = 0

        for item in idp.action_items:
            if item.status == "Completed":
                completed += 1

        if total > 0:
            idp.overall_completion = (completed / total) * 100
        else:
            idp.overall_completion = 0

        idp.save(ignore_permissions=True)