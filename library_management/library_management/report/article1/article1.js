frappe.query_reports["article1"] = {
    "filters": [
        {
            "fieldname": "article_name",
            "label": __("Article Name"),
            "fieldtype": "Link",
            "options": "Article"
        },
        {
            "fieldname": "author",
            "label": __("Author"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "publisher",
            "label": __("Publisher"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "isbn",
            "label": __("ISBN"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Data"
        }
    ]
};
