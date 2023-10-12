import requests
import parsel
import statistics
import csv
import concurrent.futures
#22.92s

f = open('松江.csv', mode='a', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '房源小区',
    '租金',
    '区域',
    '租赁方式',
    '楼层',
    '户型',
    '房子面积',
    '朝向',
    '电梯',
    '平均地铁距离',
    '维护时间',
    '入住时间',
    '车位',
    '用水',
    '用电',
    '燃气',
    '采暖',
    '租期',
    '房源介绍',
    '地铁信息',
    '图片链接',
    '看房'
])
csv_writer.writeheader()

district_pin_list_0 = ['huangpu', 'changning', 'putuo', 'hongkou', 'yangpu', 'jinshan', 'jiading', 'chongming',
                       'fengxian', 'qingpu']
district_list_0 = ["黄浦", "长宁", "普陀", "虹口", "杨浦", "金山", "嘉定", "崇明", "奉贤", "青浦"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
}



def get_page_1(district_pin):
    url_0 = 'https://sh.lianjia.com/zufang/' + district_pin
    try:
        response_0 = requests.get(url=url_0, headers=headers)
        response_0.raise_for_status()  # 检查请求是否成功
        text_0 = response_0.text
        selector_0 = parsel.Selector(text_0)
        num_0 = selector_0.css('#content > div.content__article > p > span.content__title--hl::text').get()
        num_0 = int(num_0)
        num_pages = int((num_0 - (num_0 % 30)) / 30 + 1)
        return num_pages
    except Exception as e:
        print(f"Error getting page count for {district_pin}: {str(e)}")
        return 0


def get_page_2(a):
    a = int(a)
    return int((a - (a % 30)) / 30 + 1)

district = "松江"

