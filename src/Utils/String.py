def pluralise(snippets: list[str]) -> str:
    if len(snippets) == 1:
        return snippets[0]
    else:
        return ", ".join(snippets[:-1]) + " and " + snippets[-1]


def getOrdinal(num: int) -> str:
    last = num % 10

    if last == 1:
        return f"{num}st"
    elif last == 2:
        return f"{num}nd"
    elif last == 3:
        return f"{num}rd"
    else:
        return f"{num}th"
