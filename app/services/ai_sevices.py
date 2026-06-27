

class AIServices:

    @staticmethod
    def analyze_ticket(title: str, description: str):
        text = f"{title} {description}".lower()
        category = "General"
        priority = "MEDIUM"
        summary = description
        suggestion = "Support team will investigate."
        if "login" in text:
            category = "Authentication"
            priority = "HIGH"
            suggestion = "Verify credentials and reset password."
        elif "database" in text:
            category = "Database"
            priority = "HIGH"
            suggestion = "Check database connectivity."
        elif "network" in text:
            category = "Network"
            priority = "HIGH"
            suggestion = "Check firewall and network availability."

        return {
            "category": category,
            "priority": priority,
            "summary": summary,
            "suggested_resolution": suggestion
        }