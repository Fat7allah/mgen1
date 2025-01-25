import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    if not filters:
        filters = {}

    # Ensure academic_year is provided
    if not filters.get("academic_year"):
        frappe.throw(_("الموسم الدراسي إلزامي"))

    columns = get_columns()
    data = get_data(filters)
    
    return columns, data, None, None, None

def get_columns():
    """Return columns for the report"""
    return [
        {
            "fieldname": "region",
            "label": _("الجهة"),
            "fieldtype": "Link",
            "options": "الجهة",
            "width": 120
        },
        {
            "fieldname": "province",
            "label": _("الإقليم"),
            "fieldtype": "Link",
            "options": "الاقليم",
            "width": 120
        },
        {
            "fieldname": "structure",
            "label": _("الهيكل"),
            "fieldtype": "Link",
            "options": "الهيكل",
            "width": 120
        },
        {
            "fieldname": "profession",
            "label": _("المهنة"),
            "fieldtype": "Link",
            "options": "المهنة",
            "width": 120
        },
        {
            "fieldname": "member_count",
            "label": _("عدد الأعضاء"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "cards_issued",
            "label": _("البطائق المسلمة"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "total_amount",
            "label": _("المبلغ الإجمالي"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "office_share",
            "label": _("حصة المكتب"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "region_share",
            "label": _("حصة الجهة"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "province_share",
            "label": _("حصة الإقليم"),
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    """Get report data based on filters"""
    # Build conditions for member query
    conditions = ["m.academic_year = %(academic_year)s"]
    if filters.get("region"):
        conditions.append("m.region = %(region)s")
    if filters.get("province"):
        conditions.append("m.province = %(province)s")
    if filters.get("structure"):
        conditions.append("m.structure = %(structure)s")
    if filters.get("profession"):
        conditions.append("m.profession = %(profession)s")
    if filters.get("from_date"):
        conditions.append("i.date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("i.date <= %(to_date)s")

    # Get members data
    members_data = frappe.db.sql("""
        SELECT 
            m.region,
            m.province,
            m.structure,
            m.profession,
            COUNT(DISTINCT m.name) as member_count
        FROM `tabعضو` m
        WHERE {conditions}
        GROUP BY m.region, m.province, m.structure, m.profession
    """.format(conditions=" AND ".join(conditions)), filters, as_dict=1)

    # Get income data for cards
    income_data = frappe.db.sql("""
        SELECT 
            i.region,
            i.province,
            SUM(i.count) as cards_issued,
            SUM(i.total_amount) as total_amount,
            SUM(i.office_share) as office_share,
            SUM(i.region_share) as region_share,
            SUM(i.province_share) as province_share
        FROM `tabالمداخل` i
        WHERE i.type = 'بطائق'
            AND i.academic_year = %(academic_year)s
            AND i.docstatus = 1
            {date_condition}
            {region_condition}
            {province_condition}
        GROUP BY i.region, i.province
    """.format(
        date_condition="AND i.date >= %(from_date)s" if filters.get("from_date") else "",
        region_condition="AND i.region = %(region)s" if filters.get("region") else "",
        province_condition="AND i.province = %(province)s" if filters.get("province") else ""
    ), filters, as_dict=1)

    # Merge data
    result = []
    for member in members_data:
        row = member.copy()
        # Find matching income data
        income = next((i for i in income_data 
                      if i.region == member.region 
                      and i.province == member.province), None)
        if income:
            row.update({
                "cards_issued": income.cards_issued,
                "total_amount": income.total_amount,
                "office_share": income.office_share,
                "region_share": income.region_share,
                "province_share": income.province_share
            })
        else:
            row.update({
                "cards_issued": 0,
                "total_amount": 0,
                "office_share": 0,
                "region_share": 0,
                "province_share": 0
            })
        result.append(row)

    return result
