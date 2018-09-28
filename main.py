from testrail import *
import json
import matplotlib.pyplot as plt
import time
import jsonLoader
import os
import re

config = jsonLoader.load_json("config\\config.json")
client = APIClient(config["host"])
client.user = config["user"]
client.password = config["password"]

t1 = time.time()
tests = client.send_get('get_tests/555')
t2 = time.time()

print(len(tests))
print("Requires {}".format(t2 - t1))

estore = []
testRunResults = client.send_get('get_results_for_run/555')
t3 = time.time()
for test in tests:
    if test['custom_automated_selenium_profile'] == 'INWK.ShoppingCart.srprofile':
        estore.append(test)
t4 = time.time()
print(len(estore))
print("requires {}".format(t4 - t3))
with open('output.json', 'w') as outf:
    json.dump(estore, outf)

body = ""
countOfPassed = 0
countOfRetest = 0
countOfUntested = 0
countOfFailed = 0
reportLink = ""
t5 = time.time()
for e in estore:
    result = ""
    testComment = ""
    urlFromComment = ""
    if e['status_id'] == 1:
        countOfPassed = countOfPassed + 1
        result = "Passed"
    if e['status_id'] == 4:
        countOfRetest = countOfRetest + 1
        result = "Retest"
        t7 = time.time()
        testComment = client.send_get(f"get_results_for_case/555/{e['case_id']}&limit=1")
        t8 = time.time()
        print(f'Request require {t8-t7}')
        urlFromComment = re.search('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', testComment[0]['comment']).group()
    if e['status_id'] == 3:
        countOfUntested = countOfUntested + 1
        result = "Untested"
    if e['status_id'] == 5:
        countOfFailed = countOfFailed + 1
        result = "Failed"
    body = body + "<tr>" \
                  f"<td class = 'caseId'> C{e['case_id']} </td>\n" \
                  "<td class = 'caseTitle'> 5 </td>\n" \
                  "<td class = 'casePriority'> Major </td>\n" \
                  "<td class = 'caseFailureMessage'> Failure </td>\n" \
                  f"<td class = 'casePredictedReason'> <a href = '{urlFromComment}'>{result} </a> </td>\n" \
                  "</tr>\n"
body = body + "<tr>" \
              "<td class = 'totalCount'>Total count:" \
              f"{countOfPassed + countOfRetest + countOfUntested + countOfFailed}"\
              "</td>\n" \
              "</tr>\n"
t6 = time.time()
print(f'Creating of report require {t6-t5}')
labels = ['Retest', 'Untested', 'Passed', 'Failed']
values = [countOfRetest, countOfUntested, countOfPassed, countOfFailed]
colors = ['gold', 'lightskyblue', 'yellowgreen', 'lightcoral']
explode = (0.1, 0, 0, 0.1)

plt.pie(values, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.savefig("img/plt.png")

template = """
    <html>
    <head>
    <title>Template {}</title>
    </head>
    <body>
    <table style="position: absolute;width: 50%;">
    {}   
    </table>
    <img src="../img/plt.png" style="position: absolute;width: 49%;margin-left: 50%;">
    </body>
    </html>
    """.format('Estore', body)
if not os.path.exists('htmlReport'):
    os.mkdir('htmlReport')
htmlFile = open('htmlReport/index.html', 'w')
htmlFile.write(template)
htmlFile.close()
