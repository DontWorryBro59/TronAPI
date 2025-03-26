from tronpy import Tron

tron = Tron()


address = 'TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ'
# Получаем информацию о кошельке
wallet = tron.get_account(address)
# Получаем информацию о балансе кошелька
balance = tron.get_account_balance(address)
bandwidth = tron.get_bandwidth(address)
energy = tron.get_account_resource(address)['TotalEnergyLimit']
print(f"""
Баланс кошелька: {balance}
Баланс полосы пропускания: {bandwidth}
Баланс энергии: {energy}""")