import requests
from parsel import Selector
from time import sleep


page = 1
while page <= 25:
    print(f"Parsing page......{page}")
    r = requests.get(f"https://tanglepatterns.com/page/{page}")
    s = Selector(r.text)

    posts = s.xpath("//div[@class='post-headline']")
    for post in posts:
        img_name = post.xpath("./h2/a[contains(text(), 'How to draw')]/text()").get()
        if img_name:
            img_name = img_name.split("How to draw", 1)[1].strip()
            img_src = post.xpath("./../div[@class='post-bodycopy clearfix']//img/@src").get()

            r = requests.get(img_src)
            with open(f"statics/{img_name}.jpg", "wb") as f:
                f.write(r.content)

            print(f"{img_name}.jpg is saved.")
            sleep(1)

    sleep(5)
    page += 1
