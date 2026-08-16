import re

def mock_parse(description: str) -> dict:
    original = description
    text = description.lower()

    # Priority
    priority = "medium"
    if "urgent" in text or "asap" in text:
        priority = "high"
    elif "whenever" in text or "low priority" in text:
        priority = "low"

    # Due date hint
    due_date_hint = None
    date_phrases = [
        "next monday", "next tuesday", "next wednesday", "next thursday",
        "next friday", "next saturday", "next sunday",
        "today", "tomorrow", "next week",
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ]

    for phrase in date_phrases:
        if phrase in text:
            due_date_hint = phrase
            break

    # Title cleaning - remove priority and date keywords
    title = original
    remove_words = ["urgent", "asap", "whenever", "low priority"] + date_phrases

    for word in remove_words:
        title = re.sub(r'\b' + re.escape(word) + r'\b', '', title, flags=re.IGNORECASE)

    # Clean extra spaces and punctuation leftovers
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'\s+,', ',', title)
    title = title.strip(' ,')

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date_hint
    }