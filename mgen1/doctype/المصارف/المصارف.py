import frappe
from frappe.model.document import Document
import re

class المصارف(Document):
    def validate(self):
        """
        Validate expense data before saving:
        - Validate academic year format
        - Ensure province belongs to selected region
        - Calculate total amount
        - Validate amounts are positive
        """
        self.validate_academic_year()
        self.validate_province_region()
        self.validate_amounts()
        self.calculate_total()
        
    def validate_academic_year(self):
        """Validate academic year format (YYYY-YYYY)"""
        year_pattern = r'^\d{4}-\d{4}$'
        if not re.match(year_pattern, self.academic_year):
            frappe.throw("صيغة السنة الدراسية غير صحيحة. يجب أن تكون في الشكل: YYYY-YYYY")
        
        # Validate that the second year is the first year + 1
        try:
            year1, year2 = map(int, self.academic_year.split('-'))
            if year2 != year1 + 1:
                frappe.throw("السنة الثانية يجب أن تكون السنة الأولى + 1")
        except ValueError:
            frappe.throw("صيغة السنة الدراسية غير صحيحة")

    def validate_province_region(self):
        """Ensure selected province belongs to selected region"""
        if self.province and self.region:
            province = frappe.get_doc("الاقليم", self.province)
            if province.region != self.region:
                frappe.throw("الإقليم المحدد لا ينتمي إلى الجهة المحددة")

    def validate_amounts(self):
        """Ensure amounts and count are positive"""
        if self.count <= 0:
            frappe.throw("يجب أن يكون العدد أكبر من صفر")
        if self.amount <= 0:
            frappe.throw("يجب أن يكون المبلغ أكبر من صفر")

    def calculate_total(self):
        """Calculate total amount based on count and amount"""
        self.total_amount = self.count * self.amount

    def before_save(self):
        """Perform any necessary transformations before saving"""
        if self.description:
            self.description = self.description.strip()
        if self.note:
            self.note = self.note.strip()
