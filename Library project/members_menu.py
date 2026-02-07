import json
#باز کردن و تبدیل فایل های مورد نیاز به دیکشنری پایتون
with open("books.json", "r") as booksdata:
    book_data = json.load(booksdata)

with open("user_data.json", "r") as d:
    user_data = json.load(d)
    username = user_data["username"]

while True:
    try:
        print("\n \n \n")
        print("help:At each step, press Enter continuously to return to the main menu.")
        print(" Menu:\n 1.books search \n 2.my list of borrowed books\n 3.Exit")
        choose = input("chose:").strip()
        #رفتن به سرچ
        if choose == "1":
            while True:
                search = input("Enter Title of book:").title()
                found = False
                #استفاده از حلقه فور برای پیدا کردن کتاب
                for book in book_data:
                    if search in book["title"]:
                        found = True
                        print(book)
                if found:
                    print("1.request for loan \n 2.Exit")
                    choose = input("choose:").strip()
                    if choose == "1":
                        title = input("Enter Title of book:").title()
                        #باز کردن و تبدیل فایل های مورد نیاز به دیکشنری پایتون

                        with open("books.json", "r") as booksdata:
                            book_data = json.load(booksdata)
                        with open("loans.json", "r") as loans:
                            loans = json.load(loans)
                        found = False
                        for book in book_data:
                            if (
                                book["title"] == title
                                #عدم نمایش کتاب درصورت اتمام موجودی
                                and book["available_count"] != 0
                            ):
                                found = True
                                repeat = True
                                # چک کردن عدم تکراری بودن درخواست
                                if not any(
                                    loan["username"] == username
                                    and loan["book_title"] == title
                                    for loan in loans
                                ):
                                    #ثبت درخواست در صورت تکراری نبودن
                                    loan = {
                                        "username": f"{username}",
                                        "book_title": f"{title}",
                                        "request date": "",
                                        "return date": "",
                                        "status": "pending",
                                    }
                                    #اضافه کردن درخواست به لیست دیکشنری درخواست ها
                                    with open("loans.json", "r") as l:
                                        loans = json.load(l)
                                        loans.append(loan)
                                    #جایگزین کردن لیست جدید به فایل
                                    with open("loans.json", "w") as L:
                                        json.dump(loans, L)
                                    repeat = False
                        #اعلام وضعیت درخواست
                        if not found:
                            print("<<Not found>>")

                        elif found and repeat:
                            print("<<You have already requested this book.>>")

                        elif found and not repeat:
                            print("<<done>>")

                        break

                    else:
                        break
                #اعلام پیدا نشدن کتاب
                if not found:
                    print("<<not found>>")
                    break
        #رفتن به لیست کتاب های قرض گرفته شده شخص 
        elif choose == "2":
            while True:
                #باز کردن لیست و پیدا کردن شخص با استفاده از فور
                with open("loans.json", "r") as f:
                    data_loan = json.load(f)
                    found = False
                    for user in data_loan:
                        if user["username"] == username:
                            print(user)
                            found = True
                    #ارائه پیشنهاد بازگشت یا تمدید کتاب درصورت وجود
                    #در هر دو انتخاب باید کتاب در وضعیت approved باشد
                    if found:
                        print(
                            "1.loan extension request \n 2.request to return a book \n 3.Exit "
                        )
                        choose = input("choose:")
                        #انتخاب تمدید 
                        if choose == "1":
                            title = input("Enter title of book:").title()
                            #باز کردن فایل لیست قرض جهت تغییر وضعیت
                            with open("loans.json", "r") as l:
                                loans = json.load(l)
                                found = False
                                for user in loans:
                                    if (
                                        user["username"] == username
                                        and user["book_title"] == title
                                        and user["status"] == "approved"
                                    ):
                                        user["status"] = "renew_pending"
                                        print("<<done>>")
                                        found = True
                                #وارد کردن لیست جدید
                                with open("loans.json", "w") as l:
                                    json.dump(loans, l)
                                if not found:
                                    print("<<Not found>>")
                                break
                        #انتخاب بازگشت کتاب
                        elif choose == "2":
                            title = input("Enter title of book:").title()
                            #باز کردن فایل جهت تغییر وضعیت
                            with open("loans.json", "r") as l:
                                loans = json.load(l)
                                found = False
                                for user in loans:
                                    if (
                                        user["username"] == username
                                        and user["book_title"] == title
                                        and user["status"] == "approved"
                                    ):
                                        user["status"] = "returned"
                                        print("<<done>>")
                                        found = True
                                        break
                                #وارد کردن لیست جدید
                                with open("loans.json", "w") as L:
                                    json.dump(loans, L)
                                #اعلام پیدا نشدن 
                                if not found:
                                    print("<<Not found>>")
                                break
                        else:
                            break
                    #اعلام پیدا نشدن کتاب قرض گرفته شده
                    if not found:
                        print("<<not found>>")
                        break
                break
        else:
            break
    #جلوگیری از کرش 
    except:
        print("<<invalid input>>")
#خالی کردن فایل حاوی اطلاعات ضروری کاربر
with open("user_data.json", "w") as d:
    json.dump({}, d)
import os
#کلیر کردن ترمینال
os.system("cls" if os.name == "nt" else "clear")

