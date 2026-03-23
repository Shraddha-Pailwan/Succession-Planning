# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IndividualDevelopmentPlan(Document):
    def validate(self):
        """
        Runs before every save.
        Used for validations + calculations + automation.
        """
        self.validate_dates()
        self.validate_readiness()
        self.validate_employee_in_plan()
        self.prevent_duplicate_idp()
        self.validate_action_item_dates()
        self.validate_completion_date()
        self.calculate_overall_completion()
        self.update_idp_status()

    def after_insert(self):
        """
        Runs only once when document is created.
        Used to update nominee in Succession Plan.
        """
        self.update_nominee()

    def on_update(self):
        """
        Runs on every update.
        Keeps nominee data in sync.
        """
        self.update_nominee()

    def validate_dates(self):
        """
        Ensure IDP start date is before end date.
        """
        if self.idp_period_start and self.idp_period_end:
            if self.idp_period_start > self.idp_period_end:
                frappe.throw("Start Date cannot be after End Date")

    def validate_readiness(self):
        """
        Ensure target readiness is not worse than starting readiness.
        """
        levels = ["Ready Now", "1 Year", "2+ Years"]
        if self.readiness_at_start and self.traget_readiness:
            if self.traget_readiness in levels and self.readiness_at_start in levels:
                if levels.index(self.traget_readiness) > levels.index(self.readiness_at_start):
                    frappe.throw("Target readiness cannot be worse than starting readiness")

    def validate_employee_in_plan(self):
        """
        Ensure selected employee exists in the linked Succession Plan.
        """
        if not self.succession_plan:
            return
        sp = frappe.get_doc("Succession Plan", self.succession_plan)
        employees = [n.nominee_employee for n in sp.nominees]
        if self.employee not in employees:
            frappe.throw("Employee is not part of selected Succession Plan")

    def prevent_duplicate_idp(self):
        """
        Prevent multiple IDPs for same employee + role.
        """
        if not self.employee or not self.target_role:
            return
        exists = frappe.db.get_value(
            "Individual Development Plan",
            {
                "employee": self.employee,
                "target_role": self.target_role
            },
            "name"
        )
        if exists and exists != self.name:
            frappe.throw("IDP already exists for this employee and role")

    def validate_action_item_dates(self):
        """
        Ensure target date lies within IDP period.
        """
        for item in self.action_items:
            if item.target_date and self.idp_period_start and self.idp_period_end:
                if item.target_date < self.idp_period_start or item.target_date > self.idp_period_end:
                    frappe.throw(f"Target Date for '{item.action_title}' must be within IDP period")

    def validate_completion_date(self):
        """
        Ensure completion date is not before target date.
        """
        for item in self.action_items:
            if item.completion_date and item.target_date:
                if item.completion_date < item.target_date:
                    frappe.throw(f"Completion Date cannot be before Target Date for '{item.action_title}'")

    def calculate_overall_completion(self):
        """
        Calculate overall completion percentage based on completed action items.
        """
        total = len(self.action_items)
        completed = 0
        for item in self.action_items:
            if item.status == "Completed":
                completed += 1
        if total > 0:
            self.overall_competition = (completed / total) * 100
        else:
            self.overall_competition = 0

    def update_idp_status(self):
        """
        Automatically update IDP status based on progress.
        Also auto-mark items as completed if completion date is filled.
        """
        if not self.action_items:
            self.idp_status = "Draft"
            return
        total = len(self.action_items)
        completed = 0
        for item in self.action_items:
            if item.completion_date:
                item.status = "Completed"
            if item.status == "Completed":
                completed += 1
        if completed == 0:
            self.idp_status = "In Progress"
        elif completed < total:
            self.idp_status = "In Progress"
        else:
            self.idp_status = "Completed"

    def update_nominee(self):
        """
        Update nominee table in Succession Plan:
        - Mark IDP created
        - Store IDP reference
        """
        if not self.succession_plan:
            return
        sp = frappe.get_doc("Succession Plan", self.succession_plan)
        updated = False
        for nominee in sp.nominees:
            if nominee.nominee_employee == self.employee:
                nominee.idp_created = 1
                nominee.idp_reference = self.name
                updated = True
        if updated:
            sp.flags.ignore_validate_update_after_submit = True
            sp.save(ignore_permissions=True)