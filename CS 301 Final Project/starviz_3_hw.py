'''
Created on Apr 26, 2018

@author: Amairani Zepeda
'''

############################################################################################################################
###The code below displays an animated plot of lightning strikes that occurred in each month from 1998 to 2017.          ###
###It also displays a 3D plot showing the number of lightning strikes that occurred from 1998 to 2017.                   ###
###From the output plot, we can conclude that most of the lightning strikes occurred in the months of May through August.###
###Also, the highest number of lightning strikes occurred in August, 2014.                                               ###
############################################################################################################################

import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import spline
from mpl_toolkits.mplot3d import Axes3D

#checks if the input argument is valid
if len(sys.argv) > 1:
    print "Too many arguments provided."
    print "Please run as: python starviz_3_hw.py"
if len(sys.argv) == 1:
    def interpret_csv(filename):
        
        """This function takes in a filename as a csv file type.
           Returns a list of dictionaries containing only day and count data.
        """
        ls_data = pd.read_csv(filename)
        ls_list = []; count = 0
        for day_row in ls_data["DAY"]:
            ls_dict = {}
            #checks if the first two characters of the string are digits
            if day_row[0:2].isdigit():
                ls_dict["DAY"] = day_row[0:2] + day_row[len(day_row)-4:len(day_row)]
                ls_dict["FCOUNT"] = ls_data["FCOUNT"][count]
            elif day_row[0:1].isdigit():
                ls_dict["DAY"] = "0" + day_row[0:1] + day_row[len(day_row)-4:len(day_row)]
                ls_dict["FCOUNT"] = ls_data["FCOUNT"][count]
            ls_list += [ls_dict]; count += 1     
        return ls_list
    
    def create_lists(dl):
        
        """This function takes in a list of dictionaries.
           Returns a tuple of lists for the x-axis as months and y-axis as the lightning strike count.
        """
        x_list = []; y_list = []
        for dictionary in dl:
            x_list += [int(dictionary["DAY"][0:2])] #takes in month values
            y_list += [dictionary["FCOUNT"]] #takes in count values
        count = 0; listlen = len(x_list)
        while count < listlen:
            #adds values in the y-axis list that have the same matching index month values 
            if count != listlen-1 and x_list[count] == x_list[count+1]: 
                y_list[count] += y_list[count+1]
                x_list.pop(count+1); y_list.pop(count+1)
                listlen -= 1; count -= 1
            count += 1
        return x_list, y_list
    
    def add_zeros(data_lists):
        
        """This function takes in a tuple of lists for the x and y axis.
           Returns a tuple of lists with zeros added for months with no lightning strike occurrences.
        """
        for i in range(240):
            try:
                #checks if a month is missing in the x-axis list
                if (i+1)%12 != 0 and data_lists[0][i]%12 != (i+1)%12:
                    data_lists[0].insert(i, (i+1)%12)
                    data_lists[1].insert(i, 0)
                if (i+1)%12 == 0 and data_lists[0][i]%12 != (i+1)%12:
                    data_lists[0].insert(i, 12)
                    data_lists[1].insert(i, 0)
            except IndexError:
                #checks if a month is missing at the end of the x-axis list
                if (i+1)%12 != 0:
                    data_lists[0].append((i+1)%12)
                if (i+1)%12 == 0:
                    data_lists[0].append(12)
                data_lists[1].append(0)
        return data_lists
    
    def mod_lists(data_lists):
        
        """This function takes in a tuple of lists.
           Returns a tuple of lists each containing 20 lists each containing 12 values.
        """
        x_lists = []; y_lists = [] #final lists of lists
        x_list = []; y_list = [] #temporary lists
        for i in range(240):
            #checks if the temporary lists contain 12 values
            if len(x_list) != 12 and len(y_list) != 12:
                x_list.append(data_lists[0][i]); y_list.append(data_lists[1][i])
            if len(x_list) == 12 and len(y_list) == 12:
                x_lists += [x_list]; y_lists += [y_list]
                x_list = []; y_list = []
        return x_lists, y_lists
    
    def axis_data(x_list, y_list):
        
        """This function takes in two lists of lists representing the x and y axis.
           Returns two arrays, one for the x-axis and the other for the y-axis
        """
        x=np.array(x_list)
        y=np.array(y_list)
        return x, y
    
    #2D Plot
    data_dict = interpret_csv("lightning_strike_data.csv")
    data_list = mod_lists(add_zeros(create_lists(data_dict)))
    x_list = data_list[0]; y_list = data_list[1]
    
    #Used code from https://stackoverflow.com/questions/42035779/animating-with-matplotlib-without-animation-function
    for year in range(20):
        x,y = axis_data(x_list[year], y_list[year])
        #resets the graph to go through each year
        plt.gca().cla() 
        plt.xlim(1,12); plt.ylim(-50, 400)
        #smoothes the lines (decided not to use this since it showed too much inaccuracy)
        x_smooth = np.linspace(x.min(), y.max(), 2700) 
        y_smooth = spline(x,y,x_smooth)
        #plot, format, and labels
        plt.title("Lightning Strikes in " + str(1998+year))
        plt.xticks(x, ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        plt.xlabel('Month'); plt.ylabel('Number of Lightning Strikes')
        plt.plot(x, y)
        plt.pause(0.5)
     
    #3D Plot  
    fig = plt.figure(figsize = (8,8))
    ax = plt.axes(projection='3d')
    
    x = np.array(x_list); y = np.array(y_list)
    z = np.array([i + 1 for i in range(20)])
    plt.xticks(x[0], ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    plt.xlabel('Month'); plt.ylabel('Number of Lightning Strikes')
    ax.plot3D(x, y, z)
    plt.show()