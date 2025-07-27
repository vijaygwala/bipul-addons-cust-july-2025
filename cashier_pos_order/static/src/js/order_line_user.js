odoo.define('cashier_pos_order.order_line_user', function (require) {
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

                var selectedOrderLine = order.get_selected_orderline()
                selectedOrderLine.set_cashier_name();
                selectedOrderLine.set_cashier_id();

            }
            imageUrl(id) {
                return '/web/image?model=hr.employee&id=' + id + '&field=image_1920';
            }
            RemoveCustomer() {
                var selectedOrderLine = this.env.pos.get_order().get_selected_orderline()
                selectedOrderLine.set_cashier_name();
                selectedOrderLine.set_cashier_id();
            }
        };

    Registries.Component.extend(Orderline, PosOrderline);
    return Orderline;

});
