import random
import math
import shutil
import os
from PIL import Image, ImageDraw

class Ant:
    def __init__(self, nb_fruits, map_size, random_force, position=None):
        """Constructor of the Ant class

        :param nb_fruits <int>: Number of the fruits on the map
        :param map_size <int>: Size of the map
        :param random_force <bool>: If True the Ant get AI (not implemented yet) and if False the Ant move in random places
        :param:

        Return : None
        """
        self.map_size = map_size
        self.nb_fruits = nb_fruits
        self.random_force = random_force
        self.score = 0
        self.total_moves = 0

        if position is None:
            x = y = self.map_size//2
            self.position = [x, y]
        else:
            self.position = position

    def get_around_square(self):
        """Get the coordonate of the arounding square of the actual coordonate of the ant
        
        Return <tuple> : old position coordonate and the position coordonate of the ant 

        Return <tuple> : Coordonate of the arounding squares
        """
        top_square = right_square = bottom_square = left_square = [self.position[0], self.position[1]]

        if self.position[0] - 1 >= 0 and MAP[self.position[0] - 1] != 1:
            top_square = [self.position[0] - 1, self.position[1]]

        if self.position[1] + 1 < self.map_size and MAP[self.position[1] + 1] != 1:
            right_square = [self.position[0], self.position[1] + 1]

        if self.position[0] + 1 < self.map_size and MAP[self.position[0] + 1] != 1:
            bottom_square = [self.position[0] + 1, self.position[1]]

        if self.position[1] - 1 >= 0 and MAP[self.position[1] - 1] != 1:
            left_square = [self.position[0], self.position[1] - 1]

        return (top_square, right_square, bottom_square, left_square)
    
    def get_nearest_fruit(self, coord):
        dist = {}
        nearest_distance = 1000000
        
        for fruit_coord in FRUITS_COORDS:
            delta_x = (coord[0] - fruit_coord[0])**2
            delta_y = (coord[1] - fruit_coord[1])**2
            distance = math.sqrt(delta_x + delta_y)
            dist[distance] = fruit_coord
            if distance < nearest_distance: nearest_distance = distance

        if FRUITS_COORDS:
            return (nearest_distance, dist[nearest_distance])

        return (0, None)
    
    def get_best_move(self):
        nearest_distance = 1000000
        nfs = {}
        around_squares = self.get_around_square()
        
        for square_cord in around_squares:
            distance, _ = self.get_nearest_fruit(square_cord)
            nfs[distance] = square_cord
            #if distance < nearest_distance: nearest_distance = distance
            if distance <= nearest_distance: nearest_distance = distance
          
        if FRUITS_COORDS:
            new_square = nfs[nearest_distance]
        else:
            new_square = self.position
        
        return new_square
        

    def move(self):
        """Move the ant weither with AI (not implemented yet) if it's set or not
        
        Return <tuple> : old position coordonate and the position coordonate of the ant 
        """
        # if random_force = 0 -> best moves
        # for further implementation, we'll add more than just 1 and 0 in order to have different AI level
        old_position = self.position
        if self.random_force:
            around_squares = self.get_around_square()
            new_square = random.choice(around_squares)
            self.position = new_square
            
        if not self.random_force:
            new_square = self.get_best_move()
            self.position = new_square
            
        self.total_moves += 1

        return (old_position, self.position)


