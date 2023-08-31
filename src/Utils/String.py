def pluralise(snippets: list[str]) -> str:
    if len(snippets) == 1:
        return snippets[0]
    else:
        return ", ".join(snippets[:-1]) + " and " + snippets[-1]
