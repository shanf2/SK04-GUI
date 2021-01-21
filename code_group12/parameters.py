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
Activity Threshold = integer V-Low:1, Low:2, Med-Low:3, Med:4, Med-High:5, High:6, V-High:7
Reaction Time = seconds
Response Factor = integer 1-16
Recovery Time = seconds
Maximum Sensor Rate = BPM
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
        self.act_thresh = 4
        self.react_t = 30
        self.res_fact = 8
        self.rec_t = 300
        self.msr = 120
    
    #Mode names and associated numbers
    __modes={ "AOO":1, "VOO":2, "AAI":3, "VVI":4, "DOO":5, \
              "AOOR":6, "VOOR":7, "AAIR":8, "VVIR":9, "DOOR":10, "DDDR":11}
    
    #Return a dictionary of parameters to save to database
    def save(self, uid):
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
                 , "act_thresh": self.act_thresh \
                 , "react_t": self.react_t \
                 , "res_fact": self.res_fact \
                 , "rec_t": self.rec_t \
                 , "msr": self.msr \
                 , "uid": uid }
        return params

    #Update class members with new values form pdict
    def update(self, pdict):
        self.mode = pdict["mode"]
        self.lrl = pdict["lrl"]
        self.url = pdict["url"]
        self.a_amp = pdict["a_amp"]
        self.v_amp = pdict["v_amp"]
        self.pw = pdict["pw"]
        self.a_sensi = pdict["a_sensi"]
        self.v_sensi = pdict["v_sensi"]
        self.rp = pdict["rp"]
        self.av_delay = pdict["av_delay"]
        self.act_thresh = pdict["act_thresh"]
        self.react_t = pdict["react_t"]
        self.res_fact = pdict["res_fact"]
        self.rec_t = pdict["rec_t"]
        self.msr = pdict["msr"]
    
    #Determine the name of the current mode
    def get_mode(self):
        for key, value in Parameters.__modes.items():
            if(value==self.mode):
                current_mode_name = key
                break
        return current_mode_name

    #Change the mode
    def mode_switch(self, m):
        current_mode_num = self.get_mode()

        self.mode = Parameters.__modes[m]

        return current_mode_num
    
    #Useful parameters in each mode
    def params_used(self, mode):

        useful= { "AOO": ["lrl", "url", "a_amp", "pw"] \
                , "VOO": ["lrl", "url", "v_amp", "pw"] \
                , "AAI": ["lrl", "url", "a_amp", "pw", "a_sensi", "rp"] \
                , "VVI": ["lrl", "url", "v_amp", "pw", "v_sensi", "rp"] \
                , "DOO": ["lrl", "url", "a_amp", "v_amp","pw", "av_delay"] \
                , "AOOR": ["lrl", "url", "a_amp", "pw", "msr", "act_thresh", "react_t", "res_fact", "rec_t"] \
                , "VOOR": ["lrl", "url", "v_amp", "pw", "msr", "act_thresh", "react_t", "res_fact", "rec_t"] \
                , "AAIR": ["lrl", "url", "a_amp", "pw", "msr", "rp", "a_sensi", "act_thresh", "react_t", "res_fact", "rec_t"] \
                , "VVIR": ["lrl", "url", "v_amp", "pw", "msr", "rp", "v_sensi", "act_thresh", "react_t", "res_fact", "rec_t"] \
                , "DOOR": ["lrl", "url", "a_amp", "v_amp", "pw", "av_delay", "msr", "act_thresh", "react_t", "res_fact", "rec_t"] \
                , "DDDR": ["lrl", "url", "a_amp", "v_amp", "pw", "av_delay", "msr", "rp", "a_sensi", "v_sensi", "act_thresh", "react_t", "res_fact", "rec_t"] }

        return useful[mode]