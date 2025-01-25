import frappe
from frappe.model.document import Document
import re
from datetime import datetime

class عضو(Document):
    def validate(self):
        """
        Validate member data before saving:
        - Validate phone number format
        - Validate email format if provided
        - Ensure province belongs to selected region
        - Validate academic year format
        """
        self.validate_phone()
        self.validate_email()
        self.validate_province_region()
        self.validate_academic_year()
        self.validate_structure_level()
        
    def validate_phone(self):
        """Ensure phone number follows Moroccan format"""
        phone_pattern = r'^(?:\+212|0)[5-7]\d{8}$'
        if not re.match(phone_pattern, self.phone):
            frappe.throw("رقم الهاتف غير صحيح. يجب أن يكون في الشكل: 0XXXXXXXXX أو +212XXXXXXXXX")

    def validate_email(self):
        """Validate email format if provided"""
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                frappe.throw("البريد الإلكتروني غير صحيح")

    def validate_province_region(self):
        """Ensure selected province belongs to selected region"""
        if self.province and self.region:
            province = frappe.get_doc("الاقليم", self.province)
            if province.region != self.region:
                frappe.throw("الإقليم المحدد لا ينتمي إلى الجهة المحددة")

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

    def validate_structure_level(self):
        """Ensure the structure level matches the region/province assignment"""
        if not self.structure:
            return
            
        structure = frappe.get_doc("الهيكل", self.structure)
        
        # For national level positions, no additional validation needed
        if structure.structure_level == "وطني":
            return
            
        # For regional level positions, must have a region
        if structure.structure_level == "جهوي" and not self.region:
            frappe.throw("يجب تحديد الجهة للمناصب الجهوية")
            
        # For provincial level positions, must have both region and province
        if structure.structure_level == "إقليمي" and (not self.region or not self.province):
            frappe.throw("يجب تحديد الجهة والإقليم للمناصب الإقليمية")
            
        # For local level positions, must have region, province and branch
        if structure.structure_level == "محلي" and (not self.region or not self.province or not self.branch):
            frappe.throw("يجب تحديد الجهة والإقليم والفرع للمناصب المحلية")

    def before_save(self):
        """Set default values and perform any necessary transformations"""
        # Capitalize names
        if self.first_name:
            self.first_name = self.first_name.strip().title()
        if self.last_name:
            self.last_name = self.last_name.strip().title()
            
        # Format phone number consistently
        if self.phone and self.phone.startswith('+212'):
            self.phone = '0' + self.phone[4:]
