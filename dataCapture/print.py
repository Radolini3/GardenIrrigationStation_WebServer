import re

data = '123:Palo Alto, CA -> 456:Seattle, WA 789'
citys = []
for record in data.split("->"):
    citys.append(
        re.search(r":(?P<city>[\w\s]+),\s*(?P<state>[\w]+)",record)
        .groupdict()
    )

print(citys)
