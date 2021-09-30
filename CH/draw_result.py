import matplotlib.pyplot as plt

def draw_result(point_set, convex_hull_set):
    internal_point_set = point_set-set(convex_hull_set)
    
    i_point_x_list = []
    i_point_y_list = []
    ch_point_x_list = []
    ch_point_y_list = []

    for ip in internal_point_set:
        i_point_x_list.append(ip.x)
        i_point_y_list.append(ip.y)
    
    for chp in convex_hull_set:
        ch_point_x_list.append(chp.x)
        ch_point_y_list.append(chp.y)
    
    
    plt.scatter(i_point_x_list,i_point_y_list,c='black',s=5)
    plt.scatter(ch_point_x_list,ch_point_y_list,c = 'red',s=5)
    #plt.plot(ch_point_x_list,ch_point_y_list,c = 'red')

    plt.show()