class MyEnvironment:
    def __init__(self, nb_fruits, map_size, random_force, ctx, img, drawwidth, drawheight, line_width, position=None):
        """Constructor of the MyEnvironment class

        :param:
        :param:
        :param:
        :param:
        :param:
        :param:
        :param:
        :param:
        :param:

        Return : None
        """
        self.nb_fruits = nb_fruits
        self.map_size = map_size
        self.random_force = random_force
        self.frame_count = 0
        self.ant = Ant(nb_fruits, map_size, random_force)
        self.ctx = ctx
        self.img = img
        self.drawwidth = drawwidth
        self.drawheight = drawheight
        self.grid_line_width = line_width

    def show_map_grid(self):
        """Show the map in grid to see the background map
        
        Return : None
        """
        self.map = self.get_map()
        for line in self.map:
            print(line)

    def move(self):
        """Move the ant on the environment and check if ant ate a fruit or didn't move
        
        Return : None
        """
        self.old_pos, self.pos = self.ant.move()
        if self.old_pos != self.pos:
            new_x, new_y = self.pos
            old_x, old_y = self.old_pos
            MAP[new_y][new_x] = 3
            MAP[old_y][old_x] = 0

        if (self.pos[0], self.pos[1]) in FRUITS_COORDS:
            FRUITS_COORDS.remove((self.pos[0], self.pos[1]))
            self.nb_fruits -= 1
            self.ant.score += 1
        
        if self.ant.total_moves > self.map_size * 2:
            self.ant.score -= 1

    def get_map(self):
        return self.map
    
    def get_map_size(self):
        return self.map_size
    
    def get_nb_fruits(self):
        return self.nb_fruits

    def draw_grid(self):
        """Draw the grid on the ctx with the size of the map
        
        Return : None
        """
        offset = 0
        for line in range(self.map_size + 1):
            # drawing the line
            self.ctx.line([
                    (offset, line * (self.drawheight // self.map_size)),
                    (self.drawwidth - offset, line * (self.drawheight // self.map_size))
                    ], fill="black", width=self.grid_line_width)
            # drawing the columns
            self.ctx.line([
                    (line * (self.drawwidth // self.map_size), offset),
                    (line * (self.drawwidth // self.map_size), self.drawheight - offset)
                    ], fill="black", width=self.grid_line_width)
            
    def draw_ant(self):
        """Draw the ant on the ctx with its coordonate and set to white the old position tile
        
        Return : None
        """
        # color new tile
        x, y = self.ant.position
        tile_dimension = self.drawwidth // self.map_size 
        xnew_draw_1 = x * tile_dimension + self.grid_line_width // 2  
        ynew_draw_1 = y * tile_dimension + self.grid_line_width // 2
        xnew_draw_2 = x * tile_dimension + tile_dimension - self.grid_line_width // 2 
        ynew_draw_2 = y * tile_dimension + tile_dimension - self.grid_line_width // 2
        self.ctx.rectangle([
                           (xnew_draw_1, ynew_draw_1),
                           (xnew_draw_2, ynew_draw_2)
                           ], fill='green')
        
        if self.ant.position != self.old_pos:
            # erase old tile
            x, y = self.old_pos
            tile_dimension = self.drawwidth // self.map_size 
            xold_draw_1 = x * tile_dimension + self.grid_line_width // 2  
            yold_draw_1 = y * tile_dimension + self.grid_line_width // 2
            xold_draw_2 = x * tile_dimension + tile_dimension - self.grid_line_width // 2 
            yold_draw_2 = y * tile_dimension + tile_dimension - self.grid_line_width // 2
            self.ctx.rectangle([
                            (xold_draw_1, yold_draw_1),
                            (xold_draw_2, yold_draw_2)
                            ], fill='white')
        
    def draw_fruits(self):
        """Draw the fruits on the ctx with their coordonate
        
        Return : None
        """
        for fruit_coord in FRUITS_COORDS:
            x, y = fruit_coord
            tile_dimension = self.drawwidth // self.map_size
            xnew_draw_1 = x * tile_dimension + self.grid_line_width // 2
            ynew_draw_1 = y * tile_dimension + self.grid_line_width // 2
            xnew_draw_2 = x * tile_dimension + tile_dimension - self.grid_line_width // 2 
            ynew_draw_2 = y * tile_dimension + tile_dimension - self.grid_line_width // 2
            self.ctx.rectangle([
                            (xnew_draw_1, ynew_draw_1),
                            (xnew_draw_2, ynew_draw_2)
                            ], fill='brown')

    def render_image(self):
        """Main draw function that draw all the objects on the ctx
        
        Return : None
        """
        # draw the grid
        self.draw_grid()

       # draw the objects
        # draw the ant
        self.draw_ant()

        # draw the fruits
        self.draw_fruits()

        if len(FRUITS_COORDS) >= 0:
            self.save_image(self.frame_count)
            self.frame_count += 1

    def save_image(self, i):
        """Save the frame with its frame number on the root of the project

        :param i <int>: Frame number to save

        Return : None
        """
        abspath = os.path.abspath("static/frames")
        self.img.save(f"{abspath}\\frame{i}.jpg")

def clean_up_dir():
    path = os.path.abspath("Ant_R_learning/static/frames")
    #shutil.rmtree('/path/to/folder')


def main(nb_turn, nb_fruits, map_size, random_force=True):
    """ Main function that create the main IMG and CTX objects
    :param nb_turn <int>: Number of frame for the simulation
    :param nb_fruits <int>: Number of fruits in the simulation
    :param map_size <int>: Size of the map, number of tiles on the side
    
    Return : The score of the ant (number of fruits ate)
    """
    DRAWWIDTH = 800
    DRAWHEIGHT = 800
    LINE_WIDTH = 4

    IMG = Image.new("RGB", (DRAWWIDTH, DRAWHEIGHT), "white")
    CTX = ImageDraw.Draw(IMG)
    
    myenv = MyEnvironment(int(nb_fruits), int(map_size), random_force, CTX, IMG, DRAWWIDTH, DRAWHEIGHT, LINE_WIDTH)

    # start simulator
    turn = 0
    while turn != nb_turn and len(FRUITS_COORDS) != 0:
        myenv.move()
        myenv.render_image()
        turn += 1
    
    return myenv.ant.score


def init_map(nb_fruits, map_size):
    """Create the map and add the random fruits coordonate
    
    Return <list> : self.map
    """
    fruits_coord = []
    map = [[0 for i in range(map_size)] for j in range(map_size)]
    i = 0

    while i != nb_fruits:
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        if (x, y) not in fruits_coord:
            map[y][x] = 2
            fruits_coord.append((x, y))
            i += 1
    
    return (map, fruits_coord)

if __name__ == "__main__":
    MAP_SIZE = 15
    NB_FRUITS = 5
    NB_TURN = 60
    MAP, FRUITS_COORDS = init_map(NB_FRUITS, MAP_SIZE)

    main(NB_TURN, NB_FRUITS, MAP_SIZE, random_force=False)