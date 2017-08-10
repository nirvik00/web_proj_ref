import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://spreadsheets.google.com/feeds']
creds=ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client=gspread.authorize(creds)

rel_sheet=client.open("adjacency_graph").sheet1
list_of_hashes=rel_sheet.get_all_records()
"""
columns go up-down vertical
rows go left-right horizontal
"""
row_li=rel_sheet.row_values(1)
row_count=len(row_li)
col_li=rel_sheet.col_values(1)
col_count=len(col_li)

relation_li=[]

print(str(row_count) + ", " + str(col_count))
print("going to import data...")
for i in range(2,col_count-1,1):
    for j in range(2,row_count-1,1):
        str_cell_val = rel_sheet.cell(i, j).value
        if(str_cell_val==""):
            pass
        else:
            relation_li.append([col_li[i-1], row_li[j-1], str_cell_val])

print("data imported")
final_relation_li=[]
for i in relation_li:
    s=""
    for j in i:
        s+=j+","
    final_relation_li.append(s)


for i in final_relation_li:
    print(i)