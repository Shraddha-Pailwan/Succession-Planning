frappe.ui.form.on('Succession Plan', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button('Create IDP', async () => {
                if (!frm.doc.nominees || frm.doc.nominees.length === 0) {
                    frappe.msgprint("Please add nominees first");
                    return;
                }
                let role = frm.doc.critical_role;
                if (!role) {
                    frappe.msgprint("Critical Role not set");
                    return;
                }
                let nominee_ids = frm.doc.nominees.map(n => n.nominee_employee);
                let employees = await frappe.db.get_list('Employee', {
                    filters: { name: ['in', nominee_ids] },
                    fields: ['name', 'employee_name']
                });
                let options_map = {};
                let options = employees.map(emp => {
                    let label = `${emp.name} - ${emp.employee_name}`;
                    options_map[label] = emp.name;
                    return label;
                });
                frappe.prompt([
                    {
                        fieldname: 'employee',
                        label: 'Select Nominee',
                        fieldtype: 'Select',
                        options: options,
                        reqd: 1
                    }
                ], (values) => {
                    let selected_employee = options_map[values.employee];
                    frappe.db.get_value(
                        'Individual Development Plan',
                        {
                            employee: selected_employee,
                            target_role: role
                        },
                        'name'
                    ).then(r => {
                        if (r.message && r.message.name) {
                            frappe.msgprint("IDP already exists for this employee");
                            return;
                        }
                        frappe.new_doc('Individual Development Plan', {
                            employee: selected_employee,
                            target_role: role,
                            succession_plan: frm.doc.name
                        });
                    });
                }, 'Create IDP', 'Create');
            });
        }
        if (frm.doc.critical_role && (!frm.doc.skills || frm.doc.skills.length === 0)) {
            frm.trigger("critical_role");
        }
    },

    critical_role: function(frm) {
        if (!frm.doc.critical_role) return;
        frm.clear_table("skills");
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Critical Role Register",
                name: frm.doc.critical_role
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
    }
});