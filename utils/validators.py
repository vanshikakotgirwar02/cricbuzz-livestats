
def validate_non_empty(value, field_name="Field"):
    """Check that a required text field is not empty."""
    if value is None or not str(value).strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_positive_integer(value, field_name="Value"):
    """Check that a value is a positive integer or zero."""
    try:
        number = int(value)
        if number < 0:
            return False, f"{field_name} cannot be negative."
        return True, ""
    except (TypeError, ValueError):
        return False, f"{field_name} must be a whole number."


def validate_match_format(match_format):
    """Allow common cricket match formats."""
    allowed_formats = {"Test", "ODI", "T20", "T10"}
    if match_format not in allowed_formats:
        return False, "Choose Test, ODI, T20, or T10."
    return True, ""


def validate_match_status(status):
    """Allow known match statuses."""
    allowed_statuses = {"Scheduled", "Live", "Completed", "Abandoned"}
    if status not in allowed_statuses:
        return False, "Invalid match status."
    return True, ""
