from main import choose_option


if __name__ == '__main__':
    assert choose_option('2+2*5') == 12
    assert choose_option('2*2/4') == 1
    assert choose_option('4/2+(3+3)') == 8
    assert choose_option('4/2+(3+3-(9-8))') == 7
    assert choose_option('/help') == 'This program can perform subtraction and addition etc'
    assert choose_option('/hp') == 'Unknown command'
    print('All tests is OK')
