'''
Quick rST syntax table generator i threw together
'''

while True:

    size = int(input('Size > '))

    fields = []

    widths = []

    for i in range(0, size):
        widths.append(input(f'Size {i} > '))

    for i in range(0, size):
        fields.append(input(f'Field Name {i} > '))

    text = '.. list-table::\n   :widths: ' + ' '.join(widths) + '\n\n'
    
    fo = True
    for field in fields:
        text += f'   {"*" if fo else " "} - {field}\n'
        if fo:
            fo = False
    
    while True:
        field_vals = []
        breakOut = False
        for field in fields:
            inp = input(f'{field} > ')
            if inp == 'done':
                breakOut=True 
                break
            field_vals.append(inp)
        if breakOut:
            break
        f = True
        for val in field_vals:
            text += f'   {"*" if f else " "} - {val}\n'
            if f:
                f = False

    print(text)