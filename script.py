def run_client():
    print("=== РЕЖИМ КЛІЄНТ ===")
    while True:
        message = input("Клієнт:")
        if message == "exit":
            print("СЕАНС завершенно")
            break
        print("Повідомлення відправлено серверу: {message}")
        a = input("Чекаем відповідь сервера...")
        if a == "exit":
            print("Клієнт закінчив сеанс")
            break

def run_server