frappe.ui.form.on('Succession Plan', {
    refresh: function(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button('Create IDP', () => {

                if (!frm.doc.nominees || frm.doc.nominees.length === 0) {
                    frappe.msgprint("Please add nominees first");
                    return;
                }

                // 🔥 Ensure correct role value
                let role = frm.doc.critical_role;

                if (!role) {
                    frappe.msgprint("Critical Role not set");
                    return;
                }

                let nominee_options = frm.doc.nominees.map(n => n.nominee_employee);

                frappe.prompt([
                    {
                        fieldname: 'employee',
                        label: 'Select Nominee',
                        fieldtype: 'Select',
                        options: nominee_options,
                        reqd: 1
                    }
                ], (values) => {

                    // 🔥 Check duplicate IDP safely
                    frappe.db.get_value(
                        'Individual Development Plan',
                        {
                            employee: values.employee,
                            target_role: role
                        },
                        'name'
                    ).then(r => {

                        if (r.message && r.message.name) {
                            frappe.msgprint("IDP already exists for this employee");
                            return;
                        }

                        // 🔥 Create new IDP
                        frappe.new_doc('Individual Development Plan', {
                            employee: values.employee,
                            target_role: role,
                            succession_plan: frm.doc.name
                        });

                    });

                }, 'Create IDP', 'Create');

            });

        }

    }
});