from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path
from atexit import register
from lxml.html import fromstring
from collections import defaultdict
from json import dump
import pendulum
pendulum.set_locale('de')


SEM = "2020W"
semesters = [SEM, f"{int(SEM[:4])-1}{SEM[-1]}"]


def collapse_whitespace(s):
    return ' '.join(s.split())


driver = Chrome(executable_path=binary_path)
driver.set_window_rect(0, 0, 1280, 1024)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

register(driver.quit)

driver.get("https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=5025&dsrid=300&key=64576")

data = defaultdict(list)
for semester in semesters:
    driver.get("https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=5025&dsrid=300&key=64576")
    Select(driver.find_element_by_id("j_id_2e:semesterSelect")).select_by_value(semester)

    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "tbody.ui-datatable-data"), "Ausgewählte Kapitel der Wahrscheinlichkeitstheorie (AKWTH)"))
    html = driver.find_element_by_css_selector("tbody.ui-datatable-data").get_attribute("innerHTML")
    soup = fromstring(html)

    current_subject = ""
    for row in soup.cssselect("tr"):
        cells = row.cssselect("td")
        classes = cells[0].cssselect("div")[0].get("class")
        if "nodeTable-level-1" in classes and cells[0].cssselect("div > span.bold"):
            current_subject = cells[0].text_content().strip()
            print(f"\n{current_subject}")
            print("-"*128)
        elif "nodeTable-level-4" in classes:
            links = row.cssselect("div.courseTitle > a")
            if links:
                cnum, kind, sem, title = collapse_whitespace(cells[0].text_content().strip().replace("\n", " ")).split(maxsplit=3)
                if sem not in semesters:
                    continue
                link = links[0].get("href")
                assert link[0] == '/'
                print(cnum, "    ", kind, title, link)

                cnums = set(map(lambda x: x['cnum'], data[current_subject]))
                if cnum not in cnums:
                    data[current_subject].append({
                        'cnum': cnum,
                        'kind': kind,
                        'sem': sem,
                        'title': title,
                        'link': link,
                        'ects': cells[3].text_content()
                    })
            else:
                raise ValueError("No link for", cells[0].text_content())

    assert len(data) > 0

with open("public/data.json", "w") as f:
    dump({
        'data': data,
        'sem': semesters,
        'updated': pendulum.now().format("dddd, DD. MMMM YYYY HH:mm:ss")
    }, f)