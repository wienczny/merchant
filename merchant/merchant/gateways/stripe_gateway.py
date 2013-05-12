from flask.ext.merchant import Gateway, GatewayNotConfigured
from merchant.utils.credit_card import InvalidCard, Visa, MasterCard, \
     AmericanExpress, Discover, CreditCard
import stripe


class StripeGateway(Gateway):
    supported_cardtypes = [Visa, MasterCard, AmericanExpress, Discover]
    supported_countries = ['US']
    default_currency = "USD"
    homepage_url = "https://stripe.com/"
    display_name = "Stripe"

    def purchase(self, amount, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
                }
        try:
            response = self.stripe.Charge.create(
                amount=int(amount * 100),
                currency=self.default_currency.lower(),
                card=card)
        except self.stripe.CardError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def store(self, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
                }
        try:
            customer = self.stripe.Customer.create(card=card)
        except (self.stripe.CardError, self.stripe.InvalidRequestError), error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': customer}

    def recurring(self, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
                }
        try:
            plan_id = options['plan_id']
            self.stripe.Plan.retrieve(options['plan_id'])
            try:
                response = self.stripe.Customer.create(
                    card=card,
                    plan=plan_id
                )
                return {"status": "SUCCESS", "response": response}
            except self.stripe.CardError, error:
                return {"status": "FAILURE", "response": error}
        except self.stripe.InvalidRequestError, error:
            return {"status": "FAILURE", "response": error}
        except TypeError, error:
            return {"status": "FAILURE", "response": "Missing Plan Id"}

    def unstore(self, identification, options=None):
        try:
            customer = self.stripe.Customer.retrieve(identification)
            response = customer.delete()
            return {"status": "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError, error:
            return {"status": "FAILURE", "response": error}

    def credit(self, identification, money=None, options=None):
        try:
            charge = self.stripe.Charge.retrieve(identification)
            response = charge.refund(amount=money)
            return {"status": "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError, error:
            return {"status": "FAILURE", "error": error}

    def authorize(self, money, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
                }
        try:
            token = self.stripe.Token.create(
                card=card,
                amount=int(money * 100),
            )
            return {'status': "SUCCESS", "response": token}
        except self.stripe.InvalidRequestError, error:
            return {"status": "FAILURE", "response": error}

    def capture(self, money, authorization, options=None):
        try:
            response = self.stripe.Charge.create(
                amount=int(money * 100),
                card=authorization,
                currency=self.default_currency.lower()
            )
            return {'status': "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError, error:
            return {"status": "FAILURE", "response": error}
