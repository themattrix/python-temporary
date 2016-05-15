import temporary


def test_control():
    pass


@temporary.temp_dir(make_cwd=True)
def test_temp_dir_with_make_cwd_is_registered_as_test():
    pass


@temporary.in_temp_dir()
def test_in_temp_dir_is_registered_as_test():
    pass
