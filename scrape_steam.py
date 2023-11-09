# open web page (URL) in python
import requests
import lxml.html

# open up web page
html = requests.get("https://store.steampowered.com/explore/new/")
# pass response
doc = lxml.html.fromstring(html.content)
new_releases = doc.xpath("//div[@id='tab_newreleases_content']")[0]
titles = new_releases.xpath(".//div[@class='tab_item_name']/text()")
prices = new_releases.xpath(".//div[@class='discount_final_price']/text()")
tags_divs = new_releases.xpath(".//div[@class='tab_item_top_tags']")
tags = []
for div in tags_divs:
    # text_content() returns the text contained within an HTML tag without the HTML markup
    tags.append(div.text_content())

platforms_div = new_releases.xpath(".//div[@class='tab_item_details']")
total_platforms = []

for game in platforms_div:
    temp = game.xpath(".//span[contains(@class,'platform_img')]")
    platforms = [t.get("class").split(" ")[-1] for t in temp]
    if "hmd_separator" in platforms:
        platforms.remove("hmd_separator")
    total_platforms.append(platforms)

output = []

for info in zip(titles, prices, tags, total_platforms):
    resp = {}
    resp['Title'] = info[0]
    resp['Price'] = info[1]
    resp['Tags'] = info[2]
    resp['Platforms'] = info[3]
    output.append(resp)

print(sorted(output, key=lambda i: i['Price'], reverse=True))






