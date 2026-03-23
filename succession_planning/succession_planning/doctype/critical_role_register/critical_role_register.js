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
        if (!frm.doc.designation) return;
        if (frm.doc.skills && frm.doc.skills.length > 0) return;
        frm.clear_table("skills");
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Designation",
                name: frm.doc.designation
            },
            callback: function(r) {
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
        frm.clear_table("skills");
        frm.trigger("refresh");
    },
    onload: function(frm) {
        if (frm.doc.designation) {
            frm.trigger("designation");
        }
    }
});