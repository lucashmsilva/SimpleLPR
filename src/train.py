import os
import numpy as np
from sklearn.externals import joblib

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn.ensemble import AdaBoostClassifier

from skimage.io import imread
from skimage.filters import threshold_otsu, threshold_local
from skimage.exposure import equalize_hist
from skimage.morphology import binary_closing

letters = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
          ]

models_dict = {
           'svm_rbf' : SVC(),
        'svm_linear' : SVC(kernel='linear'),
        'kneighbors' : KNeighborsClassifier(n_neighbors=3, weights='distance', n_jobs=-1),
               'sgd' : SGDClassifier(n_jobs=-1),
               'mlp' : MLPClassifier(solver='lbfgs' , alpha=1e-5, random_state=1),
           'mlp_sgd' : MLPClassifier(solver='sgd' ,alpha=1e-5, random_state=1,learning_rate='adaptive'),
          'mlp_adam' : MLPClassifier(solver='adam' ,alpha=1e-5, random_state=1)
              }

def read_training_data(training_directory):
    image_data = []
    target_data = []
    print(">>> LOADING CHAR IMAGES")
    for each_letter in letters:
        size = len(os.listdir(os.path.join(training_directory, each_letter)))
        for each in range(0,size):
            image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.png')
            img_details = imread(image_path, as_grey=True)

            img_details = img_details * 255
            img_details = equalize_hist(img_details)

            bin_otsu = img_details < threshold_otsu(img_details, 21)
            bin_otsu = binary_closing(bin_otsu)
            flat_bin_image = bin_otsu.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)

            bin_local = img_details < threshold_local(img_details, block_size=25)
            bin_local = binary_closing(bin_local)
            flat_bin_image = bin_local.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)
    
    print(">>> FINISHED LOADING CHAR IMAGES")
    return (np.array(image_data), np.array(target_data))

def cross_validation(model, num_of_fold, train_data, train_label):
    print(">>> VALIDATING MODEL")

    accuracy_result = cross_val_score(model, train_data, train_label, cv=num_of_fold)
    
    print("Cross Validation Result for ", str(num_of_fold), " -fold")

    print(accuracy_result * 100)

def model_dumper(model, save_directory, file_subdir, file_name):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    joblib.dump(model, save_directory+file_name)
    print(">>> DUMPED MODEL .plk TO ", save_directory)

def train_all(dataset_dir, model_names=['svm_rbf','svm_linear','kneighbors','sgd', 'mlp','mlp_sgd','mlp_adam']):
    image_data, target_data = read_training_data(dataset_dir)
    train_images, test_images, train_labels, test_labels = train_test_split(image_data, target_data, train_size=0.9, random_state=0)
    current_dir = os.path.dirname(os.path.realpath(__file__))

    for m_name in model_names:
        print(">>> TRAININ USING:", m_name)
        model = models_dict.get(m_name)
        model.fit(train_images, train_labels)
        print(">>> FINISHED TRAINING")
        print("SCORE FOR",m_name,"=",model.score(test_images, test_labels))

        file_subdir = '../models/'+m_name+'/'
        file_name = '/'+m_name+'.pkl'
        model_dumper(model, file_subdir,file_subdir,file_name)


###############################################################################################

dataset_dir = "../imgs/dataset"

train_all(dataset_dir,['mlp'])