def scrape_page(district_pin, page_num, backurl):
    url = 'https://sh.lianjia.com/zufang/' + district_pin + '/pg' + f'{page_num}' + backurl
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        text = response.text
        selector = parsel.Selector(text)
        href_list = selector.css(
            '#content > div.content__article > div.content__list > div > div > p.content__list--item--title > a::attr(href)').getall()
        for i in range(len(href_list)):
            href_list[i] = 'https://sh.lianjia.com' + href_list[i]

        #district = "徐汇"  # 区域
        for index in href_list:
            html_data = requests.get(url=index, headers=headers).text
            selector_1 = parsel.Selector(html_data)

            title = selector_1.css('body > div.wrapper > div:nth-child(2) > div.content.clear.w1150 > p::text').get()
            if title is None:  # 独栋

                way = "独栋"
                title = selector_1.css('#aside > p > span.aside_neme::text').get()
                price = "\\" if not (selector_1.css('#aside > p > span.aside_price::text').get()) else (
                    selector_1.css('#aside > p > span.aside_price::text').get()).strip()
                floor = '详见每户信息'
                house_type = '详见每户信息'
                area = '详见每户信息'
                pic = selector_1.css(
                    '#mySwipe > ul.content__article__slide__wrapper > div:nth-child(1) > img::attr(src)').get()
                direction = '详见每户信息'
                elevator = '详见每户信息'
                description = "无" if not (
                    selector_1.css('#info > p.flat__info--description::text').getall()) else " ".join(
                    selector_1.css('#info > p.flat__info--description::text').getall())  # 房源介绍
                if price == "\\" and description == "无":
                    continue
                maintenance = '详见每户信息'
                starting_time = '详见房源信息'
                parkinglot = '详见房源信息'
                water = '详见房源信息'
                electricity = '详见房源信息'
                gas = '详见房源信息'
                heat = '详见房源信息'
                duration = '详见房源信息'
                visit = '详见房源信息'
                subway = '详见房源信息'
                nearest_subway = '详见房源信息'

            else:
                # 整租
                way = "整租非独栋"
                title = title.strip()[3:].split(" ")[0]  # 房源小区
                price = selector_1.css('#aside > div.content__aside--title > span::text').get()  # 租金
                floor = selector_1.css('#info > ul:nth-child(2) > li:nth-child(8)::text').get()[3:]  # 楼层
                # print(title)

                house_type = selector_1.css('#aside > ul > li:nth-child(2)::text').get().split(" ")[0]  # 户型
                area = selector_1.css('#aside > ul > li:nth-child(2)::text').get().split(" ")[1][:-1]  # 房子面积
                pic = selector_1.css('#desc > ul > li:nth-child(1) > img::attr(src)').get()  # 图片链接

                # decoration_type = selector_1.css('#aside > ul > li:nth-child(2)::text').get().split(" ")[3] # 装修类型

                direction = selector_1.css('#info > ul:nth-child(2) > li:nth-child(3)::text').get()[3:]  # 朝向
                elevator = selector_1.css('#info > ul:nth-child(2) > li:nth-child(9)::text').get()[3:]  # 电梯
                description = "无" if not (selector_1.css('#desc > p::text').getall()) else " ".join(
                    selector_1.css('#desc > p::text').getall())  # 房源介绍
                maintenance = selector_1.css('#info > ul:nth-child(2) > li:nth-child(5)::text').get()[3:]  # 维护时间
                starting_time = selector_1.css('#info > ul:nth-child(2) > li:nth-child(6)::text').get()[3:]  # 入住时间
                parkinglot = selector_1.css('#info > ul:nth-child(2) > li:nth-child(11)::text').get()[3:]  # 车位
                water = selector_1.css('#info > ul:nth-child(2) > li:nth-child(12)::text').get()[3:]  # 用水
                electricity = selector_1.css('#info > ul:nth-child(2) > li:nth-child(14)::text').get()[3:]  # 用电
                gas = selector_1.css('#info > ul:nth-child(2) > li:nth-child(14)::text').get()[3:]  # 燃气
                heat = selector_1.css('#info > ul:nth-child(2) > li:nth-child(17)::text').get()[3:]  # 采暖
                duration = selector_1.css('#info > ul:nth-child(3) > li:nth-child(2)::text').get()[3:]  # 租期
                visit = selector_1.css('#info > ul:nth-child(3) > li:nth-child(5)::text').get()[3:]  # 看房
                subway = selector_1.css('#around > ul:nth-child(4) > li > span::text').getall()  # 地铁信息
                if not subway:
                    subway = "附近无地铁"

                temp_2 = selector_1.css('#around > ul:nth-child(4) > li > span:nth-child(2)::text').getall()
                nearest_subway = "附近无地铁"
                if len(temp_2) > 0:
                    for i in range(len(temp_2)):
                        temp_2[i] = temp_2[i][:-1]
                    temp_2 = [int(x) for x in temp_2]
                    nearest_subway = statistics.mean(temp_2)  # 平均地铁距离

            dit = {
                    '房源小区': title,
                    '租金': price,
                    '区域': district,
                    '租赁方式': way,
                    '楼层': floor,
                    '户型': house_type,
                    '房子面积': area,
                    '朝向': direction,
                    '电梯': elevator,
                    '平均地铁距离': nearest_subway,
                    '维护时间': maintenance,
                    '入住时间': starting_time,
                    '车位': parkinglot,
                    '用水': water,
                    '用电': electricity,
                    '燃气': gas,
                    '采暖': heat,
                    '租期': duration,
                    '房源介绍': description,
                    '地铁信息': subway,
                    '图片链接': pic,
                    '看房': visit
                }

            csv_writer.writerow(dit)
    except Exception as e:
        print(f"Error scraping data for {url}: {str(e)}")


with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    for q in range(0, 10):

        # 使用多线程爬取多个页面
        # futures = [executor.submit(scrape_page, district_pin_list_0[q], page_num, '') for page_num in
        #            range(1, get_page_1(district_pin_list_0[q]) + 1)]  # 无需分类的区域
        futures = [executor.submit(scrape_page, "songjiang", page_num, 'rco11erp5000') for page_num in
                   range(1, get_page_2(2000) + 1)] # 需要根据租金分类的区域，手动调整租金分类标准

        # 等待所有任务完成
        concurrent.futures.wait(futures)

        futures = [executor.submit(scrape_page, "songjiang", page_num, 'rco11brp5001') for page_num in
                   range(1, get_page_2(1186) + 1)]

        # 等待所有任务完成
        concurrent.futures.wait(futures)



# 关闭CSV文件
f.close()
