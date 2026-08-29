from config import BOT_TOKEN


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")
    print("Task-Bot scaffold ready")


if __name__ == "__main__":
    main()
