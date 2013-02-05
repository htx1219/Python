import cutchoose
from unit6_util import string_to_bits, bits_to_int, pad_to_block, bits_to_string, convert_to_bits

def _verify(bills, nonces, value):
    signed = cutchoose._SIGNED_BILL[0]
    for i in range(len(bills)):
        if i < signed:
            msg = cutchoose.create_bill_message(i, value, nonces[i])
        if i >= signed:
            msg = cutchoose.create_bill_message(i+1, value, nonces[i])
        if bills[i] != msg:
            return False
    return True
    ###########
cutchoose._verify = _verify

def test():
    # Alice generates some bills
    bills = cutchoose.generate_bills(50)
    # and sends them to the bank.
    # The bank picks one and sends
    # back which one
    i = cutchoose.pick_and_sign_bills(bills)
    # Alice now needs to send back 
    # the random nonces
    nonces = cutchoose.send_nonces(i)
    # bank checks the nonces and
    # if they pass, returns the signed bill

    signed = cutchoose.verify_bills_and_return_signed(nonces, 50)
    assert signed is not None
    assert bills[i] == pow(signed, cutchoose.BANK_PUBLIC_KEY[0], 
                           cutchoose.BANK_PUBLIC_KEY[1])

    # here, we'll try to cheat and see if we get caught
    bills = cutchoose.cheat_generate_bills(50, 100)
    i = cutchoose.pick_and_sign_bills(bills)
    nonces = cutchoose.send_nonces(i)
    signed = cutchoose.verify_bills_and_return_signed(nonces, 50)
    # there is a 1% chance we got away with this
    assert signed is None
    print 'test passed'

test()
