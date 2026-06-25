from src.masks import get_mask_account, get_mask_card_number

# from src.utils import transactions_csv, transactions_excel
from src.widget import mask_account_card

if __name__ == "__main__":
    # result_1 = transactions_csv("data/transactions.csv")
    # print(result_1)

    # result_2 = transactions_excel("data/transactions_excel.xlsx")
    # print(result_2)

    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_mask_card_number("0111123412341234"))
    print(get_mask_account("73654108430135874305"))
