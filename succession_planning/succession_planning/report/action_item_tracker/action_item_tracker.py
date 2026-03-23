# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from datetime import date

def execute(filters=None):

    # ---------------- COLUMNS ---------------- #

    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Action Title", "fieldname": "action_title", "fieldtype": "Data", "width": 200},
        {"label": "Target Date", "fieldname": "target_date", "fieldtype": "Date", "width": 130},
        {"label": "Completion Date", "fieldname": "completion_date", "fieldtype": "Date", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Overdue", "fieldname": "overdue", "fieldtype": "Data", "width": 120}
    ]

    data = []

    # Get all IDPs
    idps = frappe.get_all(
        "Individual Development Plan",
        fields=["name", "employee", "employee_name"]
    )

    for idp in idps:

        # Fetch child table
        doc = frappe.get_doc("Individual Development Plan", idp.name)

        for item in doc.action_items:

            # ---------------- OVERDUE LOGIC ---------------- #

            overdue = "No"

            if item.target_date and not item.completion_date:
                if item.target_date < date.today():
                    overdue = "Yes"

            # ---------------- APPEND ---------------- #

            data.append({
                "employee": idp.employee,
                "employee_name": idp.employee_name,
                "action_title": item.action_title,
                "target_date": item.target_date,
                "completion_date": item.completion_date,
                "status": item.status,
                "overdue": overdue
            })

    return columns, data
