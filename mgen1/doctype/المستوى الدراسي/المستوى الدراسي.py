import frappe
from frappe.model.document import Document

class المستوىالدراسي(Document):
    def validate(self):
        # Ensure level_order is unique
        existing = frappe.get_all(
            "المستوى الدراسي",
            filters={"level_order": self.level_order, "name": ["!=", self.name]},
            limit=1
        )
        if existing:
            frappe.throw("هناك مستوى آخر بنفس الترتيب")
