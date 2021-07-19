import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    ###################File loading#######################################
    file=open('anonymized_project.json')
    data = json.load(file)
    file=open('references.json')
    reference = json.load(file)
    file.close()

    ''' 
    print(reference)
    print(data['results']['root_node']['results']['cfa36c30-31ab-4647-bbc0-7e505db482ac']['results'])
    '''
    A=[]
    B=[]
    C=[]
    D=[]
    result = []
    time = []
    balance = []

    ################## storing of interesting data in lists ###############################
    for id in data['results']['root_node']['results']:
        chunk = data['results']['root_node']['results'][id]
        for i in range(0,len(chunk)):
            annotators = chunk['results'][i]['user']['vendor_user_id']
            img_id = chunk['results'][i]['root_input']['image_url']
            D.append(img_id[-12:-4])

            if annotators[10] =='0':
                A.append(eval(annotators[11]))
            else:
                A.append(eval(annotators[10::]))
            B.append(chunk['results'][i]['task_output']['cant_solve'])
            C.append(chunk['results'][i]['task_output']['corrupt_data'])
            result.append(chunk['results'][i]['task_output']['answer'])
            time.append(chunk['results'][i]['task_output']['duration_ms'])

    ###################Using the reference data set to assess annotators##########################
    time_history = [0]*23
    subjects=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    successful_counts =[0]*23
    print('Successful counts per annotator',successful_counts)
    for i in reference:
        #print(reference[i])
        if reference[i]['is_bicycle']==True:
            balance.append(1)
            index_temp = D.index(i)
            if result[D.index(i)] == 'yes':
                ann_temp = A[D.index(i)]
                successful_counts[ann_temp]+=1
        else:
            balance.append(0)

        ann_temp = A[D.index(i)]
        time_history[ann_temp]+=time[D.index(i)]   ###sum of times for each annotator

    count =0
    for i in range(0,len(B)):
        if i==True:
            B[i]=1
            count +=1
        else:
            B[i]=0
    for i in range(0,len(C)):
        if i==True:
            C[i]=1
            count +=1
        else:
            C[i]=0

    print('There are:', max(A), 'annotators')
    print('There are:', count, 'incidences')
    print(B)
    print(C)
    print('successful counts per annotator',successful_counts)
    print('time statistic: min, max, avr')
    print(min(time),max(time),sum(time)/len(time))

    ##########W Calculation of the average time per annotator #########################
    time_history = [i/len(A) for i in time_history]

    #################Plots###############################################################

    plt.hist(balance)
    plt.title('reference set')
    plt.xlabel('label')
    plt.ylabel('count')
    plt.show()

    plt.hist(A)
    plt.title('Annotation histogram')
    plt.xlabel('Annotator number')
    plt.ylabel('count')

    plt.show()

    plt.bar(subjects, successful_counts[1::])
    plt.title('Successful counts')
    plt.xlabel('Annotator')
    plt.ylabel('count')
    plt.show()

    plt.bar(subjects, time_history[1::])
    plt.title('Average time per annotator')
    plt.xlabel('Annotator')
    plt.ylabel('time')
    plt.show()
    print(time_history)


    print(len(data['results']['root_node']['results']))
