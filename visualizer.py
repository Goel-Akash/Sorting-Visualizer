import pygame
import random
import math
pygame.init()

class back_ground:
    BLACK = 0, 0, 0
    WHITE =255, 0, 0
    GREEN =0, 255, 0
    RED = 255, 0, 0
    background_color = WHITE

    gradient = [(0, 0, 0),(0, 0, 0),(0, 0, 0)]

    SIDE_PAD = 100
    TOP_PAD = 150

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    def __init__(self,width,height,lst):
        self.width= width
        self.height= height

        self.window=pygame.display.set_mode((width,height))
        pygame.display.set_caption("sorting Visualizer")
        self.set_list(lst)


    def set_list(self,lst):
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)
        
        self.block_width=round((self.width-self.SIDE_PAD)/len(lst))
        self.block_height=math.floor((self.height-self.TOP_PAD)/(self.max_val-self.min_val))
        self.start_x=self.SIDE_PAD//2 


def draw(back_info, algo_name, ascending):
    back_info.window.fill(back_info.background_color )

    title = back_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, back_info.GREEN)
    back_info.window.blit(title,(back_info.width/2 - title.get_width()/2,5))

    controls = back_info.FONT.render(" R- Reset | SPACE - Start sorting | A - Ascending | D - Descecding ",1,back_info.BLACK)
    back_info.window.blit(controls,(back_info.width/2 - controls.get_width()/2,47))

    sorting = back_info.FONT.render(" I - Insertion Sort | B - Bubble Sort ",1,back_info.BLACK)
    back_info.window.blit(sorting,(back_info.width/2 - sorting.get_width()/2,79))

    draw_list(back_info)
    pygame.display.update()

def draw_list(back_info, color_positions={}, clear_bg=False):

    lst=back_info.lst

    if clear_bg:
        clear_rect = (back_info.SIDE_PAD//2, back_info.TOP_PAD, back_info.width - back_info.SIDE_PAD, back_info.height - back_info.TOP_PAD)
        pygame.draw.rect(back_info.window, back_info.background_color, clear_rect)

    for i,val in enumerate(lst):
        x=back_info.start_x + i*back_info.block_width
        y=back_info.height - (val-back_info.min_val)*back_info.block_height
        color=back_info.gradient[i%3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(back_info.window, color, (x,y, back_info.block_width,back_info.height))

    if clear_bg:
        pygame.display.update()

def create_initial_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(back_info, ascending=True):
	lst = back_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(back_info, {j: back_info.GREEN, j + 1: back_info.RED}, True)
				yield True

	return lst

def insertion_sort(back_info, ascending=True):
	lst = back_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(back_info, {i - 1: back_info.GREEN, i: back_info.RED}, True)
			yield True

	return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n=200
    min_val=0
    max_val=100

    lst = create_initial_list(n, min_val, max_val)
    back_info = back_ground(1000,700,lst)

    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algo_gen = None
   
    while run:
        clock.tick(180)
        if sorting:
            try:
                next(sorting_algo_gen)
            except StopIteration:
                sorting = False
        else:
            draw(back_info, sorting_algo_name, ascending)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = create_initial_list(n,min_val,max_val)
                back_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_gen = sorting_algo(back_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algo= insertion_sort
                sorting_algo_name = "insertion sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algo= bubble_sort
                sorting_algo_name= "bubble sort"
    pygame.QUIT

if __name__ == "__main__":
	main()