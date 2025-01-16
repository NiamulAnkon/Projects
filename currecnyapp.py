from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter

try:
    def main():
        currency_rates = CurrencyRates()
        currency_codes = CurrencyCodes()
        
        print("Welcome to the Currency Converter!")
        while True:
            print("\nOptions:")
            print("1. Convert Currency")
            print("2. List Available Currencies")
            print("3. Exit")
            
            choice = input("Select an option (1/2/3): ").strip()
            
            if choice == "1":
                convert_currency(currency_rates, currency_codes)
            elif choice == "2":
                list_currencies()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def convert_currency(currency_rates, currency_codes):
        from_currency = input("Enter the base currency (e.g., USD): ").strip().upper()
        to_currency = input("Enter the target currency (e.g., EUR): ").strip().upper()
        amount = input("Enter the amount to convert: ").strip()
        
        try:
            amount = float(amount)
            result = currency_rates.convert(from_currency, to_currency, amount)
            symbol = currency_codes.get_symbol(to_currency)
            print(f"\n{amount} {from_currency} = {symbol}{result:.2f} {to_currency}")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")

    def list_currencies():
        print("\nSample currencies:")
        print("USD - United States Dollar")
        print("EUR - Euro")
        print("GBP - British Pound")
        print("JPY - Japanese Yen")
        print("AUD - Australian Dollar")
        print("...and more!")

    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Error: {e}")