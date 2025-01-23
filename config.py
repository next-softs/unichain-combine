
# использовать прокси True/False
useProxies = True

# кол-во символов в дробной части объёмов [от, до]
precision = [4, 6]

# объём для бриджа
bridge_amount = [0.035, 0.045]

# мин. объём для бриджа в unichain т.е. если unichain eth+weth меньше заданного, то бриджим
min_bridge_amount = 0.025

# объём для врапа/анврапа [от, до]
wrap_amount = [0.01, 0.025]

# шансы на рандомные действия
weights_transactions = {
    "wrap_unwrap": 0.9,
    "deploy": 0.1
}

# задержки
delay_actions = [30, 180]
