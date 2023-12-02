"""
===ссылка:
<main class="vacancy-serp-content">
<div data-qa="vacancy-serp__results" id="a11y-main-content">
<a class="serp-item__title" data-qa="serp-item__title" target="_blank"
href="https://adsrv.hh.ru/click?b=762709&c=5&place=36&meta=JF6YWQDEkyRUmHxSqo…sjlAmbfeo4er2GZ6Mgk5W68BGzKlYA47BkWlt1BIzA%3D%3D&clickType=link_to_vacancy">Python Engineer</a>
===з\п:
<span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-2">
===название компании\город:
<div class="vacancy-serp-item__meta-info-company"
<div class="vacancy-serp-item__meta-info-company">
<div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Москва</div>
===Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".:
<span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">Django</span>
"""
from urllib.parse import urljoin
import bs4
import fake_headers
import requests
import json


url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
keyword_1 = "Django"
keyword_2 = "Flask"
# headers_gen = fake_headers.Headers(os="win", browser="chrome")
# response = requests.get(url, headers=headers_gen.generate())
# main_html_data = response.text
# main_soup = bs4.BeautifulSoup(main_html_data, "lxml")
vacancy_data = []

def get_vacancy():
    num = get_next_page()
    for page in range(1, num - 38):
        cur_url = url + f'&page={page}'
        headers_gen = fake_headers.Headers(os="win", browser="chrome")
        response = requests.get(cur_url, headers=headers_gen.generate())
        main_html_data = response.text
        main_soup = bs4.BeautifulSoup(main_html_data, "lxml")

        vacancy_list_tag = main_soup.find(name="div", id="a11y-main-content")
        vacancy_tags = vacancy_list_tag.find_all(class_="vacancy-serp-item-body__main-info")
        for vacancy_tag in vacancy_tags:
            company = vacancy_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
            company_add_tag = vacancy_tag.find("div", class_="vacancy-serp-item-company")
            h3_tag = vacancy_tag.find("h3", class_="bloko-header-section-3")
            span_tag = h3_tag.find("span")
            a_tag = span_tag.find("a")
            link_relative = a_tag["href"]
            payments = vacancy_tag.find(name="span", class_="bloko-header-section-2")
            vacancy = vacancy_tag.find(class_="serp-item__title")
            response = requests.get(link_relative, headers=headers_gen.generate())
            vacancy_html_data = response.text
            vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, "lxml")
            vacancy_body_tag = vacancy_soup.find(name="div", class_="bloko-tag-list")
            if vacancy_body_tag != None and payments != None:
                if keyword_1 in vacancy_body_tag.text or keyword_2 in vacancy_body_tag.text:
                    payment = payments.text.replace("\u202f", ' ')
                    vacancy_data.append(
                        {
                            "vacancy": vacancy.text,
                            "link": link_relative,
                            "salary": payment,
                            "company": company.text.replace("\xa0", ' '),
                            "city": company_add_tag.text.replace(company.text, ''),
                        }
                    )

def get_next_page():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    response = requests.get(url, headers=headers_gen.generate())
    main_html_data = response.text
    main_soup = bs4.BeautifulSoup(main_html_data, "lxml")

    pager_list_tag = main_soup.find(name="main", class_="vacancy-serp-content")
    pager_tags = pager_list_tag.find_all("a", class_="bloko-button")
    page_quantity = []
    for page in pager_tags:
        if page.text != "Откликнуться" and page.text != "дальше":
            page_quantity.append(page.text)
    return int(page_quantity[-1])

def get_JSON():
    with open("vacancy_data.json", "w+") as f:
        json.dump(vacancy_data, f)

if __name__ == "__main__":
    get_vacancy()
    print(vacancy_data, len(vacancy_data))
    get_JSON()