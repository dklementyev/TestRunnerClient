from testrail import *
import json
import matplotlib.pyplot as plt
import time


client = APIClient("{url}")
client.user = "{login}"
client.password = "{password}"


t1 = time.time()
tests = client.send_get('get_tests/555')
t2 = time.time()

print(len(tests))
print("Requires {}".format(t2-t1))

estore = []

t3= time.time()
for test in tests:
    if test['custom_automated_selenium_profile'] == '{selenium srprofile name}':
        estore.append(test)
t4 = time.time()
print(len(estore))
print("requires {}".format(t4-t3))
with open('output.json','w') as outf:
    json.dump(estore, outf)


body = ""
countOfPassed = 0
countOfRetest = 0
countOfUntested = 0
for e in estore:
    result = ""
    if e['status_id'] == 1:
        countOfPassed = countOfPassed + 1
        result = "Passed"
    if e['status_id'] == 4:
        countOfRetest = countOfRetest + 1
        result = "Retest"
    if e['status_id'] == 3:
        countOfUntested = countOfUntested + 1
        result = "Untested"
    body = body + "<tr>" \
                "<td class = 'caseId'> C{} </td>\n" \
                "<td class = 'caseTitle'> 5 </td>\n" \
                "<td class = 'casePriority'> Major </td>\n" \
                "<td class = 'caseFailureMessage'> Failure </td>\n" \
                "<td class = 'casePredictedReason'> {} </td>\n" \
                "</tr>\n" \
                "".format(e['case_id'], result)



labels = ['Retest', 'Untested', 'Passed']
values = [countOfRetest, countOfUntested, countOfPassed]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0)

plt.pie(values, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.savefig("plt.png")

template = """
    <html>
    <head>
    <title>Template {}</title>
    </head>
    <body>
    <table>
    {}
    </table>
    <img src = 'plt.png'/>
    </body>
    </html>
    """.format('Estore', body)

htmlFile = open('index.html','w')
htmlFile.write(template)
htmlFile.close()
