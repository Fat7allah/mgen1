app_name = "mgen1"
app_title = "نظام إدارة الأعضاء والبطائق"
app_publisher = "Your Organization"
app_description = "نظام متكامل لإدارة الأعضاء والبطائق والمالية"
app_email = "your.email@example.com"
app_license = "MIT"

# Document Events
doc_events = {
    "عضو": {
        "validate": "mgen1.events.member_events.validate_member",
    }
}

# Fixtures
fixtures = [
    {
        "doctype": "المهنة",
        "filters": [["name", "not in", []]]
    },
    {
        "doctype": "التخصص",
        "filters": [["name", "not in", []]]
    },
    {
        "doctype": "الهيكل",
        "filters": [["name", "not in", []]]
    },
    {
        "doctype": "الجهة",
        "filters": [["name", "not in", []]]
    },
    {
        "doctype": "الاقليم",
        "filters": [["name", "not in", []]]
    },
    {
        "doctype": "المستوى الدراسي",
        "filters": [["name", "not in", []]]
    }
]

# Workspaces
workspaces = {
    "التخصيصات": {
        "category": "Modules",
        "icon": "octicon octicon-settings",
        "type": "module",
        "link": "modules/التخصيصات",
        "label": "التخصيصات"
    },
    "التسيير": {
        "category": "Modules",
        "icon": "octicon octicon-organization",
        "type": "module",
        "link": "modules/التسيير",
        "label": "التسيير"
    }
}

# Reports
reports = [
    {
        "doctype": "تقرير البطائق",
        "report_type": "Script Report",
        "module": "التسيير",
        "name": "تقرير البطائق",
        "ref_doctype": "المداخل",
    }
]

# Translation
translation_modules = ["mgen1"]
required_apps = ["frappe"]
