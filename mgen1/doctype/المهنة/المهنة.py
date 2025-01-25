import frappe
from frappe.model.document import Document

class المهنة(Document):
    def validate(self):
        # Add any validation logic here
        pass

    def before_save(self):
        # Add any pre-save logic here
        pass
