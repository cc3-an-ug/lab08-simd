import utils
import subprocess

def check_ex1():
    output = utils.parse_form('./ex1.txt')
    expected = {'1': 'd', '2': 'c', '3': 'c'}
    grade = 0
    err = 0
    for key in expected.keys():
        out = output.get(key)
        exp = expected.get(key)
        if out is not None:
            if exp == out:
                grade += (20 / 3)
            else:
                err = err + 1
        else:
            err = err + 1
    if err == len(expected):
        return (0, utils.failed())
    return (grade, utils.passed() if (err == 0) else utils.incomplete(), '')


# checks sum vectorized
def check_ex2():
    try:
        # compile
        utils.make(target='clean')
        task = utils.make(target='sum')
        if task.returncode != 0:
            return (0, utils.failed(), task.stderr.decode().strip())
        # run tests
        task = utils.execute(cmd=['./sum'], timeout=15)
        if task.returncode != 0:
            return (0, utils.failed(), task.stderr.decode().strip())
        # Output
        output = task.stdout.decode().strip()
        try:
            output = list(map(lambda x: float(x.strip().split(':')[1].strip('microseconds').strip()), output.split('\n')[:-1]))
            if output[0] > output[2] and output[1] > output[2]:
                return (50, utils.passed(), '')
        except:
            return (0, utils.failed(), '')
        return (0, utils.failed(), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed(), '')
    except MemoryError:
        return (0, utils.failed(), '')
    except Exception as e:
        print(e)
        return (0, utils.failed(), '')


# checks sum vectorized unrolled
def check_ex3():
    try:
        # compile
        utils.make(target='clean')
        task = utils.make(target='sum')
        if task.returncode != 0:
            return (0, utils.failed(), task.stderr.decode().strip())
        # run tests
        task = utils.execute(cmd=['./sum'], timeout=15)
        if task.returncode != 0:
            return (0, utils.failed(), task.stderr.decode().strip())
        # Output
        output = task.stdout.decode().strip()
        output = list(map(lambda x: float(x.strip().split(':')[1].strip('microseconds').strip()), output.split('\n')))
        if output[0] > output[2] and output[1] > output[2] and output[2] > output[3]:
            return (50, utils.passed(), '')
        return (0, utils.failed(), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed(), '')
    except MemoryError:
        return (0, utils.failed(), '')
    except Exception:
        return (0, utils.failed(), '')


def lab8_SIMD():
    not_found = utils.expected_files(['./ex1.txt', './sum.c'])
    if len(not_found) == 0:
        table = []
        ex1_result = check_ex1()
        table.append(('1. Familiarize Yourself', *ex1_result[0: 2]))
        ex2_result = check_ex2()
        table.append(('2. Writing SIMD Code', *ex2_result[0: 2]))
        ex3_result = check_ex3()
        table.append(('3. Loop Unrolling', *ex3_result[0: 2]))
        errors = ''
        errors += utils.create_error('Writing SIMD Code', ex2_result[2])
        errors += '\n' + utils.create_error('Loop Unrolling', ex3_result[2])
        errors = errors.strip()
        grade = 0
        grade += ex1_result[0]
        grade += ex2_result[0]
        grade += ex3_result[0]
        grade = round(grade)
        grade = min(grade, 120)
        report = utils.report(table)
        print(report)
        if errors != '':
            report += '\n\nMore Info:\n\n' + errors
        print('\n=> Score: %d/100' % grade)

if __name__ == '__main__':
    lab8_SIMD()
