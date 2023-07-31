def is_point_inside_rect(point, rect):
        """this method is used to check if a mouse click action is inside 
        a button
        Args:
            point (x,y): mouse click position
            rect (x,y,width,height): the position of the button on screen

        Returns:
            bool: 
        """      
        x, y = point
        rect_x, rect_y, rect_width, rect_height = rect
        return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height