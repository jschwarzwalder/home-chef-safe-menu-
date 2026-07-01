from bs4 import BeautifulSoup

file_path = r"C:\Users\jschw\GitHub\home-chef-safe-menu\repo\data\Home Chef Meal Delivery Service, Fresh Ingredients to Cook at Home _ Home Chef.html"

with open(file_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Print page title first (sanity check)
print("TITLE:", soup.title.text if soup.title else "No title")

# Dump some candidate text chunks
texts = soup.stripped_strings

count = 0
for t in texts:
    print(t)
    count += 1
    if count > 200:
        break