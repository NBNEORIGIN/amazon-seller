import os
from datetime import datetime

# Directory where the recovery point will be saved
PROJECT_DIR = r"G:\My Drive\003 APPS\002 AmazonSeller"

def prompt(msg, default=""):
    val = input(f"{msg} [{default}]: ")
    return val.strip() or default

def main():
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    fname_str = now.strftime("%Y%m%d_%H%M")
    filename = f"RECOVERY_POINT_{fname_str}.md"
    filepath = os.path.join(PROJECT_DIR, filename)

    # Prompt user for details
    desc = prompt("Short description for this recovery point", "Checkpoint")
    author = prompt("Saved by", "Your Name")
    changes = prompt("Recent changes/progress", "-")
    blockers = prompt("Known issues/blockers", "-")
    next_steps = prompt("Next steps/TODO", "-")

    # Template content
    content = f"""# 🚩 Recovery Point: {desc}  
**Date:** {date_str}  
**Saved by:** {author}

---

## 1. **Business/Project Context**
- **Company:** [e.g. Print & Sign Company, Alnwick]
- **Main Focus:** [Generic signage, personalized memorials, local large-format signage, etc.]
- **Sales Channels:** [Amazon (EU/US/AU), Etsy, eBay, Website, Local]
- **Production:** [CNC, Laser, UV, Sublimation, etc.]

---

## 2. **Objectives at this Point**
- [ ] Automate personalized memorial product design
- [ ] Develop Amazon reporting/account management tools
- [ ] Shipping automation (Zenstores, SP-API)
- [ ] [Other goals or milestones]

---

## 3. **Current Project Structure**
- **Data Extraction:** `001 AMAZON DATA DOWNLOAD/`
- **Order Review & GUI:** main_gui.py
- **Stake/Product Processing:** `002 D2C WRITER/`
- **Output:** `SVG_OUTPUT/`
- **Other:** [List any new or changed folders/scripts]

---

## 4. **Recent Changes / Progress**
- {changes}

---

## 5. **Known Issues / Blockers**
- {blockers}

---

## 6. **Next Steps / TODO**
- {next_steps}

---

## 7. **Environment & Dependencies**
- **Python version:** [e.g. 3.11]
- **Key packages:** [e.g. pandas, svgwrite, tkinter, selenium, etc.]
- **Virtual environment:** [.venv active? requirements.txt up to date?]
- **External APIs:** [e.g. Awaiting Amazon SP-API access]

---

## 8. **Backup Artifacts**
- [ ] Code committed to version control? (commit hash: `______`)
- [ ] Output CSV/SVG files backed up?
- [ ] requirements.txt/environment.yml saved?

---

## 9. **Notes**
- [Any additional context, ideas, or reminders for future sessions.]

---
"""

    # Write the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Recovery point saved to: {filepath}")

    # Optionally, update a latest pointer file for quick access
    latest_path = os.path.join(PROJECT_DIR, "RECOVERY_POINT_LATEST.md")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Latest recovery point also saved to: {latest_path}")

if __name__ == "__main__":
    main()
