def lecture_for(error: dict) -> str:
    code = error.get("code","")
    err = error.get("error","")
    why = error.get("why","")

    parts = []
    parts.append("❌ WHAT YOU TRIED:\n" + code + "\n")
    parts.append("🧠 WHAT PYTHON EXPECTED:\nPython follows strict syntax rules.\n")
    parts.append("⚠ WHY PYTHON COMPLAINS:\n" + why + "\n")
    parts.append("✅ HOW PROFESSIONALS FIX IT:\n")

    if "unterminated string" in err.lower():
        parts.append("Strings must start AND end with matching quotes:\nprint('Hello')\n")
    elif "expected ':'" in err:
        parts.append("Conditions must end with ':'\nif condition:\n    pass\n")
    elif "indentation" in err.lower():
        parts.append("Blocks must be indented consistently (4 spaces).\n")
    elif "nameerror" in err.lower():
        parts.append("Define variables before using them and match capitalization.\n")
    else:
        parts.append("Read the error message carefully and correct the syntax.\n")

    return "\n".join(parts)