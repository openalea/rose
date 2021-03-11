#### Not optimized but part of the model

I_threshold = 3.
slope = 0.281857451404
intercept = 0.630237580994

def burst_delay_law(I):
    if I < I_threshold : return  (I - intercept)/ slope 
    return None

def I_law(duration):
    if not duration is None : return  duration * slope + intercept 
    return None
