
import stripe

stripe.api_key = "sk_test_51LLGC6L6X1F1cMlGS8lon3H0IrNl8QMpHdxF5o7ADhehnv5xI6F5fdwTvfPKuAKbpusEUumurNwNAoeVzcaeAWtJ00RHJ1hwbY"
stripe.api_version = "2020-08-27"

a = stripe.PaymentIntent.confirm(
    'pi_3LLJ9nL6X1F1cMlG0x9ZztSM',
    payment_method='pm_card_visa'
)

print(a)