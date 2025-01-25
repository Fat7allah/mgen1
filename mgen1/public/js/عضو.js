frappe.ui.form.on('عضو', {
    refresh: function(frm) {
        // Add custom buttons or actions here
    },
    
    region: function(frm) {
        // Clear province when region changes
        if(frm.doc.region) {
            frm.set_value('province', '');
        }
    },
    
    validate: function(frm) {
        // Additional client-side validations can be added here
    }
});
