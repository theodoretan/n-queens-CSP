
board, y = '', []
with open('output.txt', 'r') as f:
    for line in f:
        board += line.strip()
    l = board[1:-1].replace(' ', '').split(',')
    for entry in l:
        y.append(entry.split(':')[-1])
    if len(y) == len(set(y)):
        print(board)
        print()
        print("The board is a solution!")
    else:
        print("The board is not a solution")
