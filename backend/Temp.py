from bs4 import BeautifulSoup

with open("backend\Example HTMLs\DOTS.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")
    table_body = soup.find("tbody")
    table = []

    # Create a 2d list of the table
    for row in table_body.find_all("tr"):
        row_list = []
        for cell in row.find_all("td"):
            row_list.append(cell.text.strip().replace(
                "\n", "").replace("  ", ""))
        table.append(row_list)

temp = []
for row in table[1:]:
    row = [row[1], row[7]]
    temp.append(row)
table = temp
