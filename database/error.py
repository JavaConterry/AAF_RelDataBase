class Error:
    def __init__(self) -> None:
        self.error = []

    def __add__(self, value) -> None:
        self.error += [value]
        return self

    def __str__(self) -> str:
        return "\n".join(self.error)


if __name__ == "__main__":
    err = Error()
    if err:
        print(err)
    err = err + "First Error"
    err += "Second Error"
    err = err + "Third Error"
    print(err)
    if err:
        print(err)
