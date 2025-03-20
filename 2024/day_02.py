from readfile import read


# input_file_name = '02_example.txt'
input_file_name = '02_input.txt'

class Solution:

    reports = []
    
    def read_input(self):
        self.reports = [
            [int(level) for level in line.split()]
            for line in read(input_file_name)
        ]
        for report in self.reports:
            print(report)
        print()



    def count_safe_reports(self):
        self.read_input()

        # returns the count of safe reports in the input file

        test_results = [
            (report, self._is_safe(report))
            for report in self.reports
        ]
        for report, result in test_results:
            pretty_result = 'safe' if result else 'unsafe'
            print(f'{report} {pretty_result}')

        return sum(
            self._is_safe(report)
            for report in self.reports
        )

    def _is_safe(self, report):
        '''
        return: 0 when report is unsafe, 1 when safe
        '''

        # print(f'testing report: {report}')

        increasing_rate = (1, 2, 3)
        decreasing_rate = (-1, -2, -3)

        # determine increasing or decreasing
        rate_test = report[1] - report[0]
        if rate_test > 0:
            expected_rate = increasing_rate
        elif rate_test < 0:
            expected_rate = decreasing_rate
        else:
            # neither inc or dec: fail
            return 0

        # test: adjacent levels respect direction
        # test: adjacent levels rate is allowed

        prev_level = report[0]


        for curr_level in report[1:]:
            # print(f'Comparing {curr_level} and {prev_level} to {expected_rate}')
            if curr_level - prev_level not in expected_rate:
                return 0
            prev_level = curr_level
        return 1

    def safe_with_retries(self, report):
        initial_check = self._is_safe(report)
        if initial_check:
            return initial_check

        for i in range(len(report)):
            # remove the item at i
            # recheck
            pruned_report = [
                level for j, level in enumerate(report)
                if j != i
            ]

            recheck = self._is_safe(pruned_report)
            if recheck:
                return recheck

        return 0

            

if __name__ == '__main__':
    s = Solution()
    count = s.count_safe_reports()

    # too low: 404
    print(f'part 1: {count}')

    for report in s.reports:
        result = s.safe_with_retries(report)
        pretty_result = 'safe' if result else 'unsafe'
        print(f'{report} {pretty_result}')

    count = sum(
        s.safe_with_retries(report)
        for report in s.reports
    )
    print(f'part 2: {count}')
