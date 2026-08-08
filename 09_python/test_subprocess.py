import pytest

def func_test():
    print("func_test")

@pytest.mark.skip(reason="bdsim import error")
def test_subprocess(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code_to_run = make_bdsim_test_code(func_test)
    output = run_bdsim_test_code_as_subprocess(code_to_run)



