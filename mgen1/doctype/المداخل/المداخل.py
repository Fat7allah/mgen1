import frappe
from frappe.model.document import Document
import re
from decimal import Decimal

class المداخل(Document):
    def validate(self):
        """
        Validate income data before saving:
        - Validate academic year format
        - Ensure province belongs to selected region
        - Calculate total amount and shares
        - Validate amounts are positive
        """
        self.validate_academic_year()
        self.validate_province_region()
        self.validate_amounts()
        self.calculate_totals()
        
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
            
        # For membership cards, amount should be 100
        if self.type == "بطائق" and self.amount != 100:
            frappe.throw("يجب أن يكون مبلغ البطاقة 100 درهم")

    def calculate_totals(self):
        """Calculate total amount and shares"""
        # Calculate total
        self.total_amount = self.count * self.amount
        
        # Calculate shares
        total = Decimal(str(self.total_amount))
        
        # Office share (50%)
        self.office_share = float(total * Decimal('0.50'))
        
        # Region share (20%)
        self.region_share = float(total * Decimal('0.20'))
        
        # Province share (30%)
        self.province_share = float(total * Decimal('0.30'))
        
        # Validate shares sum up to total
        total_shares = self.office_share + self.region_share + self.province_share
        if abs(total_shares - self.total_amount) > 0.01:  # Allow for small floating-point differences
            frappe.throw("خطأ في حساب الحصص")

    def before_save(self):
        """Perform any necessary transformations before saving"""
        if self.description:
            self.description = self.description.strip()
        if self.note:
            self.note = self.note.strip()
            
    def on_submit(self):
        """Actions to perform when the document is submitted"""
        self.create_shares_ledger_entries()
        
    def create_shares_ledger_entries(self):
        """Create ledger entries for each share"""
        # This method will be implemented when we create the shares ledger doctype
        pass
