odoo.define('pos_membership_custom.MembershipPopup', function (require) {
    'use strict';
    const { Gui } = require('point_of_sale.Gui');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('web.core');
    var rpc = require('web.rpc');
    const { useState, useRef, onMounted } = owl;
    //Creates a pop up for membership
    class MembershipPopup extends AbstractAwaitablePopup {
        setup() {

            super.setup();
            let customer = this.env.pos.get_order().get_partner()
            this.state = useState({ customer_name: customer.name, special_date: '', special_day: 'birthday', membership: '', other_type: '', total_sale: 0.0 ,current_membership_limit:600})
            this.memberships = useState([]);
            var self = this
            

            var mbts = rpc.query({
                model: 'res.partner',
                method: 'get_total_sale_current_year',
                args: [[customer.id]]
            }).then(function (total_amount) {
                self.state.total_sale = total_amount
                console.log(`Total current year sale ${self.state.total_sale} is not meeting the membership limit ${self.state.current_membership_limit}`)
                if (self.state.total_sale < self.state.current_membership_limit){
                    $("#inv-ts").text(`Total current year sale ${self.state.total_sale} is not meeting the membership limit ${self.state.current_membership_limit}`)
                    }
                    else{
                        $("#inv-ts").text("")
                    }
            })

           

            //This is used to retrieve the customers membership details
            var mbts = rpc.query({
                model: 'membership.type',
                method: 'get_memebership_types',
                args: [, { customer: customer.id }]
            }).then(function (mbts) {
                console.log(mbts)
                self.env.pos.mbts = mbts
                mbts.forEach((mbt, index, array) => {
                    self.memberships.push({
                        id: mbt.id,
                        name: mbt.name,

                    })

                    if (index == 0){
                        self.state.membership = mbt.id
                    }
                });
            })
           

           
        }
        // This is used to check the customer has membership

        async membership_create() {
            console.log(this.state)
            var self = this
            let customer = this.env.pos.get_order().get_partner()
            var mbts = rpc.query({
                model: 'membership.card',
                method: 'create_upgrade_membership',
                args: [, {
                    customer: customer.id,
                    membership: this.state.membership ? this.state.membership : $('#picker').val(),
                    special_date: this.state.special_date,
                    special_day: this.state.special_day,
                    other_type: this.state.other_type

                }]
            }).then(function (mbts) {
                self.env.posbus.trigger('close-popup', {
                    popupId: self.props.id,
                    response: { confirmed: true, payload: mbts },
                });

            })

        }
        async getDropdownValues(event) {
            var self = this
            let val = $('#special_date_type').val()
            if (val == 'other') {
                $("#other-mb").css("display", "inline-block");
                $("#other-mb-label").css("display", "flex");
            }
            else {
                $("#other-mb").css("display", "none");
                $("#other-mb-label").css("display", "none");
            }

            if (event.target.id == 'picker') {
                this.state.membership = event.target.value
            }
            else {
                this.state.special_day = event.target.value
            }
            console.log(`membership type id ${this.state.membership}`)
            var mts = await rpc.query({
                model: 'membership.type',
                method: 'get_limit_membership',
                args: [,{membership: this.state.membership}]
            }).then(function (purchase_amount) {
                self.state.current_membership_limit = purchase_amount
            })

            if (this.state.total_sale < this.state.current_membership_limit){
            $("#inv-ts").text(`Total current year sale ${this.state.total_sale} is not meeting the membership limit ${this.state.current_membership_limit}`)
            }
            else{
                $("#inv-ts").text("")
            }

        }

    }
    //Create membership popup
    MembershipPopup.template = 'MembershipPopup';
    MembershipPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: 'Membership Card',
        body: '',
    };
    Registries.Component.add(MembershipPopup);
    return MembershipPopup
});
