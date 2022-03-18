def fix_regex(expresion):
    first = []
    regex_list = []
    last_index = 0
    i = 0
    special_cases = {
        'positive_closure_group':')+',
        'null_check_group':')?',
        'positive_closure':'+',
        'null_check':'?',
    }
    # Case 01: positive closure (parenthesis)
    if expresion.find(special_cases['positive_closure_group']) != -1:
        while i < len(expresion):
            if expresion[i] == '(':
                first.append(i) # Saves the index            

            if expresion[i] == ')' and i < len(expresion) - 1: # current pos
                regex_list.append(expresion[i])
                if expresion[i + 1] == '+': # is the next pos positive closure?
                    last_index = i + 1
                    regex_list.append('*')
                    regex_list.append(expresion[first.pop() : last_index])
                    i = i + 1
                else:
                    first.pop()

            else:
                regex_list.append(expresion[i])
            i = i + 1

        expresion = ''.join(regex_list)

    #Case 02: null check (parenthesis)
    if expresion.find(special_cases['null_check_group']) != -1:
        while i < len(expresion):
            if expresion[i] == '(':
                first.append(i)                        

            if expresion[i] == ')':
                regex_list.append(expresion[i])  # current pos
                if expresion[i + 1] == '?':     # is the next pos null check?
                    last_index = i + 1
                    regex_list.append('|')
                    regex_list.append('ε')
                    regex_list.append(')')
                    regex_list.insert(first[-1], '(')
                    i = i + 1
                else:
                    first.pop()

            else:
                regex_list.append(expresion[i])
            i += 1

        expresion = ''.join(regex_list)

    final_regex = expresion

    # Case 03: positive closure to an individual symbol
    if expresion.find(special_cases['positive_closure']) != -1:
        while final_regex.find(special_cases['positive_closure']) != -1:
        # while '+' in regex_copy:
            i = final_regex.find('+')
            symbol = final_regex[i - 1]

            final_regex = final_regex.replace(symbol + '+', '(' + symbol + '*' + symbol + ')')

    # Case 04: null check to an individual symbol
    if expresion.find(special_cases['null_check']) != -1:
        while final_regex.find(special_cases['null_check']) != -1:
        # while '?' in regex_copy:
            i = final_regex.find('?')
            symbol = final_regex[i - 1]

            final_regex = final_regex.replace(symbol + '?', '(' + symbol + '|' + 'ε' + ')')

    # Case 05: user did not put the same amount of open parenthesis and close parenthesis
    if final_regex.count('(') > final_regex.count(')'):
        for i in range(final_regex.count('(') - final_regex.count(')')):
            final_regex += ')'
            print(final_regex)

    elif final_regex.count('(') < final_regex.count(')'):
        for i in range(final_regex.count(')') - final_regex.count('(')):
            final_regex = '(' + final_regex

    return add_explicit_concatenation(final_regex)

def add_explicit_concatenation(regex):
    valid_operators = ['(','*','|','?','+']
    enhanced_regex = ''
    i = 0
    
    while i < len(regex):
        if i+1 >= len(regex):
            enhanced_regex += regex[-1]
            break
        if regex[i] == '*' and regex[i+1] != ')' and not (regex[i+1] in valid_operators):
            enhanced_regex += regex[i]+'.'
        elif regex[i] == '*' and regex[i+1] == '(':
            enhanced_regex += regex[i]+'.'
        elif regex[i] == '?' and regex[i+1] != ')' and not (regex[i+1] in valid_operators):
            enhanced_regex += regex[i]+'.'
        elif regex[i] == '?' and regex[i+1] == '(':
            enhanced_regex += regex[i]+'.'
        elif not (regex[i] in valid_operators) and regex[i+1] == ')':
            enhanced_regex += regex[i]
        elif (not (regex[i] in valid_operators) and not (regex[i+1] in valid_operators)) or (not (regex[i] in valid_operators) and (regex[i+1] == '(')):
            enhanced_regex += regex[i]+'.'
        else:
            enhanced_regex += regex[i]
        i += 1
    return enhanced_regex
