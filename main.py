from datetime import datetime

def hello():
    return f"MTI Engine initialisé : {datetime.now()}"


if __name__ == "__main__":
    print(hello())
