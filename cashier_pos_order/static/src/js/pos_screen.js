/**@odoo-module **/
import PosComponent from "point_of_sale.PosComponent";
import ProductScreen from "point_of_sale.ProductScreen";
import { useListener } from "@web/core/utils/hooks";
import Registries from "point_of_sale.Registries";
import { isConnectionError } from "point_of_sale.utils";

export class CashierButton extends PosComponent {
    /**
     * Sets up the component and adds a click listener to the button.
     */
    setup() {
        super.setup();
        useListener("click", this.onClick);
    }
   
    
   
    async onClick() {
        try {
           
            this.showPopup("CashierPopup", {
                'employees': this.env.pos.employee_ids
            });

        } catch (error) {
            if (isConnectionError(error)) {
                this.showPopup("ErrorPopup", {
                    title: this.env._t("Network Error"),
                    body: this.env._t("Cannot access Product screen if offline."),
                });
            } else {
                throw error;
            }
        }
    }
}
CashierButton.template = "CashierButton";
ProductScreen.addControlButton({
    component: CashierButton,
    condition: function() {
        return true;
    },
});
Registries.Component.add(CashierButton);
