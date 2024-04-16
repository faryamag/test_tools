import requests
import zipfile
import sys
from tempfile import TemporaryFile


def pygen_test(url, file):
    tasks = {}

    with open(file, 'wb') as zip_file:
        zip_file.write(requests.get(url).content)

    with zipfile.ZipFile(file) as archive:
        for file in archive.filelist:
            with archive.open(file, mode='r') as archived_file:
                if '.clue' not in archived_file.name:
                    tasks[archived_file.name]= {}
                    dict.setdefault(tasks[archived_file.name],'task',archived_file.read().decode())
                elif archived_file.name.endswith('.clue'):
                    dict.setdefault(tasks[archived_file.name.rstrip('.clue')],'answear',archived_file.read().decode())


    for name, task in tasks.items():
        print('Task number:', name)

        with TemporaryFile(mode='w+') as temp:
            sys.stdout=temp
            exec(task['task'])
            sys.stdout = sys.__stdout__
            temp.seek(0)
            try:
                assert temp.read().strip() == task['answear']
                print("Успех")
            except Exception as e:
                temp.seek(0)
                print(f'Ошибка сравнения результата в задании: {name}')
                print(f"Ожидается результат: \n{task['answear']}")
                print(f"Получен результат: \n{temp.read().strip()}")


if __name__ =='__main__':
    url= 'https://stepik.org/media/attachments/lesson/569748/tests_2310066.zip'
    file = 'test.zip'
    pygen_test(url=url, file=file)
