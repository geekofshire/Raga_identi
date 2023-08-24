import os
import librosa
import webview
import subprocess
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = r'C:\Users\soham\Desktop\Coding\Project\New folder\Music_classifier'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return "No audio file part"
        
        audio_file = request.files['audio_file']
        
        if audio_file.filename == '':
            return "No selected file"
        
        if audio_file:
            temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(temp_file_path)
            output = main(temp_file_path)
            return output
    
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="audio_file">
        <input type="submit" value="Upload">
    </form>'''


def main(str):
    print("Enter song path : ")
    # path = r"Laga Chunari Mein Daag.wav"
    path = str
    try:
        os.remove('res.wav')
    except:
        """"""
    subprocess.call(['ffmpeg', '-i', path, 'res.wav'])
    y, sr = librosa.load(path, sr=22050, mono=True)
    print(len(y))
    
    obtained_thaat = []
    possible_thaat_list = []
    thaat_count = []
    d = 50
    
    n_frames = int(np.ceil(len(y) / sr))
    n_samples = int(np.ceil(n_frames / d))

    for i in range(n_samples):
        if(i==n_samples-1):
            end = len(y)
            start = end - sr * d
        else:
            start = i * sr * d
            end = start + sr * d

        y_sample = y[start:end]
        sr_sample = sr
        obt_thaat = main_2(y_sample, sr_sample)
        for i in obt_thaat:
            obtained_thaat.append(i)
        
    print()
    print()
    print()
    for i in obtained_thaat:
        if(i in possible_thaat_list):
            idx = possible_thaat_list.index(i)
            thaat_count[idx] = thaat_count[idx] + 1
        else:
            possible_thaat_list.append(i)
            thaat_count.append(1)
    
    print(possible_thaat_list)
    
    therapy = healing_therapies(possible_thaat_list)
    
    return therapy



def healing_therapies(thaat_list):
    thaat = ["Bilawal", "Kalyan", "Khamaj", "Kafi", "Asavari", "Todi", "Poorvi", "Marva", "Bhairavi", "Bhairav"]
    
    therapy = ["Gives healthy mind and body",
               "Control sound and sonorous sleep",
               "Reduce mental tension",
               "Relief from headache",
               "Relief from cough and cold",
               "Relief from problems of high blood pressure",
               "Can cure Rheumatic Arthritis",
               "Relief from asthma",
               "Prevents hysteria",
               "Brings joy",
               "Mitigate insomina",
               "Reduces anxiety",
               "Reduces hypertension",
               "Brings Creativity and Happiness",
               "Cure low blood pressure",
               "Control psychological hazards and builds confidence",
               "Used for constipation",
               "Brings serenity",
               "Enhances compassion and patience",
               "Relief from High fever",
               "Relief from phlegm, toothache, intestinal gas, sinusitis",
               "It can be used for Emotional strength, Devotion and Peace, Restful Sleep, Tranquility, Relaxation & Rest",
               "Peace Integration"]
    
    therapy_choice = [[1,2],
                      [3,4,5,6,7],
                      [2,3,8,9],
                      [1,10,11,12,13],
                      [3,13,14,15,16,17],
                      [3,4,5,9,12,18],
                      [3,11],
                      [0,9,19],
                      [4,14,19,20,21],
                      [4,5,18,22]]
    
    therapy_number = []
    for i in range(len(thaat)):
        if(thaat[i] in thaat_list):
            for j in therapy_choice[i]:
                if(j not in therapy_number):
                    therapy_number.append(j)
    
    print()
    print()
    print("Possible therapies of the song : ")
    
    dict = {}
    for i in range(len(therapy_number)):
        print((i+1), end='. ')
        print(therapy[therapy_number[i]])
        dict[i+1] = therapy[therapy_number[i]]
    print()
    return dict


def closest_array(str_arr1, str_arr2):

    # Finding jaccard similarity of the obtained notes with the database notes
    similarities = []
    for i in range(len(str_arr2)):
        similarity = jaccard_similarity(str_arr1, str_arr2[i])
        similarities.append((similarity, i))
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    ret = []
    ret.append(similarities[0][1])
    # print(len(similarities))
    for i in range(len(similarities)):
        if(i==0):
            continue
        if(similarities[i-1][0]==similarities[i][0]):
            ret.append(similarities[i][1])
        else:
            break
    
    # Now, for tie cases we calculate the similarity by taking the closest among the possible options
    similarities = []
    for i in ret:
        similarity = check_similarity(str_arr1, str_arr2[i])
        similarities.append((similarity, i))
    similarities.sort(key=lambda x: x[0], reverse=False)
    
    # Taking the thaats that have lowest difference, if we still have multiple thaats then we are printing both of them as possible
    ret = []
    print(similarities)
    ret.append(similarities[0][1])
    for i in range(len(similarities)):
        if(i==0):
            continue
        if(similarities[i-1][0]==similarities[i][0]):
            ret.append(similarities[i][1])
        else:
            break
    return ret

def jaccard_similarity(str_arr1, str_arr2):

    # Making two sets of the arrays and finding the arrays with the most similarities
    set1 = set(str_arr1)
    set2 = set(str_arr2)
    intersection = set1.intersection(set2)
    return len(intersection)

def check_similarity(str_arr1, str_arr2):

    # Finding the non-matching notes
    note = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
    num_note = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    set1 = set(str_arr1)
    set2 = set(str_arr2)
    intersection = set1.intersection(set2)
    set1 = set1-intersection
    set2 = set2-intersection
    
    set1 = list(set1)
    set2 = list(set2)
    
    # Calculating distance of the closest notes in the array
    sum_dist = 0
    for i in range(len(set1)):
        for j in range(len(note)):
            if set1[i]==note[j]:
                sum_dist += num_note[j]
                set1[i] = num_note[j]
    
    for i in range(len(set2)):
        for j in range(len(note)):
            if set2[i]==note[j]:
                sum_dist -= num_note[j]
                set2[i] = num_note[j]
                
    return abs(sum_dist)


def find_thaat(obt_thaat):
    
    # The dataset of the various songs
    thaat = ["Bilawal", "Kalyan", "Khamaj", "Kafi", "Asavari", "Todi", "Poorvi", "Marva", "Bhairavi", "Bhairav"]
    check_thaat = [np.array(["C", "G", "D", "E", "F", "A", "B"]), 
                   np.array(["C", "G", "D", "E", "F#/Gb", "A", "B"]),
                   np.array(["C", "G", "D", "E", "F", "A", "A#/Bb"]), 
                   np.array(["C", "G", "D", "D#/Eb", "F", "A", "A#/Bb"]),
                   np.array(["C", "G", "D", "D#/Eb", "F", "G#/Ab", "A#/Bb"]), 
                   np.array(["C", "G", "C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]),
                   np.array(["C", "G", "C#/Db", "E", "F#/Gb", "G#/Ab", "B"]), 
                   np.array(["C", "G", "C#/Db", "E", "F#/Gb", "A", "B"]),
                   np.array(["C", "G", "C#/Db", "D#/Eb", "F", "G#/Ab", "A#/Bb"]), 
                   np.array(["C", "G", "C#/Db", "E", "F", "G#/Ab", "B"])]
    
    obt_thaat = np.array(obt_thaat)
    
    # Finding the closest thaat corresponding to the obtained pitch values
    closest_index = closest_array(obt_thaat, check_thaat)
    possible_thaat_list = []
    print("Thaat(s) :", end=' ')
    for i in closest_index:
        possible_thaat_list.append(thaat[i])
        print(thaat[i], end=' ')
    
    return possible_thaat_list


def find_closest(list, list1, list2, target):

    closest_index = 0
    for i in range(len(list1)):
        if abs(list1[i] - target) < abs(list2[closest_index] - target):
            closest_index = i
    
    for i in range(len(list2)):
        if abs(list2[i] - target) < abs(list2[closest_index] - target):
            closest_index = i
    
    for i in range(len(list)):
        if abs(list[i] - target) < abs(list[closest_index] - target):
            closest_index = i
    
    return closest_index


def octave_table(most_prominent_note):
    
    # Intialising the notes and the octave values of the notes
    note = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
    octave2 = [65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47]
    octave3 = [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94]
    octave4 = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88]
    
    octave2_ll = [64.72855, 68.70765, 72.7327, 77.1305, 81.8172, 86.722, 91.7842, 97.03175, 102.94515, 109.19075, 115.5236, 122.10605]
    octave3_ll = [129.4471, 137.4053, 145.4554, 154.261, 163.6244, 173.434, 183.5684, 194.0635, 205.8803, 218.3815, 231.0472, 244.2121]
    octave4_ll = [258.9042, 274.8106, 290.9108, 308.532, 327.2588, 346.878, 367.1268, 388.127, 411.7606, 436.763, 462.0944, 488.4242]
    
    octave2_hl = [66.09145, 69.89235, 74.1073, 78.4295, 83.0028, 87.898, 93.2158, 98.96825, 104.71485, 110.80925, 117.5564, 124.83395]
    octave3_hl = [132.1729, 139.7747, 148.2046, 156.859, 165.9956, 175.786, 186.4316, 197.9365, 209.4197, 221.6185, 235.1128, 249.6679]
    octave4_hl = [264.3558, 279.5494, 296.4092, 313.728, 332.0012, 351.582, 372.8532, 395.873, 418.8394, 443.237, 470.2256, 499.3358]   
    
    octave_to_be_used_ll = []
    octave_to_be_used_hl = []
    octave_to_be_used = []
    
    # Finding under which note the most prominent note will fall
    if(most_prominent_note < 127.14):
        octave_to_be_used = octave2
        octave_to_be_used_ll = octave2_ll
        octave_to_be_used_hl = octave2_hl
        
    elif(most_prominent_note < 254.286):
        octave_to_be_used = octave3
        octave_to_be_used_ll = octave3_ll
        octave_to_be_used_hl = octave3_hl
    else:
        octave_to_be_used = octave4
        octave_to_be_used_ll = octave4_ll
        octave_to_be_used_hl = octave4_hl
    
    # Finding the note of the most prominent note
    closest = find_closest(octave_to_be_used, octave_to_be_used_ll, octave_to_be_used_hl, most_prominent_note)
    
    final = []
    final.append(most_prominent_note)
    
    # Finding the other pitch values of the notes of the octave
    for i in range(closest):
        number = (octave_to_be_used[closest-i-1]/octave_to_be_used[closest-i]) * final[0]
        final.insert(0,number)
    
    for i in range(closest,(len(octave_to_be_used)-1)):
        number = (octave_to_be_used[i+1]/octave_to_be_used[i]) * final[i]
        final.append(number)
    
    # Calculatng errors of formulated pitch and actual pitch
    for i in range(len(final)):
        final[i] = abs(octave_to_be_used[i]-final[i])/octave_to_be_used[i]
        
    # Sorting according to the least errors
    for i in range(len(final)):
        for j in range(len(final)):
            if(final[i]<final[j]):
                temp = final[i]
                final[i] = final[j]
                final[j] = temp
                
                temp = note[i]
                note[i] = note[j]
                note[j] = temp

    # Appending the corresponding notes       
    thaat = []
    thaat.append(note[closest])
    c = 0
    for i in range(len(final)):
        if(note[closest]==note[i]):
            continue
        thaat.append(note[i])
        c = c+1
        
    print(thaat)
    obtained_thaat = find_thaat(thaat[0:7])
    return obtained_thaat

def check(x):
    octave2_ll = [64.72855, 68.70765, 72.7327, 77.1305, 81.8172, 86.722, 91.7842, 97.03175, 102.94515, 109.19075, 115.5236, 122.10605]
    octave3_ll = [129.4471, 137.4053, 145.4554, 154.261, 163.6244, 173.434, 183.5684, 194.0635, 205.8803, 218.3815, 231.0472, 244.2121]
    octave4_ll = [258.9042, 274.8106, 290.9108, 308.532, 327.2588, 346.878, 367.1268, 388.127, 411.7606, 436.763, 462.0944, 488.4242]
    
    octave2_hl = [66.09145, 69.89235, 74.1073, 78.4295, 83.0028, 87.898, 93.2158, 98.96825, 104.71485, 110.80925, 117.5564, 124.83395]
    octave3_hl = [132.1729, 139.7747, 148.2046, 156.859, 165.9956, 175.786, 186.4316, 197.9365, 209.4197, 221.6185, 235.1128, 249.6679]
    octave4_hl = [264.3558, 279.5494, 296.4092, 313.728, 332.0012, 351.582, 372.8532, 395.873, 418.8394, 443.237, 470.2256, 499.3358]   
    
    for i in range(len(octave4_hl)):
        if((x>=octave2_ll[i] and x<=octave2_hl[i]) or (x>=octave3_ll[i] and x<=octave3_hl[i]) or (x>=octave4_ll[i] and x<=octave4_hl[i])):
            return 1
    
    return 0

def main_2(y,sr):
    print()
    print()
    print()
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    
    arr = []
    # Taking the pitches in a array which are in the range of 50-500
    for i in range(len(pitch)):
        for j in range(len(pitch[i])):
            if(int(pitch[i][j])>=int(50) and int(pitch[i][j])<=int(500)):
                arr.append(int(pitch[i][j]))

    # Finding the most prominent note
    most_prominent_note = max(set(arr), key=arr.count)
    print(most_prominent_note)

    # Finding the notes
    obtained_thaat = octave_table(most_prominent_note)
    try:
        os.remove("res.wav")
    except:
        """"""
    return obtained_thaat


if __name__ == '__main__':
    app.run(debug=True)
    #webview.start()
