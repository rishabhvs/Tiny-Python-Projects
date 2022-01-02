import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

grid = []  # initialise empty grid
print('\n~~~~~~~ Online Sudoko Solver ~~~~~~~')
level = (input("Choose Difficulty Level (1-4): "))
print('Launching level {} Puzzle on nine.websudoko.com ....'.format(level))
# create driver and open website according to difficulty.
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get('https://nine.websudoku.com/?level='+level)


def isPossible(x, y, n):
    '''
    Check if number is possible at position.
    '''
    global grid
    # check if exists in column
    for i in range(9):
        if grid[i][x] == n:
            return False

    # check if exists in row
    for i in range(9):
        if grid[y][i] == n:
            return False

    # check if exists in corresponding subgrid
    srow, scol = y-y % 3, x-x % 3
    for i in range(3):
        for j in range(3):
            if grid[srow+i][scol+j] == n:
                return False

    return True


def solveOnline(finalGrid):
    '''
    Enter solved suduko on website.
    '''
    choice = input("\nReveal Solution and Start Solving Online?? (y/n): ")
    if choice == 'y' or choice == 'Y':
        sleep(3)
        print('\n',np.matrix(finalGrid))
        for i in range(9):
            for j in range(9):
                cell = driver.find_element_by_id('f'+str(j)+str(i))
                cell.send_keys(str(finalGrid[i][j]))
        sleep(2)
        driver.find_element_by_class_name('bs').click()
        print('\nPuzzle Successfully Solved.')
        sleep(3)


def readOnline():
    '''
    Read Sudoku grid from website and fill grid variable.
    '''
    print('Captured Grid (0 indicates blank cell) :\n')
    global grid
    for i in range(9):
        row = []
        for j in range(9):
            cell = driver.find_element_by_id('f'+str(j)+str(i))
            cellVal = cell.get_attribute('value')
            if not cellVal.isnumeric():
                row.append(0)
            else:
                row.append(int(cellVal))
        grid.append(row)
    print(np.matrix(grid))
    solve()  # Call the solve function.


def solve():
    '''
    Recursive function to solve the suduko grid.
    '''
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10, 1):
                    if isPossible(x, y, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    solveOnline(grid)


readOnline()
driver.quit()

