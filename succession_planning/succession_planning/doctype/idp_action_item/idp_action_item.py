# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IDPActionItem(Document):
    def before_save(self):
        self.set_status()

    def set_status(self):
        if self.completion_date:
            self.status = "Completed"
        elif self.status == "Completed" and not self.completion_date:
            self.status = "In Progress"