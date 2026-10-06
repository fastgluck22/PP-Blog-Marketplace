def build_context(results) -> str:
    context_parts = []

    for article, distance in results:
        context_parts.append(
            f"Title: {article.title}\n"
            f"Text: {article.text}"

        )
    return "\n\n".join(context_parts)
