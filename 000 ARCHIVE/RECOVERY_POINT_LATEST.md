Project Summary — Recovery Point: regular_stakes.py script working well
Date: 2025/04/26
Saved by: TF

1. Business/Project Context
Company: Print & Sign Company, Alnwick (update as needed)
Main Focus: Generic signage, personalized memorials, local large-format signage, etc.
Sales Channels: Amazon (EU/US/AU), Etsy, eBay, Website, Local
Production Methods: CNC, Laser, UV, Sublimation, etc.
2. Objectives at this Point
[x] Automate personalized memorial product design
[x] Develop Amazon reporting/account management tools
[x] Shipping automation (Zenstores, SP-API)
[ ] [Other goals or milestones]
3. Current Project Structure
Data Extraction: 001 AMAZON DATA DOWNLOAD/
Order Review & GUI: main_gui.py
Stake/Product Processing: 002 D2C WRITER/
Output: SVG_OUTPUT/
Other: [Add any new or changed folders/scripts as needed]
4. Recent Changes / Progress
Dynamic Text Sizing:
Line 1 and Line 2 text sizes increased by 20%.
Line 3 font size is dynamic:
10–30 chars: same as Line 1
31–90 chars: 90% of Line 1
90 chars: smaller, original Line 3 size

Line 3 Wrapping:
Text is split and wrapped using textwrap, max 5 lines.
Carriage returns (\n) inserted between split lines for easier editing.
Robust SVG Line Spacing:
All lines after the first in Line 3 use dy="1.2em" for proportional, non-overlapping spacing.
Grammar & Typo Checks:
Detects extra spaces before punctuation, future dates, and capitalization issues.
Graphics Handling:
Embeds user-specified graphics, with error handling for missing files.
Batch Processing:
3x3 grid layout per SVG batch, with batch CSVs generated.
Reference Point:
Small blue square in the SVG corner for print alignment.
GUI Integration:
"Create Regular Stake SVGs" button in main_gui.py now triggers SVG generation, passing correct output and graphics paths to regular_stakes.py.
Error handling added for missing output.csv.
5. Known Issues / Blockers
None currently identified.
6. Next Steps / TODO
Continue visual testing with a variety of real orders.
Consider advanced grammar/spell-check integration.
Keep documentation and requirements up to date.
Expand automation to other product types or sales channels as needed.
7. Environment & Dependencies
Python version: 3.11 (update if different)
Key packages: pandas, svgwrite, textwrap, re, datetime, tkinter, selenium, etc.
Virtual environment: .venv recommended; ensure requirements.txt is current.
External APIs: Awaiting Amazon SP-API access (if not already configured).
8. Backup Artifacts
[ ] Code committed to version control? (commit hash: ______)
[ ] Output CSV/SVG files backed up?
[ ] requirements.txt/environment.yml saved?
9. Notes
The script and batch processing logic are now robust and visually reliable.
All recent enhancements are included in this recovery point.
For future edits, refer to this summary for context and rationale.
If you need to restore, audit, or share this recovery point, this summary contains all key technical and business details up to this milestone.
This summary is suitable for backup, audit, or team handover. If you require a more detailed breakdown of any section, or a full code snapshot, just ask!