import traceback


def get_traceback(ex):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    return ''.join(tb_lines)

if __name__ == '__main__':
    print(f'{str(int("A001"[-1]) + 1)}')