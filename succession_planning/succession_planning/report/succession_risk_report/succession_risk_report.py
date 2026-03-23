# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

    # ---------------- COLUMNS ---------------- #

    columns = [
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
            "label": "Risk Level",   # 🔥 NEW COLUMN
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

    # Get all succession plans
    succession_plans = frappe.get_all(
        "Succession Plan",
        fields=["name", "critical_role", "department", "bench_status"]
    )

    for sp in succession_plans:

        # Get nominees for each plan
        nominees = frappe.get_all(
            "Succession Nominee",
            filters={"parent": sp.name},
            fields=["readiness_level"]
        )

        # Count values
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

        # ---------------- APPEND ---------------- #

        data.append({
            "critical_role": sp.critical_role,
            "department": sp.department,
            "bench_status": sp.bench_status,
            "risk_level": risk_level,   # 🔥 ADDED
            "total_nominees": total_nominees,
            "ready_now": ready_now
        })

    return columns, data