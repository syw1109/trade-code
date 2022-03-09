import pyupbit

access = "kOGUe0SNWDmntPRhSdwMVN8ltxxg1CYioRNcf2Gn"          # 본인 값으로 변경
secret = "llNZP0GwWE21OP26Cb9yOYbXQbFFEchNZuXlRuYX"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회