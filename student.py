import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.indiabix.com/general-knowledge/sports/"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, "html.parser")

question_tags = soup.find_all("div", class_="bix-td-qtxt table-responsive w-100")
option_blocks = soup.find_all("div", class_="bix-tbl-options")
answer_blocks = soup.find_all("div", class_="bix-div-answer")

data = []

for q_tag, opt_block, ans_block in zip(question_tags, option_blocks, answer_blocks):
    question = q_tag.get_text(strip=True)
    options_raw = opt_block.find_all("div", class_="flex-wrap")
    options = [opt.get_text(strip=True) for opt in options_raw[:4]]
    
    # Pad missing options
    while len(options) < 4:
        options.append("")

    # Extract correct answer letter
    answer_letter_tag = ans_block.find("span", class_="option-svg-letter")
    answer_letter = answer_letter_tag.get_text(strip=True).upper() if answer_letter_tag else ""

    # Add each item as a separate row
    data.append({"Type": "Q", "Text": question})
    data.append({"Type": " ", "Text": f"A: {options[0]}"})
    data.append({"Type": " ", "Text": f"B: {options[1]}"})
    data.append({"Type": " ", "Text": f"C: {options[2]}"})
    data.append({"Type": " ", "Text": f"D: {options[3]}"})
    data.append({"Type": " ", "Text": f"Answer: {answer_letter}"})

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("mcq_indiabix_rows.xlsx", index=False)

print("✅ Scraped MCQs with answers (in separate rows) saved to mcq_indiabix_rows.xlsx")

'''import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.indiabix.com/general-knowledge/sports/013001"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, "html.parser")

question_tags = soup.find_all("div", class_="bix-td-qtxt table-responsive w-100")
option_blocks = soup.find_all("div", class_="bix-tbl-options")
answer_blocks = soup.find_all("div", class_="bix-div-answer")

lines = []  # collect lines instead of rows

for q_tag, opt_block, ans_block in zip(question_tags, option_blocks, answer_blocks):
    question = q_tag.get_text(strip=True)
    options_raw = opt_block.find_all("div", class_="flex-wrap")
    options = [opt.get_text(strip=True) for opt in options_raw[:4]]
    
    # Pad missing options
    while len(options) < 4:
        options.append("")

    # Extract correct answer letter
    answer_letter_tag = ans_block.find("span", class_="option-svg-letter")
    answer_letter = answer_letter_tag.get_text(strip=True).lower() if answer_letter_tag else ""

    # Add each item as a separate line
    lines.append(f"Q {question}")
    lines.append(f"a) {options[0]}")
    lines.append(f"b) {options[1]}")
    lines.append(f"c) {options[2]}")
    lines.append(f"d) {options[3]}")
    lines.append(f"Answer: {answer_letter}")
    lines.append("")  # Empty line for spacing between questions

# Save to text file
with open("mcq_indiabix_rows.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("✅ Scraped MCQs with answers saved to mcq_indiabix_rows.txt")
'''