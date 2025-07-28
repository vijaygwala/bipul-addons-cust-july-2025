/**@odoo-module **/
import AbstractAwaitablePopup from "point_of_sale.AbstractAwaitablePopup";
import Registries from "point_of_sale.Registries";
const { useState,useRef } = owl;
var core = require('web.core');
var rpc = require('web.rpc');
const { Gui } = require('point_of_sale.Gui');
var _t = core._t;
class CashierPopup extends AbstractAwaitablePopup {

    setup() {
        super.setup();
        this.CashierRef = useRef('CashierRef')
        this.employee_allowed = useState([])
        var self = this
        var employyy = rpc.query({
            model: 'hr.employee',
            method: 'get_employii',
            args: [Object.values(this.env.pos.config.employee_ids)]
        }).then(function (employeess) {

            employeess.forEach(function (item, index) {
                
                self.employee_allowed.push(item)
              });

        })
        
    }
   
    confirm() {

            let option = this.CashierRef.el.selectedOptions[0]
            console.log(option.id,option.value,Object.values(this.env.pos.config.employee_ids))
            var order = this.env.pos.get_order()
            // order.set_order_cashier(parseInt(option.id))
            // this.env.pos.selectedOrder.selected_orderline.salesperson = [parseInt(option.id), option.value]
            var selectedOrderLine = order.get_selected_orderline()
                selectedOrderLine.set_cashier_name(option.value);
                selectedOrderLine.set_cashier_id(parseInt(option.id));
            
            this.env.posbus.trigger("close-popup", {
                popupId: this.props.id,
                response: {
                    confirmed: true,
                    payload: null,
                },
            });
    
    }
    /**
     * Cancel the selection of a salesperson for the selected orderline, and close the popup.
     */
    cancel() {
        this.env.posbus.trigger("close-popup", {
            popupId: this.props.id,
            response: {
                confirmed: false,
                payload: null,
            },
        });
    }
}
CashierPopup.template = "CashierPopup";
Registries.Component.add(CashierPopup);
