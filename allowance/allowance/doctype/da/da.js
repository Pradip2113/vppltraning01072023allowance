// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('DA', {
	get_details: function (frm) {
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	}
});
