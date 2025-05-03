Here is your updated project summary restore point as of 2025-04-28:

🚩 Project Restore Point: Amazon Seller Memorial Stake Automation
Date: 2025/04/28
Saved by: TF

1. Business/Project Context
Company: [e.g. Print & Sign Company, Alnwick]
Focus: Automated personalized memorial product design, Amazon/Etsy/eBay order management, and shipping automation.
Sales Channels: Amazon (EU/US/AU), Etsy, eBay, Website, Local
Production: CNC, Laser, UV, Sublimation, etc.
2. Objectives at This Point
[x] Automate personalized memorial product design (SVG generation)
[x] Develop Amazon reporting/account management tools
[x] Shipping automation (Zenstores, SP-API)
[ ] [Other goals or milestones as needed]
3. Current Project Structure
Data Extraction: 001 AMAZON DATA DOWNLOAD/
Order Review & GUI: main_gui.py
Stake/Product Processing: 002 D2C WRITER/ (e.g., regular_stakes.py, coloured_large_stakes.py)
Output: SVG_OUTPUT/
Other: requirements.txt, environment management, backup scripts
4. Recent Changes / Progress
regular_stakes.py updated to:
Accept the colours 'stone' and 'marble' in the COLOUR column.
Accept 'regular plaque' in the TYPE column.
Improved robustness for missing/non-string fields in grammar/typo checks.
Filtering and batch processing logic confirmed to work for new types/colours.
Restore point created after successful code and logic update.
5. Known Issues / Blockers
Some rows in output.csv may still be skipped if they do not meet the updated filter criteria.
Ongoing need to keep requirements.txt and virtual environment in sync.
6. Next Steps / TODO
Consider logging skipped rows and reasons for exclusion for easier debugging.
Continue development of new stake types and automation features.
Regularly update and backup requirements.txt and other environment files.
7. Environment & Dependencies
Python version: 3.11+ (confirmed working with 3.11/3.13)
Key packages: pandas, svgwrite, tkinter, selenium, etc.
Virtual environment: .venv active, requirements.txt up to date
External APIs: Awaiting Amazon SP-API access
8. Backup Artifacts
[x] Code committed to version control (commit hash: ______)
[x] Output CSV/SVG files backed up
[x] requirements.txt/environment.yml saved
9. Notes
Filtering logic is now more inclusive for new product types and colours.
Restore point created after a successful code update and test run.
If you need to roll back to this state, reference this restore point and the date.
Let me know if you want this summary saved to a file or committed to version control!