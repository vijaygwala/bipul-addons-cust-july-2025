odoo.define('pos_membership_custom.VerifyMembership', function (require) {
    "use strict";
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require('point_of_sale.ProductScreen');
    var { Gui } = require('point_of_sale.Gui');
    const { useListener } = require("@web/core/utils/hooks");
    var core = require('web.core');
    var _t = core._t;
    const { EventBus} = owl;
    // const { EventBus } = require("@web/core/utils");
    const bus = new EventBus();

    class VerifyMembership extends PosComponent {


        setup() {
            super.setup()
            useListener("click", this.verify_membership);
        }

        async verify_membership() {
            if (this.env.pos.get_order().get_partner()) {
                // this.pbc.Membership_check();
                
                const { confirmed, payload } = await this.showPopup('MembershipPopupVerify')
                // const pbc = new MembershipPopupVerify();
                
            }
            else {
                Gui.showPopup("ErrorPopup", {
                    'title': _t("Customer"),
                    'body': _t("You Must Select a Customer"),
                });
            }
        }
    }
    VerifyMembership.template = "VerifyMembership"


    ProductScreen.addControlButton({
        component: VerifyMembership,
        position: ["after", "CreateMembership"],

    });

    Registries.Component.add(VerifyMembership);
    return VerifyMembership;
});


