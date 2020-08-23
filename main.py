from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path
from atexit import register
from time import sleep
from lxml.html import fromstring
from collections import defaultdict


SEM = "2020W"


def collapse_whitespace(s):
    return ' '.join(s.split())


driver = Chrome(executable_path=binary_path)
driver.set_window_rect(0, 0, 1280, 1024)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

register(driver.quit)

driver.get("https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=5025&dsrid=300&key=64576")
Select(driver.find_element_by_id("j_id_2e:semesterSelect")).select_by_value(SEM)

wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "tbody.ui-datatable-data"), "Random walks on graphs"))
html = driver.find_element_by_css_selector("tbody.ui-datatable-data").get_attribute("innerHTML")
soup = fromstring(html)

data = defaultdict(list)
current_subject = ""
for row in soup.cssselect("tr"):
    cells = row.cssselect("td")
    classes = cells[0].cssselect("div")[0].get("class")
    if "nodeTable-level-2" in classes and cells[0].cssselect("div > span.bold"):
        current_subject = cells[0].text_content().strip()
        print(f"\n{current_subject}")
        print("-"*128)
    elif "nodeTable-level-4" in classes:
        links = row.cssselect("div.courseTitle > a")
        if links:
            cnum, kind, sem, title = collapse_whitespace(cells[0].text_content().strip().replace("\n", " ")).split(maxsplit=3)
            assert sem == SEM
            print(cnum, "    ", kind, " hugo ", title, links[0].get("href"))
            data[current_subject].append({
                'cnum': cnum,
                'kind': kind,
                'title': title,
                'link': links[0].get("href")
            })
        else:
            raise ValueError("No link for", cells[0].text_content())

sleep(1e6)