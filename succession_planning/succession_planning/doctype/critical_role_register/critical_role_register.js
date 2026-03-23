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
frappe.ui.form.on('Critical Role Register', {

    refresh: function(frm) {

        if (!frm.doc.designation) return;

        // prevent duplicate filling
        if (frm.doc.skills && frm.doc.skills.length > 0) return;

        // clear table
        frm.clear_table("skills");

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Designation",
                name: frm.doc.designation
            },
            callback: function(r) {

                console.log("DATA 👉", r.message);

                if (r.message && r.message.skills) {

                    r.message.skills.forEach(function(row) {

                        let child = frm.add_child("skills");
                        child.skill = row.skill;

                    });

                    frm.refresh_field("skills");
                }
            }
        });
    },

    designation: function(frm) {
        // also run when manually changed
        frm.clear_table("skills");
        frm.trigger("refresh");
    }
});

frappe.ui.form.on('Critical Role Register', {
    onload: function(frm) {
        if (frm.doc.designation) {
            frm.trigger("designation");
        }
    }
});
