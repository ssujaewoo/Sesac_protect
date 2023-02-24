import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt
import matplotlib.pyplot as plt
cred = credentials.Certificate('/home/pi/Downloads/webapp/nugunaaiot1-firebase-adminsdk-yc79i-cb185525cb.json') #firebase key
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def db_set():  #DB setting
    doc_ref = db.collection('user').document('송예성')
    doc_ref.set({
    })

def db_upload(good, bad, empty, count): #upload DB
    
    doc_ref = db.collection('user').document('송예성')
    doc_ref.update({str(count): {'Good_posture': good,
                            'Bad_posture': bad,
                            'Empty': empty,
                            'upload_time': firestore.SERVER_TIMESTAMP
                            }
                    })
def db_visual_all_pie():  #Draw pie graph
    user_ref = db.collection('user').document('송예성').get()
    user_dict = user_ref.to_dict()

    good_sum = 0
    bad_sum = 0
    
    for k in user_dict.keys():
        good_sum += user_dict[k]['Good_posture']
        bad_sum += user_dict[k]['Bad_posture']
        
    values = [good_sum, bad_sum]
    
    return values

def db_visual_table():  #Draw table
    user_ref = db.collection('user').document('송예성').get()
    user_dict = user_ref.to_dict()
    key_list = []

    for i in range(1, len(user_dict.keys())+1):
        key_list.append(str(i))
    
    for k in key_list:
        user_dict[k]['upload_time'] = user_dict[k]['upload_time'] + dt.timedelta(hours=9)
        user_dict[k]['upload_time'] = user_dict[k]['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
    
    return user_dict, key_list
