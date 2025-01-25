import frappe
from frappe.model.document import Document

class الاقليم(Document):
    def validate(self):
        # Validate that the province belongs to a valid region
        if self.region:
            region = frappe.get_doc("الجهة", self.region)
            if not region:
                frappe.throw("الجهة غير موجودة")
    
    def before_save(self):
        # Additional logic before saving
        pass
