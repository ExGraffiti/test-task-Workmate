#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class Employee:
    """Класс для хранения данных о сотруднике."""

    def __init__(self, data: Dict[str, str]):
        self.department = data['department']
        self.hours_worked = float(data['hours_worked'])
        self.hourly_rate = self._get_hourly_rate(data)

    def _get_hourly_rate(self, data: Dict[str, str]) -> float:
        """Получает часовую ставку из данных с учётом разных названий столбцов."""
        rate_keys = ['hourly_rate', 'rate', 'salary']
        for key in rate_keys:
            if key in data:
                return float(data[key])
        return 0.0

    @property
    def payout(self) -> float:
        """Рассчитывает общую выплату для сотрудника."""
        return self.hours_worked * self.hourly_rate


class ReportGenerator:
    """Генератор отчётов."""

    @staticmethod
    def generate_payout_report(employees: List[Employee]) -> str:
        """Генерирует отчёт по выплатам."""
        if not employees:
            return "No employee data available"

        total_payout = sum(e.payout for e in employees)
        department_payouts: Dict[str, float] = {}

        for employee in employees:
            department_payouts[employee.department] = (
                    department_payouts.get(employee.department, 0.0) + employee.payout
            )

        report = [
            f"Total payout: ${total_payout:.2f}",
            "",
            "Department payout:"
        ]

        for department, payout in sorted(department_payouts.items()):
            report.append(f"- {department}: ${payout:.2f}")

        return "\n".join(report)


class CSVReader:
    """Читатель CSV файлов."""

    @staticmethod
    def read_file(file_path: Path) -> List[Dict[str, str]]:
        """Читает CSV файл и возвращает список словарей."""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        headers = [header.strip() for header in lines[0].split(',')]
        return [
            dict(zip(headers, [value.strip() for value in line.split(',')]))
            for line in lines[1:]
        ]


class EmployeeProcessor:
    """Обработчик данных сотрудников."""

    def __init__(self):
        self.report_generators = {
            'payout': ReportGenerator.generate_payout_report
        }

    def process_files(self, file_paths: List[str], report_type: str) -> Optional[str]:
        """Обрабатывает файлы и генерирует отчёт."""
        if report_type not in self.report_generators:
            return None

        employees = []
        for file_path in file_paths:
            data = CSVReader.read_file(Path(file_path))
            employees.extend(Employee(row) for row in data)

        return self.report_generators[report_type](employees)


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description='Employee salary report generator')
    parser.add_argument('files', nargs='+', help='CSV files with employee data')
    parser.add_argument('--report', required=True,
                        help='Type of report to generate (currently only "payout")')
    return parser.parse_args()


def main():
    """Основная функция."""
    args = parse_args()
    processor = EmployeeProcessor()
    report = processor.process_files(args.files, args.report)

    if report is None:
        print(f"Error: Unknown report type '{args.report}'")
        exit(1)

    print(report)


if __name__ == '__main__':
    main()