import pygame
import random
import ModelFull
import numpy as np
import DecisionTree
import csv

pygame.init()
TheModel = ModelFull.createModel()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (106,13,173)

global reward
reward = 0 
global score
score = 0
global game_close
game_close = False

dis_width = 800
dis_height = 600
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake AI w17006484')
 
clock = pygame.time.Clock()

global snake_speed
snake_block = 10

global tree
tree = DecisionTree.ReturnTree()

font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont("comicsansms", 35)

SnakeArray = [0,0,0,0,0,0,0,0,0]

 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, red)
    dis.blit(value, [0, 0])

 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/3, dis_height/3])
    
def message2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/10, dis_height/2])
    
def message3(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/3, dis_height/1.5])
    
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
def PredictText(text):
    SampleData = np.array(text)
    SD = SampleData.reshape(1,9)
    theNum = TheModel.predict_classes(SD)
    
    if (theNum==[[1]]):
        return "east"
    elif (theNum==[[0]]):
        return "north"
    elif (theNum==[[3]]):
        return "west"
    elif (theNum==[[2]]):
        return "south"
    else:
        print("I DON'T KNOW")
        
def AddToDoc(TSnakeArray2, TreeResult, TSnakeArray):
    TSnakeArray[0] = TSnakeArray2[0]
    fields = np.array(TSnakeArray)
    x = tree.predict([TSnakeArray])
    fields2 = np.array(x)
    if str(x[0]) == "[0. 0. 0. 1.]":
        fields2 = np.array([0,0,0,1])
    if str(x[0]) == "[0. 0. 1. 0.]":
        fields2 = np.array([0,0,1,0])
    if str(x[0]) == "[0. 1. 0. 0.]":
        fields2 = np.array([0,1,0,0])
    if str(x[0]) == "[1. 0. 0. 0.]":
        fields2 = np.array([1,0,0,0])
    arr = np.concatenate((fields, fields2))
    print(arr)
    with open(r'FullSnake.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(arr)
    print("The training database has updated!")
def GetTreeResult(SnakeArray):
    x = tree.predict([SnakeArray])
    if str(x[0]) == "[0. 0. 0. 1.]":
        return "west"
    if str(x[0]) == "[0. 0. 1. 0.]":
        return "south"
    if str(x[0]) == "[0. 1. 0. 0.]":
        return "east"
    if str(x[0]) == "[1. 0. 0. 0.]":
        return "north"
def BothWereWrong(TSnakeArray2, TreeResult, TSnakeArray):
    LocalLoop = True
    key = False
    pygame.display.update()
    dis.fill(white)
    message2("Please press the key corresponding to the correct direction", red)
    pygame.display.update()
    while LocalLoop == True:
        message3("",red)
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        fields2 = np.array([0,0,0,1])
                        key = True
                        LocalLoop = False
                    if event.key == pygame.K_RIGHT:
                        fields2 = np.array([0,1,0,0])
                        key = True
                        LocalLoop = False
                    if event.key == pygame.K_DOWN:
                        fields2 = np.array([0,0,1,0])
                        key = True
                        LocalLoop = False
                    if event.key == pygame.K_UP:
                        fields2 = np.array([1,0,0,0])
                        key = True
                        LocalLoop = False
        if key == True:
            TSnakeArray[0] = TSnakeArray2[0]
            fields = np.array(TSnakeArray)        
            arr = np.concatenate((fields, fields2))
            print(arr)
            with open(r'FullSnake.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(arr)
            print("The training database has updated!")
def gameLoop():  # creating a function
    game_over = False
    game_close = False

    snake_speed = 8
    x1 = dis_width / 2
    y1 = dis_height / 2
    
    global TreeResult
    TreeResult = "hello"
    
    x1_change = 0
    y1_change = 0
    
    SnakeArray2 = [0,0,0,0,0,0,0,0,0]
    frame = 0
    
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
 
    while not game_over:
        while game_close == True:
            #Reset function of game
            message("Press Q-Quit or C-Play Again", red)
            message2("The Decision Tree thinks you'd live if you went (%s)" % TreeResult, red)
            message3("if it was right, press Y, otherwise, press N", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_y:
                        AddToDoc(SnakeArray2, TreeResult, SnakeArray)
                    if event.key == pygame.K_n:
                        BothWereWrong(SnakeArray2, TreeResult, SnakeArray)
                        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                #Allows for manual movement by user, if that's ever relevant
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    SnakeArray[0]=5
                elif event.key == pygame.K_F5:
                    game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Allows the user to place the food
                (x,y) = pygame.mouse.get_pos()
                x = round(x/10)*10
                y = round(y/10)*10
                foodx,foody = (x,y)
                print(pygame.mouse.get_pos())
                
        #check the snake position to feed to the AI
        #Start to check if the snake will hit it's tail
        
        SnakeArray[1] = 0
        SnakeArray[3] = 0
        SnakeArray[5] = 0
        SnakeArray[7] = 0
        if x1+10 >= dis_width:#if there is a wall to the east
            SnakeArray2[3]=SnakeArray[3]
            SnakeArray[3] = 1
        else:
            SnakeArray2[3]=SnakeArray[3]
            SnakeArray[3] = 0
        if x1-10<0:#if there is a wall to the west
            SnakeArray2[5]=SnakeArray[5]
            SnakeArray[5] = 1
        else:
            SnakeArray2[5]=SnakeArray[5]
            SnakeArray[5] = 0
        if y1 +10 >= dis_height:#if there is a wall to the south
            SnakeArray2[7]=SnakeArray[7]
            SnakeArray[7] = 1
            
        else:
            SnakeArray2[7]=SnakeArray[7]
            SnakeArray[7] = 0
        if y1 -10 < 0:
            SnakeArray2[1]=SnakeArray[1]
            SnakeArray[1] = 1
        else:
            SnakeArray2[1]=SnakeArray[1]
            SnakeArray[1] = 0
        #Start to check if the snake is on the same plane as the food
        if round(x1/10)*10 == foodx and foody > y1:
            SnakeArray2[8]=SnakeArray[8]
            SnakeArray[8] = 1
        else:
            SnakeArray2[8]=SnakeArray[8]
            SnakeArray[8] = 0
        if round(x1/10)*10 == foodx and foody < y1:
            SnakeArray[2] = 1
        else:
            SnakeArray[2] = 0
        if round(y1/10)*10 == foody and foodx > x1:
            SnakeArray2[4]=SnakeArray[4]
            SnakeArray[4] = 1
        else:
            SnakeArray2[4]=SnakeArray[4]
            SnakeArray[4] = 0
        if round(y1/10)*10 == foody and foodx < x1:
            SnakeArray2[6]=SnakeArray[6]
            SnakeArray[6] = 1
        else:
            SnakeArray2[6]=SnakeArray[6]
            SnakeArray[6] = 0
        for x in snake_List[:-1]: #check if the snake is next to it's tail
            if(x[0]-10==x1 and x[1]==y1):
                SnakeArray2[3]=SnakeArray[3]
                SnakeArray[3]=1
            if(x[0]+10==x1 and x[1]==y1):
                SnakeArray2[5]=SnakeArray[5]
                SnakeArray[5]=1
            if(x[1]+10==y1 and x[0]==x1):
                SnakeArray2[1]=SnakeArray[1]
                SnakeArray[1]=1
            if(x[1]-10==y1 and x[0]==x1):
                SnakeArray2[7]=SnakeArray[7]
                SnakeArray[7]=1
            
        #Feed the AI the information and ask for direction
        print("The data that is sent to the AI is: ", SnakeArray)
        
        directionGo = (PredictText(SnakeArray))
        print("The Neural Network has decided to go with the direction: ", directionGo)
        if (directionGo=="east"):
            #If the AI says go east, go positive along the X axis
             x1_change = snake_block
             y1_change = 0
             SnakeArray2[0]=SnakeArray[0]
             SnakeArray[0]=3
             
        elif (directionGo=="north"):
            #if the AI says go north, go negative aloing tthe Y axis
             y1_change = -snake_block
             x1_change = 0
             SnakeArray2[0]=SnakeArray[0]
             SnakeArray[0]=2
        elif (directionGo=="west"):
            #if the AI says go west, go negative along the X axis
             x1_change = -snake_block
             y1_change = 0
             SnakeArray2[0]=SnakeArray[0]
             SnakeArray[0]=5
        elif (directionGo=="south"):
            #if the AI goes south, go positive along the Y axis
             y1_change = snake_block
             x1_change = 0
             SnakeArray2[0]=SnakeArray[0]
             SnakeArray[0]=4
         
        #Check if the Snake is dead
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            TreeResult = GetTreeResult(SnakeArray)
            game_close = True
            
        #If the snake is nor dead, move it in the direction it chose to move
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        #draw vision0
        vision = 0
        while vision<2500:
            #Draws the vision range for food
            pygame.draw.rect(dis,purple, [vision,y1, snake_block, snake_block])
            pygame.draw.rect(dis,purple, [x1,vision, snake_block, snake_block])
            vision+=1
        #Draws the vision boxes for the danger
        pygame.draw.rect(dis,red, [x1,y1-10, snake_block, snake_block])
        pygame.draw.rect(dis,red, [x1,y1+10, snake_block, snake_block])
        pygame.draw.rect(dis,red, [x1+10,y1, snake_block, snake_block])
        pygame.draw.rect(dis,red, [x1-10,y1, snake_block, snake_block])
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
        #Store the location of the snake
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
            #Check if the snake is goin g to bash into itself and perish
        for x in snake_List[:-1]:
            if x == snake_Head:
                TreeResult = GetTreeResult(SnakeArray)
                game_close = True
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        #update the score
        frame = frame+1
        #To stop the game from going on for too long, if the AI doesn't find food within 1,000 moves it dies
        if(frame>60000):
            TreeResult = "You timed the snake out"
            game_close = True
        pygame.display.update()
        #When food gets eaten, make snake bigger and hide food
        #Until user clicks again
        if x1 == foodx and y1 == foody:
            snake_speed +=100
            foodx = -9999
            foody = -9999
            frame = 0
            Length_of_snake += 1
        clock.tick(snake_speed)
    pygame.quit()

def returngametype():
    return game_close
def returnSnakeArray():
    return SnakeArray

gameLoop()