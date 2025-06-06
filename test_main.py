import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from main import Employee, CSVReader, ReportGenerator, EmployeeProcessor


@pytest.fixture
def sample_csv_data():
    return """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
"""


@pytest.fixture
def sample_csv_data_alt():
    return """email,name,department,hours_worked,salary,id
test@example.com,Test User,Sales,140,60,301
"""


def test_employee_creation():
    data = {
        'id': '1',
        'email': 'test@example.com',
        'name': 'Test',
        'department': 'Test',
        'hours_worked': '160',
        'hourly_rate': '50'
    }
    employee = Employee(data)
    assert employee.payout == 8000.0


def test_employee_alt_rate_names():
    data1 = {'rate': '30', 'hours_worked': '100', 'department': 'Test'}
    data2 = {'salary': '25', 'hours_worked': '100', 'department': 'Test'}
    data3 = {'hourly_rate': '20', 'hours_worked': '100', 'department': 'Test'}

    assert Employee(data1).payout == 3000.0
    assert Employee(data2).payout == 2500.0
    assert Employee(data3).payout == 2000.0


def test_csv_reader(sample_csv_data):
    with patch('builtins.open', mock_open(read_data=sample_csv_data)):
        data = CSVReader.read_file(Path('test.csv'))
        assert len(data) == 3
        assert data[0]['name'] == 'Alice Johnson'
        assert float(data[1]['hours_worked']) == 150.0


def test_csv_reader_alt(sample_csv_data_alt):
    with patch('builtins.open', mock_open(read_data=sample_csv_data_alt)):
        data = CSVReader.read_file(Path('test.csv'))
        assert len(data) == 1
        assert data[0]['name'] == 'Test User'
        assert float(data[0]['salary']) == 60.0


def test_payout_report():
    employees = [
        Employee({
            'id': '1',
            'department': 'Marketing',
            'hours_worked': '160',
            'hourly_rate': '50'
        }),
        Employee({
            'id': '2',
            'department': 'Design',
            'hours_worked': '150',
            'hourly_rate': '40'
        }),
        Employee({
            'id': '3',
            'department': 'Design',
            'hours_worked': '170',
            'hourly_rate': '60'
        })
    ]

    report = ReportGenerator.generate_payout_report(employees)
    assert "Total payout: $24200.00" in report
    assert "- Design: $16200.00" in report
    assert "- Marketing: $8000.00" in report


def test_employee_processor(sample_csv_data, sample_csv_data_alt):
    with patch('builtins.open') as mocked_open:
        mocked_open.side_effect = [
            mock_open(read_data=sample_csv_data)(),
            mock_open(read_data=sample_csv_data_alt)()
        ]

        processor = EmployeeProcessor()
        report = processor.process_files(['file1.csv', 'file2.csv'], 'payout')

        assert report is not None
        assert "Total payout: $" in report
        assert "- Design: $" in report
        assert "- Marketing: $" in report
        assert "- Sales: $" in report


def test_invalid_report_type():
    processor = EmployeeProcessor()
    assert processor.process_files([], 'invalid') is None