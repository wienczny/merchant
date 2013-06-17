# MERCHANT SETTINGS
MERCHANT_TEST_MODE = True
MERCHANT_SETTINGS = {
    "authorize_net": {
        "LOGIN_ID" : '7Sjt4A3k8',
        "TRANSACTION_KEY" : '8e23TH9G48fBVe4g',
        "MD5_HASH": "Gp5m42rq"
    },

    "pay_pal": {
        "WPP_USER" : 'probiz_1273571007_biz_api1.uswaretech.com',
        "WPP_PASSWORD" : 'LJKRH4CWWE6JTNSN',
        "WPP_SIGNATURE" : 'ADZb7XvwG3K4qw8AuQOMhbhAZ-6HACL1wp2xcDPWwMcjXnxuQVPhrCGy',
        "RECEIVER_EMAIL" : 'probiz_1273571007_biz@uswaretech.com',
        },

    "eway": {
        "CUSTOMER_ID" : '87654321',
        "USERNAME" : "test@eway.com.au",
        "PASSWORD" : "test123"
        },

    "google_checkout": {
        # GOOGLE CHECKOUT SETTINGS
        "MERCHANT_ID" : '646831507676008' ,
        "MERCHANT_KEY" : 'NHyIFSDAM4lu__yPK80dnQ'
        },

    "world_pay": {
        # WORLDPAY settings
        "HOSTED_URL_TEST": "https://select-test.wp3.rbsworldpay.com/wcc/purchase",
        "HOSTED_URL_LIVE" : "https://secure.wp3.rbsworldpay.com/wcc/purchase",
        "INSTALLATION_ID_TEST": "12345",
        "MD5_SECRET_KEY": 'testmd5'
        },

    "stripe": {
        # Stripe settings
        "API_KEY" : "LnCHYifVhMyG08xtkLOZqh4iQ5T8MD8a",
        "PUBLISHABLE_KEY" : "pk_odadWDmylnlpMiHYl4UlipJVOjYJz"
        },

    # Paylane Settings
    "paylane": {
        "USERNAME": "javed.agiliq",
        "PASSWORD": "chi8swe9"
        },

    "samurai": {
        # Samurai Merchant Key
        "MERCHANT_KEY" : "150dda63e796d678f5efe4b9",
        "MERCHANT_PASSWORD" : "b8e43e5ccb9170be59d7e92d",
        "PROCESSOR_TOKEN" : "f5d58b8a0d362fb172f2a848"
        },

    "amazon_fps": {
        "AWS_ACCESS_KEY" : "AKIAI74UIJQ37QS6XLTA",
        "AWS_SECRET_ACCESS_KEY" : "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"
        },

    "braintree_payments": {
        "MERCHANT_ACCOUNT_ID" : "nx2r5xy5g5mzrn7p",
        "PUBLIC_KEY" : "9xzvscgwry3zsq6p",
        "PRIVATE_KEY" : "4197fe85ca47ed01652a752dd46b8e3c"
        },

    # WePay Settings
    "we_pay": {
        "CLIENT_ID": "167247",
        "CLIENT_SECRET": "88ae6d9858",
        "ACCOUNT_ID": "157432",
        "ACCESS_TOKEN": "28befdcda1576511e9421023ee792cb83669a191867f715365f3b190adbee8d9",
    },

    "beanstream": {
        "MERCHANT_ID": 271990000,
        "LOGIN_COMPANY": "AgiliqInfoSolutionsSB",
        "LOGIN_USER": "admin",
        "LOGIN_PASSWORD": "423c2Ae2",
        "HASH_ALGORITHM"   : "SHA1",
        "HASHCODE"  : "merchant_test",
        "payment_profile_passcode":"BCCE75A688F8497E9CDBC77AA8178581",
    },

    "chargebee": {
        "API_KEY": "QSFYXOVdl4uKqhIJo8dhKm5cuu0zKmOXz",
        "SITE": "agiliq-test"
    },

    "bitcoin": {
        "RPCUSER": "bitcoinrpc",
        "RPCPASSWORD": "jAAn91Hlkw",
        "HOST": "merchant.agiliq.com",
        "PORT": "18332",
        "ACCOUNT": "merchant",
    },
}
