# Тестовое задание для стажера на позицию «Программист на языке Python»

------

## Сервер реализован с помощью:

- Python версии 3.11 64-bit
- http.server

------

## Все данные берутся  из текстового файла *RU.txt* и, если необходимо вызвать метод 4, файл *timeZones.txt* должен быть в директории, где был вызван скрипт сервера *script.py*. Сервер принимает GET запросы. Скрипт запускается следующим образом: python3 script.py.

------

### Первый метод: Метод принимает идентификатор geonameid и возвращает информацию о городе.

```python
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
```

Метод перебирает заранее составленный список со всеми городами на наличие города с заданным geonameid.

Пример запроса с использованием утилиты curl: curl -X GET http://127.0.0.1:8000/api/method1/451747

------

### Второй метод: Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией.

```python
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
```

Метод отображает список городов на заданной странице с заданным количеством городов. Если после отсчета целых страниц(с заданным количеством городов) остается последняя страница с меньшим количеством городов, и клиент выбирает последнюю страницу, она будет показана, но в ней будут лишь оставшиеся города.

Пример запроса с использованием утилиты curl: curl -X GET http://127.0.0.1:8000/api/method2/2/3

------

### Третий метод: Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона и насколько часов она отличается.

```python
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
```

При необходимости увидеть, на сколько часов различаются временные зоны у указанных городов, в директории со скриптом *script.py* должен находиться файл *timeZones.txt* из архива, приложенного к заданию.

Пример запроса с использованием утилиты curl: curl -X GET http://127.0.0.1:8000/api/method3/Москва/Новосибирск

### Метод, показывающий варианты городов, название которых начинается с введенных клиентом символов на английском языке.

```python
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
```

Пример запроса с использованием утилиты curl: curl -X GET http://127.0.0.1:8000/api/method4/Novosib

