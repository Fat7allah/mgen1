frappe.ui.form.on('المصارف', {
    refresh: function(frm) {
        // Add custom buttons or actions here
    },
    
    region: function(frm) {
        // Clear province when region changes
        if(frm.doc.region) {
            frm.set_value('province', '');
        }
    },
    
    count: function(frm) {
        // Recalculate total when count changes
        if(frm.doc.count && frm.doc.amount) {
            frm.set_value('total_amount', frm.doc.count * frm.doc.amount);
        }
    },
    
    amount: function(frm) {
        // Recalculate total when amount changes
        if(frm.doc.count && frm.doc.amount) {
            frm.set_value('total_amount', frm.doc.count * frm.doc.amount);
        }
    }
});
