import pickle


def open_browser():
    import webbrowser

    webbrowser.open("https://digital.alfabank.ru/vacancies")


class MyClass:
    def __init__(self, name: str, company: str):
        self.name = name
        self.company = company

    def __reduce__(self):
        return (open_browser, ())
