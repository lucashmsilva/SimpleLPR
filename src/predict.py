from os import listdir
from os.path import splitext, join, realpath, dirname
from sklearn.externals import joblib
import segmentation
from copy import deepcopy
import sys

algs = ['svm_rbf','svm_linear','kneighbors','sgd', 'mlp','mlp_sgd','mlp_adam']
letters = {
            '0':[0,0], '1':[0,0], '2':[0,0], '3':[0,0], '4':[0,0], '5':[0,0],
            '6':[0,0], '7':[0,0], '8':[0,0], '9':[0,0], 'A':[0,0], 'B':[0,0],
            'C':[0,0], 'D':[0,0], 'E':[0,0], 'F':[0,0], 'G':[0,0], 'H':[0,0],
            'I':[0,0], 'J':[0,0], 'K':[0,0], 'L':[0,0], 'M':[0,0], 'N':[0,0],
            'P':[0,0], 'R':[0,0], 'S':[0,0], 'T':[0,0], 'U':[0,0], 'V':[0,0],
            'W':[0,0], 'X':[0,0], 'Y':[0,0], 'Z':[0,0]
          }
letter_predict = {}
cont_100 = {}
ac_geral = {}
cont_100_geral = []
cont_100_geral.append(0)

def load_models(models_dir="../models"):
    models = []
    for alg in algs:
        current_dir = dirname(realpath(__file__))
        model_dir = join(current_dir, models_dir+'/'+alg+'/'+alg+'.pkl')
        models.append(joblib.load(model_dir))
    return models

def load_plates(plates_path="../imgs/plates/", plate=None):
    if not plate == None:
        plate_label = splitext(plate)[0]
        return ([plate], [plate_label])
    else:
        plates = listdir(plates_path)
        plate_labels = [splitext(p)[0] for p in plates]
        return (plates,plate_labels)

def preditc(plate, plate_label, models, plates_path="../imgs/plates/", verbose=0):
    characters,column_list = segmentation.segment(plates_path,plate)
    segmentation.disp_img()
    if characters == None:
        return -1

    classification_result = [[]]
    for model in models:
        result = []
        for each_character in characters:
            each_character = each_character.reshape(1, -1);
            result.append(model.predict(each_character))
        classification_result.append(result)

    plate_strings = []
    for model_predict in classification_result:
        plate_string = ''
        for eachPredict in model_predict:
            plate_string += eachPredict[0]
        plate_strings.append(plate_string)

    plate_strings = plate_strings[1:]

    sorted_strigs = []
    column_list_copy = column_list[:]
    column_list.sort()
    for plate_string in plate_strings:
        rightplate_string = ''
        for each in column_list:
            rightplate_string += plate_string[column_list_copy.index(each)]
        sorted_strigs.append(rightplate_string)
    
    compute_preditcion(sorted_strigs,plate_label,verbose=verbose)

    return 1
   
def compute_preditcion(sorted_strigs, plate_label, verbose=0):
    alg = 0
    sorted_by_model = []
    for s in sorted_strigs:
        cont_ac = 0;
        for i in range(0,len(s)):
            letter_predict[algs[alg]][s[i]][0] += 1
            if s[i] == plate_label[i]:
                letter_predict[algs[alg]][s[i]][1] += 1
                cont_ac += 1
        # ac = 1.0*len([i for i, j in zip(s, plate_label) if i == j])/len(s)*100
        ac = 1.0*cont_ac/len(s)*100
        ac = round(ac,2)
        sorted_by_model.append((algs[alg],s,ac))
        alg += 1
    sorted_by_model.sort(key=lambda tup: tup[2])
    sorted_by_model.reverse()

    alg = 0
    if verbose == 1: print('{:<22s} {:<5s}'.format("LABEL:", plate_label))
    print(sorted_by_model[0][0],sorted_by_model[0][2])
    if 100.0 == sorted_by_model[0][2]:
        cont_100_geral[0] += 1
    for model_name,string,ac in sorted_by_model:
        opt = ""
        if(ac == 100.0):
            opt = "***"
            cont_100[model_name] += 1
        ac_geral[model_name] += ac 
        if verbose == 1: print('{:<10s} {:<10s} {:<5s}'.format(model_name,"PREDICTION:",string),str(ac)+"%",opt)
        alg += 1

    segmentation.disp_img()

###############################################################################################

def test_all():
    plates,plate_labels = load_plates();
    n_plates = len(plates)

    for i in algs:
        letter_predict.update({i:deepcopy(letters)})
        cont_100.update({i:0})
        ac_geral.update({i:0})

    models = load_models()

    right_seg = 0
    i = 0
    for plate in plates:
        plate_label = plate_labels[i]
        if 'O' in plate_label:
            plate_label = plate_label.replace('O','0')
        print(plate_label)
        res = preditc(plate, plate_label, models)
        if res != -1:
            right_seg += 1
        i += 1

    models[:] = []
    f = open("result",'w')
    output = []
    seg_rate = 1.0*right_seg/n_plates
    round(seg_rate,2)
    output.append("ACERTO NA SEGMENTAÇÃO: " + str(right_seg)+'/'+str(n_plates)+'\n')
    output.append('\t\t'+str(seg_rate))
    f.writelines(output)
    output[:] = []

    rate = 1.0*cont_100_geral[0]/right_seg
    rate = round(rate,2)
    output.append("\nACERTO GERAL USANDO TODOS MODELOS: " + str(cont_100_geral[0])+'/'+str(right_seg)+'\n')
    output.append('\t\t'+str(rate))
    f.writelines(output)
    output[:] = []

    i = 0
    for alg in algs:
        output.append("\n" + alg + ":\n")

        output.append("\tACERTO GERAL: " + str(cont_100[alg])+"/"+str(right_seg)+'\n')
        rate = 1.0*cont_100[alg]/right_seg
        rate = round(rate,2)
        output.append('\t\t'+ str(rate) + "\n")

        output.append("\tACERTO MEDIO EM TODAS PLACAS: " + str(round(ac_geral[alg],2))+"/"+str(right_seg)+'\n')
        rate = 1.0*ac_geral[alg]/right_seg
        rate = round(rate,2)
        output.append('\t\t'+ str(rate) + "\n")

        output.append("\tACERTO POR LETRA:\n")
        for key, value in sorted(letter_predict[alg].items()):
            rate = 0
            if(value[0] != 0):
                rate = 1.0*value[1]/value[0]
                rate = round(rate,2)
            output.append("\t\t" + str(key) + " : " + str(rate) + "\n")

        output.append('\n')
        i += 1
        f.writelines(output)
        output[:] = []
    cont_100_geral[0] = 0  

def test_one(plate):
    for i in algs:
        letter_predict.update({i:deepcopy(letters)})
        cont_100.update({i:0})
        ac_geral.update({i:0})
    
    models = load_models()
    p,p_label = load_plates(plate=plate)
    preditc(p[0],p_label[0],models,verbose=1)

try:
    arg = sys.argv[1]
    if arg == "-a":
        test_all()
    elif arg == "-t":
        plate = sys.argv[2]
        test_one(plate)
    else:
        print("Usage: python3 predict.py [OPTIONS] [IMAGE FILENAME]")
        print("[OPTIONS]\n \t-a \t Test with entire plate dataset (doesn't require filename)\n \t-t \t Test with one image (filiname must be provided <label.png>)")
except Exception as e:
        print("Usage: python3 predict.py [OPTIONS] [IMAGE FILENAME]")
        print("[OPTIONS]\n \t-a \t Test with entire plate dataset (doesn't require filename)\n \t-t \t Test with one image (filiname must be provided <label.png>)")
