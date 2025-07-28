/** @odoo-module **/

import models from 'point_of_sale.models';
import { Order, Orderline } from 'point_of_sale.models';
import Registries from "point_of_sale.Registries";
const CashierOrderLine = (Orderline) => class CashierOrderLine extends Orderline {
     constructor() {
          super(...arguments);
          this.cashier_employee_id = this.cashier_employee_id || null;
     }
     set_cashier_id(cashier_employee_id) {
          this.cashier_employee_id = cashier_employee_id
     }
     set_cashier_name(cashier_employee_name) {
          this.cashier_employee_name = cashier_employee_name
     }
     get_cashier_id() {
          return this.cashier_employee_id
     }
     get_cashier_name() {
          return this.cashier_employee_name 
     }
     //send order data to send to the server
     export_as_JSON() {
          const json = super.export_as_JSON(...arguments)
          json.cashier_employee_id = this.cashier_employee_id;
          return json;
     }
     init_from_JSON(json) {
          super.init_from_JSON(...arguments);
          this.cashier_employee_id = json.cashier_employee_id;
     }
};
Registries.Model.extend(Orderline, CashierOrderLine);