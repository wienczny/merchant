from flask.ext.wtf import Form
from wtforms import TextField, DecimalField, SelectField
import decimal
import datetime

curr_year = datetime.datetime.now().year
month_choices = ((ii, ii) for ii in range(1, 13))
year_choices = ((ii, ii) for ii in range(curr_year, curr_year + 7))


class StripeForm(Form):
    # Small value to prevent non-zero values. Might need a relook
#    amount = DecimalField(min_value=decimal.Decimal('0.001'))
    amount = DecimalField()
    credit_card_number = TextField()
    credit_card_cvc = TextField()
    credit_card_expiration_month = SelectField(choices=month_choices)
    credit_card_expiration_year = SelectField(choices=year_choices)
