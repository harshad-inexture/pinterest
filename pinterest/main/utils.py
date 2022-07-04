def user_interest_tags(interested_tags):
    list = []
    for interest in interested_tags:
        list.append(interest[0])
    return list

def user_interest_pins(inst_pin_id):
    list = []
    for pin in inst_pin_id:
        list.append(pin.pin_id)
    return list
