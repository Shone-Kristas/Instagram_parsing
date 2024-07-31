import instaloader
import argparse
import csv

# Аутентификация
def auth_instagram(username, password, L):
    try:
        L.login(username, password)
    except instaloader.exceptions.BadCredentialsException:
        print("Invalid credentials")
    except instaloader.exceptions.ConnectionException:
        print("Connection error")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Загрузка профиля
def load_profile(scan_username, L):
    try:
        profile = instaloader.Profile.from_username(L.context, username=scan_username)
        followers = profile.get_followers()
        print(f"Количество подписчиков: {profile.followers}")
        with open('followers.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Username'])  # Заголовок
            for follower in followers:
                writer.writerow([follower.username])
        print("Данные успешно записаны в followers.csv")
    except instaloader.exceptions.ConnectionException:
        print("Failed to connect")
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Создаем объект Instaloader
    L = instaloader.Instaloader()

    parser = argparse.ArgumentParser(
        description="Instagram Parser"
    )

    parser.add_argument("username", type=str, help="Your account name: (your_account@example.com)")
    parser.add_argument("password", type=str, help="Your account password: (password)")
    parser.add_argument("scan_username", type=str, help="Account name for parse: (without @)")
    args = parser.parse_args()

    username = args.username
    password = args.password
    scan_username = args.scan_username

    auth_instagram(username, password, L)
    load_profile(scan_username, L)


if __name__ == "__main__":
    main()