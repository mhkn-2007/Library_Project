#تعریف تابع خواندن فایل
def read_json(x):
    import json

    with open(x + ".json", "r") as r:
        data = json.load(r)
        return data

#تعریف تابع نگاشتن فایل
def write_json(y, x):
    import json

    with open(x + ".json", "w") as w:
        json.dump(y, w)

#کتابخوانه datetime 
from datetime import date, timedelta

today = date.today()
five_days_later = today + timedelta(days=5)


while True:
    try:
        print("\n \n \n \n")
        print("help:At each step, press Enter continuously to return to the main menu.")
        print(
            " Menu:\n1.View and manage requests \n 2.Add book\n 3.Edit the book\n 4.delete the book \n 5.Add Member \n 6.Delete Member\n 7.Deactivate/Activate user\n 8.Users list \n 9.Books list \n10.Loans list \n 11.Exit"
        )
        choice = input("choose:").strip()
        #رفتن به بررسی درخواست ها
        if choice == "1":
            loans = read_json("loans")
            n = 0
            found = False
            #پیدا کردن درخواست های تایید نشده
            for request in loans:
                n += 1
                if request["status"] != "approved":
                    print(n, ":", request)
                    found = True
            #فعال شدن گزینه های جدید در صورت وجود درخواست تایید نشده
            if found:
                print("1.Approval of requests \n 2.rejection of requests \n 3.Exit")
                choice = input("choose:").strip()
                #رفتن به قبول درخواست ها
                if choice == "1":
                    #وارد کردن شماره درخواست
                    print("Enter the requests' number with spaces:")
                    choice = input("choose:").split()
                    found = False
                    #مرتب کردن شماره درخواست های وارد شده به صورت ریورس
                    indexes = sorted([int(I) - 1 for I in choice], reverse=True)
                    for i in indexes:
                        #برسی وضعیت های مختلف
                        if loans[i]["status"] == "pending":
                            loans[i]["status"] = "approved"
                            #ثبت تاریخ درخواست و بازگشت کتاب
                            loans[i]["request date"] =f"{today}"
                            loans[i]["return date"] =f"{five_days_later}"
                            #برداشتن موضوع کتاب برای کم کردن تعداد موجودی کتاب
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] -= 1
                            #وارد کردن لیست جدید
                            write_json(books, "books")
                            found = True

                        elif loans[i]["status"] == "returned":
                            #برداشتن موضوع کتاب برای افزایش موجودی
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] += 1
                            #حذف از لیست درخواست ها
                            loans.remove(loans[i])
                            #وارد کردن لیست جدید
                            write_json(books, "books")
                            found = True

                        elif loans[i]["status"] == "renew_pending":
                            loans[i]["status"] = "approved"
                            #ثبت تاریخ درخواست و بازگشت کتاب
                            loans[i]["request date"] =f"{today}"
                            loans[i]["return date"] =f"{five_days_later}"
                            found = True
                        #وارد کردن لیست جدید
                        write_json(loans, "loans")
                    #اعلام پیدا نشدن شماره درخواست
                    if not found:
                        print("<<Not found>>")
                        continue
                    if found:
                        print("<<done>>")
                #رفتن به رد کردن درخواست ها
                elif choice == "2":
                    print("Enter the requests' number with spaces:")
                    choice = input("choose:").split()
                    found = False
                    #چینش برعکس شماره درخواست ها
                    indexes = sorted([int(I) - 1 for I in choice], reverse=True)
                    for i in indexes:
                        #برسی وضعیت های مختلف
                        if loans[i]["status"] == "renew_pending":
                            #برداشتن موضوع کتاب برای حذف درخواست و افزایش موجودی
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] += 1

                            loans.remove(loans[i])
                            found = True
                        elif loans[i]["status"] == "pending":
                            found = True
                            #حذف درخواست
                            loans.remove(loans[i])
                        elif loans[i]["status"] == "returned":
                            found = True
                            loans[i]["status"] = "approved"
                        #وارد کردن فهرست جدید
                        write_json(loans, "loans")
                    if found:
                        print("<<done>>")
                    if not found:
                        print("<<Not found>>")
                        continue
                else:
                    continue
            if not found:
                print("<<Not Found>>")
        #رفتن به اضافه کردن کتاب
        elif choice == "2":
           
            while True:
                print("1.Add new book \n 2.Exit")
                choice = input("choose:").strip()
                #اضافه کردن کتاب جدید
                if choice == "1":
                    title = input("Enter title:").title()
                    booksdata = read_json("books")
                    #چک کردن عدم وجود کتاب از قبل
                    if (book["title"]==title for book in booksdata):
                        print("<<This book has already been added>>")
                        continue
                    author = input("Enter author:").title()
                    category = input("Enter category:").title()
                    total_count = int(input("Enter total_count:"))
                    #برسی وارد نکردن موجودی نامعتبر
                    if total_count < 0:
                        print("<<Invalid input>>")
                        continue
                    bookdata = {
                        "title": f"{title}",
                        "author": f"{author}",
                        "category": f"{category}",
                        "total_count": total_count,
                        "available_count": total_count,
                    }
                    booksdata = read_json("books")
                    #اضافه کردن تغییرات
                    booksdata.append(bookdata)
                    #وارد کردن لیست جدید
                    write_json(booksdata, "books")
                    print("<<done>>")
                else:
                    break
        #رفتن به ویرایش کتاب
        elif choice == "3":
            
            found = False
            #گرفتن اطلاعات مورد نیاز
            search = input("Enter title of book:").title()
            title = input("Enter new title:").title()
            author = input("Enter new author:").title()
            category = input("Enter new category:").title()
            total_count = int(input("Enter new total_count:"))
            available_count = int(input("Enter new available_count:"))
            bookdata = {
                "title": f"{title}",
                "author": f"{author}",
                "category": f"{category}",
                "total_count": total_count,
                "available_count": available_count,
            }
            booksdata = read_json("books")
            #برسی صحیح بودن اطلاعات
            if available_count > total_count or total_count < 0:
                print("<<Invalid input>>")
                continue
            for book in booksdata:
                if book["title"] == search:
                    book.update(bookdata)
                    found = True
                    print("<<done>>")
            if not found:
                print("<<not found>>")
            #وارد کردن لیست جدید
            write_json(booksdata, "books")

        #رفتن به حذف کتاب
        elif choice == "4":
            found = False
            search= input("Enter title of book:").title()
            booksdata = read_json("books")
            for book in booksdata:
                if book["title"] == search:
                    booksdata.remove(book)
                    print("<<done>>")
                    #وارد کردن لیست جدید
                    write_json(booksdata, "books")
                    found = True
            if not found:
                print("<<Not found>>")
        #رفتن به اضافه کردن کاربر
        elif choice == "5":
            while True:
                print("1.Add new user \n 2.Exit")
                choice = input("choose:").strip()
                #اضافه کردن کاربر جدید
                if choice == "1":
                    while True:
                        #گرفتن نام کاربری
                        username = (
                            input("Enter username's user:").strip().replace(" ", "")
                        )
                        users = read_json("users")
                        #برسی تکراری نبودن نام کاربری
                        if any(u["username"] == username for u in users):
                            print("<<This username is invalid>>")
                        else:
                            #گرفتن بقیه اطلاعات کاربر
                            full_name = input("Enter full_name's user:").title()
                            password = (
                                input("Enter password's user:").strip().replace(" ", "")
                            )
                            role = (
                                input("Enter role's user(admin/librarian/member):")
                                .lower()
                                .strip()
                            )
                            #برسی معتبر بودن نقش
                            if role not in ["admin", "librarian", "member"]:
                                print("<<Invalid role>>")
                                continue
                            user = {
                                "username": f"{username}",
                                "password": f"{password}",
                                "full_name": f"{full_name}",
                                "role": f"{role}",
                                "is_active": True,
                            }
                            #اضافه کردن کاربر و وارد کردن لیست جدید
                            users.append(user)
                            write_json(users, "users")
                            print("<<done>>")
                            break
                else:
                    break
        #رفتن به حذف کاربر
        elif choice == "6":
            username = input("Enter username's user:")
            users = read_json("users")
            found = False
            #پیدا کردن کاربر 
            for user in users:
                if user["username"] == username:
                    users.remove(user)
                    write_json(users, "users")
                    found = True
                    print("<<done>>")
            if not found:
                print("<<Not found>>")
        #رفتن به فعال/غیرفعال کردن کاربر
        elif choice == "7":
            found = False
            search = input("Enter  user's username:").strip()
            users = read_json("users")
            #پیدا کردن کاربر
            for user in users:
                if user["username"] == search:
                    #وارونه کردن وضعیت کاربر
                    user["is_active"] = not user["is_active"]
                    print(
                        "<<User activated>>"
                        if user["is_active"]
                        else "<<User deactivated>>"
                    )
                    #وارد کردن لیست جدید
                    write_json(users, "users")
                    found = True
            if not found:
                print("<<Not found>>")
        #رفتن به فهرست کاربران
        elif choice == "8":
            users = read_json("users")
            for u in users:
                print(u)
        #رفتن به فهرست کتاب ها
        elif choice == "9":
            books = read_json("books")
            for u in books:
                print(u)
        #رفتن به فهرست قرض ها
        elif choice == "10":
            loans = read_json("loans")
            for u in loans:
                print(u)

        else:
            break
    except:
        print("<<invalid input>>")
#کلیر کردن ترمینال
import os

os.system("cls" if os.name == "nt" else "clear")
import json
#حذف کردن اطلاعات کاربر از فایل موقت
with open("user_data.json", "w") as d:
    json.dump({}, d)
