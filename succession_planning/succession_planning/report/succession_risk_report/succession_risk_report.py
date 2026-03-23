# Copyright (c) 2026, Quantbit Technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):

    # ---------------- COLUMNS ---------------- #

    columns = [
        {
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 150
        },
        {
            "label": "Critical Role",
            "fieldname": "critical_role",
            "fieldtype": "Link",
            "options": "Critical Role Register",
            "width": 200
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 150
        },
        {
            "label": "Bench Status",
            "fieldname": "bench_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Risk Level",
            "fieldname": "risk_level",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "No. of Nominees",
            "fieldname": "total_nominees",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "Ready Now Count",
            "fieldname": "ready_now",
            "fieldtype": "Int",
            "width": 150
        }
    ]

    # ---------------- DATA ---------------- #

    data = []

    # 🔥 Fetch with Branch
    succession_plans = frappe.get_all(
        "Succession Plan",
        fields=["name", "critical_role", "department", "bench_status", "branch"],
        order_by="branch asc"
    )

    current_branch = None

    for sp in succession_plans:

        # ---------------- GROUP HEADER ---------------- #
        if current_branch != sp.branch:
            current_branch = sp.branch

            data.append({
                "branch": f"🔹 {current_branch}",
                "indent": 0,
                "is_group": 1
            })

        # ---------------- NOMINEES ---------------- #

        nominees = frappe.get_all(
            "Succession Nominee",
            filters={"parent": sp.name},
            fields=["readiness_level"]
        )

        total_nominees = len(nominees)
        ready_now = 0

        for n in nominees:
            if n.readiness_level == "Ready Now":
                ready_now += 1

        # ---------------- RISK LOGIC ---------------- #

        if sp.bench_status == "Critical Gap":
            risk_level = "High"
        elif sp.bench_status == "At Risk":
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # ---------------- CHILD ROW ---------------- #

        data.append({
            "branch": sp.branch,
            "critical_role": sp.critical_role,
            "department": sp.department,
            "bench_status": sp.bench_status,
            "risk_level": risk_level,
            "total_nominees": total_nominees,
            "ready_now": ready_now,
            "indent": 1
        })

    return columns, data