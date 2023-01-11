# coding=UTF-8

import shioaji as sj

api = sj.Shioaji(simulation=True)
api.logout()

accounts = api.login("帳號", "密碼")
api.activate_ca(
    ca_path="憑證路徑",
    ca_passwd="身分證字號",
    person_id="Person of this Ca",
)


# from shioaji.data import Ticks



# ticks = api.ticks(
    # contract=api.Contracts.Stocks["2330"], 
    # date="2022-12-27"
# )

# import pandas as pd
# df = pd.DataFrame({**ticks})
# df.ts = pd.to_datetime(df.ts)
# print(df.head())

api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type="tick")
api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type="bidask")




api.logout()