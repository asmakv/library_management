import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.calc_delay_fine()
            self.update_article_list()
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                article.status = "Issued"
                article.save()

        elif self.type == "Return":
            self.validate_return()
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                article.status = "Available"
                article.save()

    def validate_issue(self):
        self.validate_membership()
        for row in self.article_list:
            article = frappe.get_doc("Article", row.article)
            if article.status == "Issued":
                frappe.throw("Article is already issued by another member")

    def before_save(self):
        if self.type == "Return":
            self.validate_return()
            self.delay_fine = self.calc_delay_fine() or 0  # Assign 0 if self.delay_fine is None
            damage_fine = int(self.damage_fine) if self.damage_fine else 0
            self.total_fine = self.delay_fine + damage_fine

    def validate_return(self):
        for row in self.article_list:
            article = frappe.get_doc("Article", row.article)
            if article.status == "Available":
                frappe.throw("Article cannot be returned without being issued first")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

    def calc_delay_fine(self):
        delay_fine = 0
        for row in self.article_list:
            valid_delay_fine = frappe.db.exists(
                "Library Transaction",
                {
                    "library_member": self.library_member,
                    "article": row.article,
                    "docstatus": 1,
                    "type": "Issue",
                },
            )

            if valid_delay_fine:
                issued_doc = frappe.get_last_doc(
                    "Library Transaction",
                    filters={
                        "library_member": self.library_member,
                        "article": row.article,
                        "docstatus": 1,
                        "type": "Issue",
                    },
                )
                issued_date = issued_doc.date

                loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
                actual_duration = frappe.utils.date_diff(self.date, issued_date)

                if actual_duration > loan_period:
                    single_day_fine = frappe.db.get_single_value('Library Settings', 'single_day_fine')
                    delay_fine += single_day_fine * (actual_duration - loan_period)

        return delay_fine

    def update_article_list(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        if self.type == "Issue":
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                library_member.append("issued_articles", {
                    "article_name": article.name,
                    # "issue_date": self.date,
                    # "due_date": self.due_date  # Ensure these fields exist in your doctype
                    })

        library_member.save()
