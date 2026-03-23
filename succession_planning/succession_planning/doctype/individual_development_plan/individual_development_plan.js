// Copyright (c) 2026, Quantbit Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Individual Development Plan', {
    setup: function(frm) {
        frm.set_query("employee", function() {
            return {};
        });
    },
    refresh: function(frm) {
        apply_employee_filter(frm);
    },
    succession_plan: function(frm) {
        apply_employee_filter(frm);
    }
});

function apply_employee_filter(frm) {
    if (!frm.doc.succession_plan) return;
    frappe.db.get_doc('Succession Plan', frm.doc.succession_plan)
        .then(sp => {
            let allowed_employees = sp.nominees.map(n => n.nominee_employee);
            frm.set_query("employee", function() {
                return {
                    filters: {
                        name: ["in", allowed_employees]
                    }
                };
            });
        });
}