import json
import pandas
import os
import time


class BigExcel:
    """ 生成所有数据 xlsx文件"""

    def __init__(self, path="excel_res"):
        self.brand_dic = {'10000': 'ROARINGWILD',
                          '10001': 'Thrasher',
                          '10002': 'Y-3', '10012': 'Balenciaga', '10013': 'Neil Barrett', '10014': 'KENZO',
                          '10016': 'Vetements',
                          '10017': 'PLACES+FACES', '10018': '大疆',
                          '10019': 'Givenchy', '10021': 'Cav Empt', '10022': 'LONGINES', '10024': 'BANDAI',
                          '10027': 'DICKIES',
                          '10029': 'McQ', '10030': 'CarharttWIP', '10031': 'Alpha Industries',
                          '10033': 'Hasbro', '10035': 'dyson', '10037': 'C2H4', '10038': 'KITH',
                          '10039': 'Randomevent', '10082': 'FOG', '10084': 'Bounce', '1222': 'NOAH',
                          '1245': 'OFF-WHITE',
                          '13': 'Jordan', '1310': 'Champion', '144': 'Nike', '176': 'CONVERSE', '1860': 'THOM BROWNE',
                          '2': 'Puma',
                          '2389': 'LEGO', '3': 'adidas', '3023': 'UNDERCOVER', '33': '李宁', '34': '安踏',
                          '4': 'New Balance', '421': 'Kaws',
                          '439': 'Supreme', '45': 'THE NORTH FACE', '494': 'adidas original', '4981': '虎扑优选',
                          '4985': 'Revenge Storm',
                          '4988': 'OMEGA', '4991': 'Medicom Toy', '4992': 'FR2', '4993': 'Fucking Awesome',
                          '577': 'PALACE',
                          '6': 'Reebok', '634': 'A BATHING APE', '65': 'Apple', '7': 'Under Armour', '8': 'Asics',
                          '843': 'CASIO', '9': 'Vans'
                          }
        self.path = path
        try:
            os.mkdir(self.path)
        except:
            print("path {} has been exists!".format(self.path))

    def work_thead(self, time_name, k, v):
        key_list = ["id", "name", "productId", "price", "size_list", "brand_id", "color", "articleNumber", "authPrice",
                    "sellDate", "exchangeDesc", "soldNum", "text_string", "img_list", "size_price"]
        new_list = []
        str_list = []
        for i in v:
            size_price = i['size_price']
            if type(size_price) != list:
                size_price = json.loads(size_price)
            for price_list in size_price:
                if price_list[0] not in i:
                    i[price_list[0]] = price_list[1]
                if price_list[0] not in new_list and price_list[0] not in str_list:
                    if "." in price_list[0]:
                        try:
                            price_list[0] = float(price_list[0])
                            new_list.append(price_list[0])
                        except:
                            str_list.append(price_list[0])
                    elif price_list[0].isdigit():
                        price_list[0] = int(price_list[0])
                        new_list.append(price_list[0])
                    else:
                        str_list.append(price_list[0])
        new_list = sorted(new_list)
        key_list = key_list + new_list + str_list
        for i in v:
            for key in key_list:
                key = str(key)
                if key not in i:
                    i[key] = "--"
            for key in i:
                try:
                    i[key] = json.loads(i[key])
                except:
                    pass
        try:
            brand_name = self.brand_dic[k]
        except:
            brand_name = k
        writer = pandas.ExcelWriter("{}/{}/{}.xlsx".format(self.path, time_name, brand_name))
        pdfrm = pandas.DataFrame(data=v)
        pdfrm.to_excel(writer)
        writer.save()
        print("{} excel write complete! ".format(brand_name))

    def run(self, data):

        all_data = {}
        for i in data:
            # all_data['all_data'].append(i)
            if str(i['brand_id']) not in all_data:
                all_data[str(i['brand_id'])] = [i]
            else:
                all_data[str(i['brand_id'])].append(i)
        time_name = time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))
        try:
            os.mkdir("{}/{}".format(self.path, time_name))
        except BaseException as e:
            print(e)
            print("dir has exists!")
        t_list = []
        import multiprocessing
        pool = multiprocessing.Pool()
        for k, v in all_data.items():
            pool.apply_async(self.work_thead, (time_name, k, v,))
        pool.close()
        pool.join()
