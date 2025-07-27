odoo.define('pos_membership_custom.ValidationClient', function (require) {
    const PartnerDetailsEdit = require("point_of_sale.PartnerDetailsEdit");
    const Registries = require("point_of_sale.Registries");
    const { _t } = require("web.core");
    const PartnerDetailsEditInherit = PartnerDetailsEdit => class extends PartnerDetailsEdit {
        setup() {
            super.setup()
            const partner = this.props.partner;
            this.changes.custom_state = partner.custom_state || '';

        }
        ValidateEmail(input) {
            console.log(input)

            if(!input)
                {
                    return true
                }

            var validRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

            if (input.match(validRegex)) {



                return true;

            } else {



                return false;

            }

        }

        validateContact(input) {
            console.log(input)

            if(!input)
            {
                return true
            }

            var regex = new RegExp(/^(\+?\d{1,3}[-.\s]?)?(\(?\d{1,4}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,9}[-.\s]?\d{0,9}$/);
            //regex.test('0501234567'); // return true;
            if (regex.test(input)) {
                return true
            } else {
                return false
            }
        }

        async saveChanges() {
            

            const is_email_valid = this.ValidateEmail(this.changes.email)
            const is_phone_valid = this.validateContact(this.changes.phone)
            const is_mobile_valid = this.validateContact(this.changes.mobile)
            console.log(is_email_valid,is_mobile_valid,is_phone_valid)
            if(!is_email_valid)
            {
                return this.showPopup("ErrorPopup", {
                    title: _t("Please Enter an Valid Email Address"),
                });

            }

            if(!is_mobile_valid)
                {
                    return this.showPopup("ErrorPopup", {
                        title: _t("Please Enter an Valid Mobile Number"),
                    });
    
                }

                if(!is_phone_valid)
                    {
                        return this.showPopup("ErrorPopup", {
                            title: _t("Please Enter an Valid Phone Number"),
                        });
        
                    }

            console.log(is_email_valid,is_mobile_valid,is_phone_valid)
            super.saveChanges();
        }

        captureChange(event) {
            super.captureChange(event)
            this.changes[event.target.name] = event.target.value

        }
    };

    Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditInherit);

    return PartnerDetailsEditInherit;
});