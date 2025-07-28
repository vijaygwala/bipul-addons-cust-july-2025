odoo.define('pos_salesperson_app.SalesPersonPopupWidget', function(require) {
	"use strict";

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	

	class SalesPersonPopupWidget extends AbstractAwaitablePopup {
		setup() {
	    	super.setup();
		}
		client_click_event(event){
			var self = this;
			var order = this.env.pos.get_order();
			var o_id = $(event.srcElement).data('id');
			var user_name = $(event.srcElement).data('name');
			order.get_selected_orderline().set_sales_person(o_id, user_name);
			self.trigger('close-popup');
			var add_user = $('.add_salesuser');
			var info_user = $('.user_info');
			for (var i = 0; i < add_user.length; i++){
				if ($(add_user[i]).find('.user_add_id').val() == this.props.list.id){
					$(add_user[i]).hide();
				}
			}
			for (var i = 0; i < info_user.length; i++){
				if ($(info_user[i]).find('.user_info_id').val() == this.props.list.id){
					$(info_user[i]).show();
				}
			}
		}
		cancel(){
			this.env.posbus.trigger('close-popup', {
                popupId: this.props.id,
                response: { confirmed: false, payload: null },
            });
		}
	}

	SalesPersonPopupWidget.template = 'SalesPersonPopupWidget';
	SalesPersonPopupWidget.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: '',
        body: '',
        list: [],
        startingValue: '',
    };

	Registries.Component.add(SalesPersonPopupWidget);

});
