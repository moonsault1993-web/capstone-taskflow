def mock_parse(description: str) -> dict:
    """
    Deterministic rule-based mock parser as specified in the assignment.
    """
    original = description
    text = description.lower()

    # Priority detection
    priority = "medium"
    if "urgent" in text or "asap" in text:
        priority = "high"
    elif "whenever" in text or "low priority" in text:
        priority = "low"

    # Due date detection
    due_date_hint = None
    date_phrases = [
        "today", "tomorrow", "next week",
        "next monday", "next tuesday", "next wednesday", "next thursday",
        "next friday", "next saturday", "next sunday",
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ]

    for phrase in date_phrases:
        if phrase in text:
            due_date_hint = phrase
            break

    # Title cleaning
    title = original
    keywords_to_remove = ["urgent", "asap", "whenever", "low priority"] + date_phrases

    for kw in keywords_to_remove:
        # case-insensitive replace
        import re
        title = re.sub(re.escape(kw), "", title, flags=re.IGNORECASE)

    title = " ".join(title.split()).strip()  # clean extra spaces
    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date_hint
    }