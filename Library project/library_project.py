import os
print("<<Hi>>")
attemps = 0
while attemps <= 2:
    #دریافت نام کاربری و رمز عبور و انتخاب نقش 
    username = input("Enter username:").strip().replace(" ", "")
    password = input("Enter password:").strip().replace(" ", "")
    role = input("Enter role(1.Admin 2.Librarian 3.Member):")

    if role == "1":
        role = "admin"
    elif role == "2":
        role = "librarian"
    elif role == "3":
        role = "member"
    data = False
    import json
#باز کردن فایل فهرست مشخصات کاربران برای صحت سنجی اطلاعات ورودی کاربر
    with open("users.json", "r") as d:
        users = json.load(d)
    for user in users:
        if (
            user["username"] == username
            and user["password"] == password
            and user["role"] == role
            and user["is_active"]
        ):
            data = True
#وارد کردن اطلاعات ضروری کاربر به فایل موقت در صورت  درست بودن اطلاعات 
            user_data = {
                "username": f"{username}",
                "password": f"{password}",
                "role": f"{role}",
            }
            with open("user_data.json", "w") as d:
                json.dump(user_data, d)

            break
#پیام هشدار درصورت وارد کردن اطلاعات اشتباه
    if not data:
        attemps += 1
        os.system("cls" if os.name == "nt" else "clear")
        print("<<Username and password did not match or User is inactive>>")
        continue
    break

if attemps <= 2:
    if data:
        #خوش آمد گویی
        print(f"<<Welcome {user["full_name"]}>>")
    #رفتن به منو ادمین
    if role == "admin":
        import admin_menu
    #رفتن به منو کتابدار
    elif role == "librarian":
        import librarian_menu
    #رفتن به منو اعضاء
    else:
        import members_menu
else:
    print(
        """<<The number of login attempts has exceeded the allowed limit.

Please try again later.>>"""
    )
