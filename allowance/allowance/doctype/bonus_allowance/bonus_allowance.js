// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bonus Allowance', {
	onload: function(frm) {
		frm.clear_table("component_details")
		frm.refresh_field('component_details')
		frm.call({
			method:'get_components',
			doc: frm.doc,
		});
	},
	get_details:function(frm) {
		frm.clear_table("bonus_allowance_details")
		frm.refresh_field('bonus_allowance_details')
		frm.call({
			method:'get_details',
			doc: frm.doc,
		});
	}
});