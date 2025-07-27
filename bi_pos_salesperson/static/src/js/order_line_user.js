odoo.define('bi_pos_salesperson.order_line_user', function(require) {
    'use strict';

   const PosComponent = require('point_of_sale.PosComponent');
   const Registries = require("point_of_sale.Registries");
   const Orderline = require("point_of_sale.Orderline");


   const PosOrderline = (Orderline) =>
        class extends Orderline {
            setup() {
                super.setup();
			}
            selectLine() {
                this.env.pos.get_order().select_orderline(this.props.line);
            }
            async ShowCustomerRecord() {
                var self = this;
                var order = self.env.pos.get_order();
			    var orderlines = order.orderlines;
                var lst = self.env.pos.pos_salesperson_record;

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
                    var selectedOrderLine = order.get_selected_orderline()
                    selectedOrderLine.set_customer_name(selecteduser.name);
                    selectedOrderLine.set_customer_id(selecteduser.id);
			    }
            }
            imageUrl(id) {
			    return '/web/image?model=res.users&id='+id+'&field=image_1920';
            }
            RemoveCustomer(){
                var selectedOrderLine = this.env.pos.get_order().get_selected_orderline()
                selectedOrderLine.set_customer_name();
                selectedOrderLine.set_customer_id();
            }
        };

    Registries.Component.extend(Orderline, PosOrderline);
    return Orderline;

    });
