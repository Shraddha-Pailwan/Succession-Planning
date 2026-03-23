// Copyright (c) 2026, Quantbit Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Critical Role Register', {
    refresh: function(frm) {

        if (!frm.is_new()) {
            frm.add_custom_button('Create Succession Plan', function() {

                frappe.new_doc('Succession Plan', {
                    critical_role: frm.doc.name,
                    department: frm.doc.department
                });

            });
        }

    }
});
