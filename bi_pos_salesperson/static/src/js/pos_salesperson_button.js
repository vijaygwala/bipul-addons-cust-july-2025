odoo.define('bi_pos_salesperson.pos_salesperson_button', function(require) {
'use strict';

   const PosComponent = require('point_of_sale.PosComponent');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const Registries = require('point_of_sale.Registries');
   const { useListener } = require("@web/core/utils/hooks");
	var core = require('web.core');
	var _t = core._t;

	class SelectSalespersonButton extends PosComponent {
		setup() {
          super.setup();
		   useListener('click', this.onClick);
		}
		async onClick() {
			var self = this;
			var order = self.env.pos.get_order();
			var orderlines = order.orderlines;
			let lst = self.env.pos.pos_salesperson_record;
			const selectedOrderline = this.env.pos.get_order().get_selected_orderline();

			if (orderlines.length === 0) {
				self.showPopup('ErrorPopup',{
					'title': self.env._t('Empty Order'),
					'body': self.env._t('There must be at least one product in your order before applying cashier.'),
				});
				return;
			}else{
				const selectionList = lst.map(otype => ({
					id: otype.id,
					label: otype.name,
					isSelected:false,
					item: otype,
				}));

				const { confirmed, payload: selecteduser } = await self.showPopup('SelectionPopup',{
					title: self.env._t('Choose Cashier'),
					list: selectionList,
				});
				if (confirmed) {
					selectedOrderline.set_customer_name(selecteduser.name);
					selectedOrderline.set_customer_id(selecteduser.id);
				}
			}
		}
	}
	SelectSalespersonButton.template = 'SelectSalespersonButton';
	ProductScreen.addControlButton({
	   component: SelectSalespersonButton,
	   condition: function() {
		   return this.env.pos.config.allow_cashier;
	   },
	});
	Registries.Component.add(SelectSalespersonButton);
	return SelectSalespersonButton;
});
