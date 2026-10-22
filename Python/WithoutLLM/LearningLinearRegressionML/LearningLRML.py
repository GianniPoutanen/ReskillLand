import numpy


def run():
    # Step 1  - collect data - x is hours studied, y is score achieved
    points = numpy.genfromtxt('data.csv', delimiter=',')
    
    # Step 2 - define hyperparameters - tuning nobs - the params that defines how the model is analysing the data
    
    # How fast the model converges to the optimal solution - learning rate 
    # too small - model takes too long to converge, too large - model may never converge
    learning_rate = 0.0001
    
    # y = mx + b (slope formula) - we need to find the optimal values for m and b
    initial_b = 0  # initial y-intercept guess
    initial_m = 0  # initial slope guess
    num_iterations = 1000  # number of iterations to run the gradient descent algorithm
    
    # Step 3 - train model - using gradient descent to find optimal values for m and b
    print("starting gradient descent at b = {0}, m = {1}, error = {2}"
          .format(initial_b, initial_m, compute_error_for_line_given_points(initial_b, initial_m, points)))
    [b,m] = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
    print("ending point after {0} iterations b = {1}, m = {2}, error = {3}"
          .format(num_iterations, b, m, compute_error_for_line_given_points(b, m, points)))
    
def compute_error_for_line_given_points(b, m, points):
    # This function computes the error for a line defined by slope m and y-intercept b given a set of points
    total_error = 0
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        # Getting sum of squared errors - (y - (mx + b))^2
        total_error += (y - (m * x + b)) ** 2
    # Return average error - total error divided by number of points
    return total_error / float(len(points))
    
def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
    # This function runs the gradient descent algorithm to find the optimal values for m and b
    b = starting_b
    m = starting_m
    
    # Gradient descent algorithm - iteratively update b and m to minimize the error
    for i in range(num_iterations):
        b, m = step_gradient(b, m, numpy.array(points), learning_rate)
    return [b, m]

def step_gradient(b_current, m_current, points, learning_rate):
    # This function computes the gradient for b and m and updates their values
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        # Calculate the gradients for b and m
        # This gives the direction in which the error is travelling - we want to move in the opposite direction of the gradient to minimize the error
        b_gradient += -(2/N) * (y - ((m_current * x) + b_current))
        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current))
    
    # Update b and m using the gradients and learning rate
    new_b = b_current - (learning_rate * b_gradient)
    new_m = m_current - (learning_rate * m_gradient)
    
    return [new_b, new_m]
    

if __name__ == "__main__":
    run()