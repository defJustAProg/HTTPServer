from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import unquote

full_data_list = []
count_of_sities=0
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path[:12] == '/api/method1':
            self.handleMethod1(self.path)
        elif self.path[:12] == '/api/method2':
            self.handleMethod2(self.path[13:])
        elif self.path[:12] == '/api/method3':
            self.handleMethod3(self.path[13:])
        elif self.path[:12] == '/api/method4':
            self.handleMethod4(self.path[13:])
        else:
            self.send_response(404)
            self.end_headers()


    def sendAnswer(self, response_data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(response_data, ensure_ascii=False, indent=4)
        self.wfile.write(response.encode('utf-8'))

    def handleMethod1(self, path):
        try:
            geonameid=int(path[13:])
            response_data = {'geonameid': '',
                             'name': '',
                             'asciiname': '',
                             'alternatenames': '',
                             'latitude': '',
                             'longitude': '',
                             'feature class': '',
                             'feature code': '',
                             'country code': '',
                             'cc2': '',
                             'admin1 code': '',
                             'admin2 code': '',
                             'admin3 code': '',
                             'admin4 code': '',
                             'population': '',
                             'elevation': '',
                             'dem': '',
                             'timezone': '',
                             'modification date': '', }
            for sity in full_data_list:
                if sity['geonameid'] == geonameid:
                    for element in sity:
                        response_data[element] = sity[element]
                    self.sendAnswer(response_data)
                    break
            else:
                response_data = {'method1': 'method1', 'data': 'There is not sity whith this geonameid'}
                self.sendAnswer(response_data)
        except ValueError:
            response_data = {'method': 'method1', 'data': 'Invalid value'}
            self.sendAnswer(response_data)



    def handleMethod2(self, path):
        pagenumber=path[:path.index('/')]
        count=path[path.index('/')+1:]
        response_data = {'method1': 'method1'}
        try:
            if float(pagenumber) % 1 == 0 and float(count) % 1 == 0:
                count=int(count)
                pagenumber=int(pagenumber)
                count_of_pages=0
                for sity in range(0, count_of_sities-1, count):
                    count_of_pages+=1
                    if count_of_pages == pagenumber:
                        for element_number in range(sity, sity + count):
                                response_data["{number}".format(number=element_number)]=full_data_list[element_number]
                                if element_number==count_of_sities-1:
                                    break
                        break
                else:
                    raise ValueError

                self.sendAnswer(response_data)
            else:
                raise ValueError



        except ValueError:
            response_data = {'method1': 'method1', 'data': 'Invalid value'}
            self.sendAnswer(response_data)



    def handleMethod3(self,path):

        def differenceOfHours(first_sity_dict, second_sity_dict):
            first_value=0
            second_value=0
            try:
                f = open('timeZones.txt', 'r', encoding="utf-8")
                for zone in f:
                    data = zone.split('\t')
                    if first_sity_dict['timezone'] == data[1]:
                        first_value = float(data[2])
                    elif second_sity_dict['timezone'] == data[1]:
                        second_value = float(data[2])
                    if first_value and second_value:
                        return abs(abs(first_value) - abs(second_value))
                f.close()
            except FileNotFoundError:
                return 'Отсутствует Файл timeZones.txt'




        first = unquote(path[:path.index('/')], encoding='utf-8')
        second = unquote(path[path.index('/') + 1:], encoding='utf-8')

        first_sity_dict={}
        second_sity_dict={}
        north=''
        situated_on_the_same_timezone=False

        for sity in full_data_list:
            if first=='' or second =='':
                continue

            name=[]
            name.append(sity['alternatenames'].split(','))
            if first in name[0]:
                first_sity_dict = sity
            elif second in name[0]:
                second_sity_dict = sity

            if first_sity_dict and second_sity_dict:
                if first_sity_dict['latitude'] > second_sity_dict['latitude']:
                    north = first_sity_dict['alternatenames']
                elif first_sity_dict['latitude'] < second_sity_dict['latitude']:
                    north = second_sity_dict['alternatenames']

                if first_sity_dict['timezone'] == second_sity_dict['timezone']:
                    situated_on_the_same_timezone = True


                response_data = {'method': 'method3', 'first sity': first_sity_dict, 'second sity':second_sity_dict, 'north': north, 'situated in the same zone':situated_on_the_same_timezone, 'difference in hours': differenceOfHours(first_sity_dict, second_sity_dict)}
                self.sendAnswer(response_data)

                break


        else:
            response_data = {'method': 'method3', 'data': 'No sity whith this name'}
            self.sendAnswer(response_data)



    def handleMethod4(self, path):
        response_data={}
        count=0
        for sity in full_data_list:
            if path == '':
                continue
            if path == sity['name'][:len(path)]:
                response_data[count]=sity
                count += 1
        if response_data:
            self.sendAnswer(response_data)
        else:
            response_data={'method':'method4', 'data':'No sity whith this name'}
            self.sendAnswer(response_data)


def run():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, RequestHandler)

    f = open('RU.txt', 'r', encoding="utf-8")
    list_of_keys = ['geonameid',
                    'name',
                    'asciiname',
                    'alternatenames',
                    'latitude',
                    'longitude',
                    'feature class',
                    'feature code',
                    'country code',
                    'cc2',
                    'admin1 code',
                    'admin2 code',
                    'admin3 code',
                    'admin4 code',
                    'population',
                    'elevation',
                    'dem',
                    'timezone',
                    'modification date']
    global full_data_list
    global count_of_sities
    for line in f:
        count_of_sities+=1
        dict_of_element = {}
        data = line.split('\t')
        key_number = 0
        for element in data:
            if key_number==0:
                dict_of_element[list_of_keys[key_number]] = int(element)
                key_number += 1
                continue
            dict_of_element[list_of_keys[key_number]] = element
            key_number += 1
            if key_number==len(data):
                dict_of_element[list_of_keys[len(data) - 1]] = element.replace('\n', '')
                break
        full_data_list.append(dict_of_element)

    print('count_of_sities=',count_of_sities)
    f.close()
    print('Сервер запущен на localhost:8000...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

