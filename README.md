# Employee Salary Report Generator

Простой скрипт для генерации отчетов по зарплатам сотрудников на основе CSV файлов.

## Функциональность

- Чтение данных сотрудников из CSV файлов
- Поддержка различных названий для колонки с часовой ставкой (`hourly_rate`, `rate`, `salary`)
- Генерация отчета по выплатам (payout) с разбивкой по отделам
- Обработка нескольких входных файлов

## Требования

- Python 3.6+

## Установка

Не требуется, скрипт готов к использованию.

## Использование

```bash
python3 main.py file1.csv file2.csv --report payout
```

Где:

file1.csv, file2.csv - CSV файлы с данными сотрудников

payout - тип отчета (в текущей версии поддерживается только этот тип)

## Формат CSV файла
Файл должен содержать следующие колонки (названия могут отличаться):

department - отдел сотрудника

hours_worked - отработанные часы

Одна из колонок с часовой ставкой: hourly_rate, rate или salary


## Пример файла:

```text
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
```

## Пример вывода
```text
Total payout: $24200.00

Department payout:
- Design: $16200.00
- Marketing: $8000.00
```

# Добавление новых отчетов
Для добавления нового типа отчета:

Создайте новый метод в классе ReportGenerator, например:

```python
@staticmethod
def generate_avg_rate_report(employees: List[Employee]) -> str:
    # Логика генерации отчета
	...
    return report_text
```
Добавьте новый тип отчета в EmployeeProcessor:

```python
def __init__(self):
    self.report_generators = {
        'payout': ReportGenerator.generate_payout_report,
        'avg_rate': ReportGenerator.generate_avg_rate_report
    }
```
Обновите parse_args(), добавив новый тип в список допустимых значений:

```python
parser.add_argument('--report', required=True, 
                   choices=['payout', 'avg_rate'],
                   help='Type of report to generate')
```


# Тестирование
Для запуска тестов:

```bash
pytest test_main.py
```

## Тесты проверяют:

### - Создание объекта Employee

### - Чтение CSV файлов

### - Генерацию отчета payout

### - Обработку неверного типа отчета

### - Обработка ошибок

## Скрипт обрабатывает следующие ошибки:

### - Неверный тип отчета (выводит сообщение об ошибке)

### - Отсутствие обязательных аргументов (обрабатывается argparse)



## Примеры работы

### Запуск скрипта
![Пример запуска](./screenshots/usage.jpg)

### Пример отчета
![Пример отчета](./screenshots/usage-2.jpg)

### Запуск тестов
![Пример запуска](./screenshots/test-usage.jpg)

### Пример отчета теста
![Пример отчета](./screenshots/test-usage-2.jpg)