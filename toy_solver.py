#
# Given some parameters, see if we can find X's

model = [0.00027337005594505457, 45.83556746097803]

def eval(X, Y):
    # Using the model that we've been given, generate the Y values

    # Regenerate the stats 
    xmin = min(X)
    xmax = max(X)
    fit = np.polyfit( X, 

