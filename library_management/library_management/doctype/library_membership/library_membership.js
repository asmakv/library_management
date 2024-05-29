
frappe.ui.form.on('Library Membership', {
  from_date: function(frm){
    console.log('test');
    if(frm.doc.to_date && frm.doc.from_date > frm.doc.to_date){
      frappe.throw('Invalid ');
    }
  },
  to_date: function(frm){
    console.log('test');
    if(frm.doc.from_date > frm.doc.to_date){
      frappe.throw('Invalid ');
}
}
});
