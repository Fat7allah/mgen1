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

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/mgen1/css/mgen1.css"
app_include_js = "/assets/mgen1/js/mgen1.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/mgen1/css/mgen1.css"
# web_include_js = "/assets/mgen1/js/mgen1.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mgen1/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "عضو": "public/js/عضو.js",
    "المداخل": "public/js/المداخل.js",
    "المصارف": "public/js/المصارف.js"
}

# Translation
translation_modules = ["mgen1"]
required_apps = ["frappe"]
