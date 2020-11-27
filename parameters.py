'''
mode = integer-> "AOO":1, "VOO":2, "AAI":3, "VVI":4, "DOO":5, 
                  "AOOR":6, "VOOR":7, "AAIR":8, "VVIR":9, "DOOR":10, "DDDR":11
Lower Rate Limit = beats per minute (BPM)
Upper Rate Limit = BPM
Atrial Amplitude = mV
Ventrical Amplitude = mV
Atrial/Ventricular Pulse Width = ms
Atrial Sensitivity = mV
Ventrical Sensitivity = mV
Refractory Period = ms
Atrial/Ventricular Delay = ms
Maximum Sensor Rate = BPM
Activity Threshold = integer V-Low:1, Low:2, Med-Low:3, Med:4, Med-High:5, High:6, V-High:7
Reaction Time = seconds
Response Factor = integer 1-16
Recovery Time = seconds
'''
class Parameters:

    def __init__(self):
        self.mode = 1
        self.lrl = 60
        self.url = 120
        self.a_amp = 5000
        self.v_amp = 5000
        self.pw = 1
        self.a_sensi = 0
        self.v_sensi = 0
        self.rp = 320
        self.av_delay = 150
        self.msr = 120
        self.act_thresh = 4
        self.react_t = 30
        self.res_fact = 8
        self.rec_t = 300
    
    __modes={ "AOO":1, "VOO":2, "AAI":3, "VVI":4, "DOO":5, \
              "AOOR":6, "VOOR":7, "AAIR":8, "VVIR":9, "DOOR":10, "DDDR":11}
    
    def save(self):
        params = { "mode": self.mode \
                 , "lrl": self.lrl \
                 , "url": self.url \
                 , "a_amp": self.a_amp \
                 , "v_amp": self.v_amp \
                 , "pw": self.pw \
                 , "a_sensi": self.a_sensi \
                 , "v_sensi": self.v_sensi \
                 , "rp": self.rp \
                 , "av_delay": self.av_delay \
                 , "msr": self.msr \
                 , "act_thresh": self.act_thresh \
                 , "react_t": self.react_t \
                 , "res_fact": self.res_fact \
                 , "rec_t": self.rec_t }
        return params

    def mode_switch(self, m):
        for key, value in Parameters.__modes.items():
            if(value==self.mode):
                current_mode = key
                break

        self.mode = Parameters.__modes[m]
        
        exec(current_mode+"_mode.configure(relief=raised)")
        exec(m+"_mode.configure(relief=sunken)")

        return
