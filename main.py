import re

AVAILABLE_COMMAND = ('/exit', '/help')
AVAILABLE_CHARS = '1234567890+-*/'


def check_last(last_sign):
    """
    Check correct ending
    :param last_sign:
    :return:
    """
    if last_sign in '+-*/':
        return False
    return True


def is_there_a_sign(nums):
    """
    Check signs in exp
    :param nums:
    :return:
    """
    if '+' in nums or '-' in nums or '/' in nums or '*' in nums:
        return True
    return False


def sort_input(nums, var):
    """
    Make dict of digits with their signs
    :param nums:
    :param var:
    :return:
    """
    negative = False
    current_num = ''
    current_var = ''
    last_operation = ''
    multi_flag = False
    div_flag = False
    nums_with_sign = {'+': [], '-': []}
    for n in nums:
        if n in AVAILABLE_CHARS:
            if n.isdigit():
                current_num += n
            elif current_num != '':
                if multi_flag:
                    nums_with_sign[last_operation][-1] *= int(current_num)
                    multi_flag = False
                elif div_flag:
                    nums_with_sign[last_operation][-1] /= int(current_num)
                    div_flag = False
                else:
                    if negative:
                        nums_with_sign['-'].append(int(current_num))
                        last_operation = '-'
                    else:
                        nums_with_sign['+'].append(int(current_num))
                        last_operation = '+'
                    negative = False
                current_num = ''
            elif current_var != '':
                if current_var in list(var.keys()):
                    if multi_flag:
                        nums_with_sign[last_operation][-1] *= var[current_var]
                        multi_flag = False
                    elif div_flag:
                        nums_with_sign[last_operation][-1] /= var[current_var]
                        div_flag = False
                    else:
                        if negative:
                            nums_with_sign['-'].append(var[current_var])
                            last_operation = '-'
                        else:
                            nums_with_sign['+'].append(var[current_var])
                            last_operation = '+'
                        negative = False
                    current_var = ''
                else:
                    return False
            if n == '-':
                negative = not negative
            if (n == '/' and div_flag) or (n == '*' and multi_flag):
                return False
            if n == '*' and not multi_flag:
                multi_flag = True
            if n == '/' and not div_flag:
                div_flag = True
        elif n.isalpha():
            current_var += n
        else:
            return False
    return nums_with_sign


def search_brackets(nums):
    """
    Process  braces
    :param nums:
    :return:
    """
    try:
        left_brackets_index = nums.index('(')
    except ValueError:
        return 0, 0
    try:
        right_brackets_index = nums.rindex(')')
    except ValueError:
        return 0, 0
    return left_brackets_index, right_brackets_index


def calculation(nums, var):
    if '(' in nums or ')' in nums:
        left_brackets_index, right_brackets_index = search_brackets(nums)
        if not left_brackets_index:
            return 'Invalid expression'
        else:
            inner_part = nums[left_brackets_index + 1:right_brackets_index]
            inner_part = calculation(inner_part, var)
            if right_brackets_index != len(nums) - 1:
                right_part = nums[right_brackets_index + 1:]
            else:
                right_part = ''
            nums = nums[:left_brackets_index] + '+' + str(inner_part) + right_part
    if check_last(nums[-1]) and is_there_a_sign(nums) and nums != 'Invalid expression' and nums[0] != '+':
        nums = sort_input(nums + '+', var)
        if nums:
            return int(sum(nums['+']) - sum(nums['-']))
        else:
            return 'Invalid expression'
    else:
        return 'Invalid expression'


def check_var(user_input, var):
    if not bool(re.match(r'^[A-Za-z]+$', user_input[0].strip())):
        return 'Invalid identifier'
    if len(user_input) != 1:
        if not (user_input[1].strip()).isdigit():
            if not bool(re.match(r'[A-Za-z]+$', user_input[1].strip())):
                return 'Invalid assignment'
            if user_input[1].strip() not in list(var.keys()):
                return 'Unknown variable'
        if len(user_input) != 2:
            return 'Invalid assignment'
        return False
    else:
        if user_input[0].strip() not in list(var.keys()):
            return 'Unknown variable'
        return var[user_input[0]]


def add_new_var(user_input, var):
    if (user_input[1].strip()).isdigit():
        var[user_input[0].strip()] = int(user_input[1].strip())
    else:
        var[user_input[0].strip()] = var[user_input[1].strip()]
    return var


def choose_option(user_input):
    """
    Check input
    :param user_input:
    :return:
    """
    var = {}
    if len(user_input) == 0:
        pass
    elif user_input[0] == '/':
        if user_input not in AVAILABLE_COMMAND:
            return 'Unknown command'
        elif user_input == '/help':
            return 'This program can perform subtraction and addition etc'
    else:
        if '=' in user_input:
            user_input = user_input.split('=')
            not_valid = check_var(user_input, var)
            if not_valid:
                return not_valid
            else:
                var = add_new_var(user_input, var)
        elif len(user_input.split()) == 1 and '+' not in user_input and '-' not in user_input \
                and '/' not in user_input and '*' not in user_input:
            if user_input.isdigit():
                return user_input
            else:
                return check_var(user_input.split(), var)
        else:
            user_input = user_input.split()
            return calculation(''.join(user_input), var)


def main():
    """
    Read input
    :return:
    """
    user_input = input()
    while user_input != '/exit':
        print(choose_option(user_input))
        user_input = input()
    print('Bye!')


if __name__ == '__main__':
    main()
