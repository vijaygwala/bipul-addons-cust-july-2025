odoo.define('cashier_pos_order.pos', function(require) {
    "use strict";
    var { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    /**
    * This function creates a new class that extends PosGlobalState with an additional property res_users.
    * The res_users property is loaded from the backend and contains all users in the system.
    */
    const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.employee_ids = loadedData['employee_ids'];
        }
    }
    Registries.Model.extend(PosGlobalState, NewPosGlobalState);
});
