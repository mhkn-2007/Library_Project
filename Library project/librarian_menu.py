def read_json(x):
    import json

    with open(x + ".json", "r") as r:
        data = json.load(r)
        return data


def write_json(y, x):
    import json

    with open(x + ".json", "w") as w:
        json.dump(y, w)


from datetime import date, timedelta

today = date.today()
five_days_later = today + timedelta(days=5)


while True:
    try:
        print("\n \n \n \n")
        print("help:At each step, press Enter continuously to return to the main menu.")
        print(
            " Menu:\n1.View and manage requests \n 2.Add book\n 3.Edit the book\n 4.delete the book\n 5.Users list \n 6.Books list \n7.Loans list \n 8.Exit"
        )
        choice = input("choose:").strip()
        if choice == "1":
            loans = read_json("loans")
            n = 0
            found = False
            for request in loans:
                n += 1
                if request["status"] != "approved":
                    print(n, ":", request)
                    found = True
            if found:
                print("1.Approval of requests \n 2.rejection of requests \n 3.Exit")
                choice = input("choose:").strip()
                if choice == "1":
                    print("Enter the requests' number with spaces:")
                    choice = input("choose:").split()
                    found = False
                    indexes = sorted([int(I) - 1 for I in choice], reverse=True)
                    for i in indexes:
                        if loans[i]["status"] == "pending":
                            loans[i]["status"] = "approved"
                            loans[i]["request date"] = today.isoformat()
                            loans[i]["return date"] = five_days_later.isoformat()
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] -= 1
                            write_json(books, "books")
                            found = True

                        elif loans[i]["status"] == "returned":
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] += 1
                            loans.remove(loans[i])

                            write_json(books, "books")
                            found = True

                        elif loans[i]["status"] == "renew_pending":
                            loans[i]["status"] = "approved"
                            loans[i]["request date"] = today.isoformat()
                            loans[i]["return date"] = five_days_later.isoformat()
                            found = True
                        write_json(loans, "loans")
                    if not found:
                        print("<<Not found>>")
                        continue
                    if found:
                        print("<<done>>")

                elif choice == "2":
                    print("Enter the requests' number with spaces:")
                    choice = input("choose:").split()
                    found = False
                    indexes = sorted([int(I) - 1 for I in choice], reverse=True)
                    for i in indexes:
                        if loans[i]["status"] == "renew_pending":
                            title = loans[i]["book_title"]
                            books = read_json("books")
                            for book in books:
                                if book["title"] == title:
                                    book["available_count"] += 1

                            loans.remove(loans[i])
                            found = True
                        elif loans[i]["status"] == "pending":
                            found = True
                            loans.remove(loans[i])
                        elif loans[i]["status"] == "returned":
                            found = True
                            loans[i]["status"] = "approved"
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
        elif choice == "2":
            try:
                while True:
                    print("1.Add new book \n 2.Exit")
                    choice = input("choose:").strip()
                    if choice == "1":
                        title = input("Enter title:").title()
                        author = input("Enter author:").title()
                        category = input("Enter category:").title()
                        total_count = int(input("Enter total_count:"))
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
                        booksdata.append(bookdata)
                        write_json(booksdata, "books")
                        print("<<done>>")
                    else:
                        break
            except:
                print("<<invalid input>>")

        elif choice == "3":
            try:
                found = False
                search1 = input("Enter title of book:").title()
                search2 = input("Enter author of book:").title()
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
                if available_count > total_count or total_count < 0:
                    print("<<Invalid input>>")
                    continue
                for book in booksdata:
                    if book["title"] == search1 and book["author"] == search2:
                        book.update(bookdata)
                        found = True
                        print("<<done>>")
                if not found:
                    print("<<not found>>")
                write_json(booksdata, "books")
            except:
                print("<<invalid input>>")

        elif choice == "4":
            found = False
            search1 = input("Enter title of book:").title()
            search2 = input("Enter author of book:").title()
            booksdata = read_json("books")
            for book in booksdata:
                if book["title"] == search1 and book["author"] == search2:
                    booksdata.remove(book)
                    print("<<done>>")
                    write_json(booksdata, "books")
                    found = True
            if not found:
                print("<<Not found>>")

        elif choice == "5":
            users = read_json("users")
            for u in users:
                print(u)

        elif choice == "6":
            books = read_json("books")
            for u in books:
                print(u)

        elif choice == "7":
            loans = read_json("loans")
            for u in loans:
                print(u)

        else:
            break
    except:
        print("<<invalid input>>")

import os

os.system("cls" if os.name == "nt" else "clear")
import json

with open("user_data.json", "w") as d:
    json.dump({}, d)

