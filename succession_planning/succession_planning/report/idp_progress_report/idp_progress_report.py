# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Target Role",
            "fieldname": "target_role",
            "fieldtype": "Link",
            "options": "Critical Role Register",
            "width": 200
        },
        {
            "label": "IDP Status",
            "fieldname": "idp_status",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": "Completion %",
            "fieldname": "overall_competition",
            "fieldtype": "Percent",
            "width": 130
        },
        {
            "label": "Start Date",
            "fieldname": "idp_period_start",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": "End Date",
            "fieldname": "idp_period_end",
            "fieldtype": "Date",
            "width": 130
        }
    ]
    data = []
    idps = frappe.get_all(
        "Individual Development Plan",
        fields=[
            "employee",
            "employee_name",
            "target_role",
            "idp_status",
            "overall_competition",
            "idp_period_start",
            "idp_period_end"
        ]
    )

    for idp in idps:
        data.append({
            "employee": idp.employee,
            "employee_name": idp.employee_name,
            "target_role": idp.target_role,
            "idp_status": idp.idp_status,
            "overall_competition": idp.overall_competition,
            "idp_period_start": idp.idp_period_start,
            "idp_period_end": idp.idp_period_end
        })
    return columns, data