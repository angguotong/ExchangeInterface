import pandas as pd
import json 
import requests

class crypto_pricing ():
    
    def __init__ (self):
        self.websites = {
            "Binance_Price": r"https://www.binance.com/api/v3/ticker/price",
            "Crypto_Price": r"https://api.crypto.com/v2/public/get-ticker"
        }
        self.Price_list = {
            "Binance": "",
            "Crypto": ""
        }
        self.Counter = 0
        self.frame = ""

    def main (self):
        user_input = input("Please enter currency pair in 'BTC/ETH' format or key 'ALL' for everything, type exit to quit: ").upper()
        if type(user_input) == str and "/" in user_input:
            Currency_1,Currency_2 = user_input.split("/")
            self.requesting_website(Currency_1,Currency_2)
            print (self.Price_list)

        elif user_input == "ALL":
            user_input = input ("(Binance)BI or (Crypto.com)CRY: ").upper()
            while user_input != "BI" and user_input != "CRY" and user_input != "EXIT":
                user_input = input ("Please enter BI or CRY type exit to quit: ").upper()
            if user_input == "EXIT":
                pass
            self.requesting_website (exchange = user_input)
            print (self.frame)
                
        elif user_input == "EXIT":
            pass

        else:
            print("INVALID ENTRY, Please enter in the format as shown")
            self.main()
            #If in valid, they will prompt and re run command.
        
    def requesting_website (self, Currency_1 = None, Currency_2 = None, exchange = None):

        if exchange:
            if "BI" in exchange:
                prices = self.request_quote(self.websites["Binance_Price"])
                frame = pd.DataFrame(prices) # transform to a dataframe for easy manupliation and user reading
                frame.column = ["Symbol", "Last Traded"]
                # print (frame)
                self.frame = frame

            elif "CRY" in exchange:
                prices = self.request_quote(self.websites["Crypto_Price"])
                prices = prices["result"]["data"]
                frame = pd.DataFrame(prices)
                frame["i"] = frame["i"].str.replace("_","")
                frame = frame.loc[:,"i":"b"]
                frame.columns = ["Symbol","Last Traded"]
                # print (frame)
                self.frame = frame
                
            else: 
                pass

        else:
            for websites in self.websites:
                if "Binance_Price" in websites:
                    Price = self.request_quote (self.websites[websites]+"?symbol="+Currency_1+Currency_2)
                    try:
                        Cleaned_price = float(Price["price"])
                        self.Price_list["Binance"] = Cleaned_price
                        self.Counter = 0
                    except:
                        print ("currency pair input does not exist on Binance")
                        pass
                elif "Crypto_Price" in websites:
                    Price = self.request_quote (self.websites[websites]+ "?instrument_name="+Currency_1+"_"+Currency_2)
                    try:
                        Cleaned_price = float(Price['result']["data"]["b"])
                        self.Price_list ["Crypto"] = Cleaned_price
                        self.Counter = 0
                    except:
                        print ("currency pair input not exist on crypto.com")
                else:
                    pass
            if not self.Price_list and self.Counter <= 1 and not exchange:
                Currency_exchange = Currency_1
                Currency_1 = Currency_2
                Currency_2 = Currency_exchange
                print ("We will try the following pair: {}/{}".format(Currency_1,Currency_2))
                self.Counter += 1
                self.requesting_website(Currency_1,Currency_2)
                
            elif self.Counter > 1: 
                print ("Wrong symbol")
                print ("Restarting........")
                self.main()

    def request_quote (self, website):
        request_site = requests.get(website).json()
        return (request_site)



if __name__ == "__main__":
    crypto_pricing().main()
