#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:06:48 2017

@author: leo
"""

# -*- coding: utf-8 -*-
'''
@brief 将训练数据转化为lmdb。
@author riwei.chen
@author modified by decheng.liu
@update
    2016.04.27: 添加no_index版本。
    2016.05.02: 去除no_index
    2017.05.09: select 8,000 identi train+val data(Celebface+) 
'''
import os
TOOLS = '/home/leo/caffe/build/tools/'	
Path_Root = '/home/leo/caffe/examples/exercise-deepid1/'

save_image_size = (128,128)
def div_train_val(file_in, file_train,file_val, val_rate = 10):
    '''
	@brief 将list训练数据划分为训练数据和验证数据集
	@param file_in: 输入的文件夹列表，
	@param file_train: 输出的训练列表
	@param file_val: 输出的验证列表
	@param val_rate: 测试数据的比例，即1/val_rate的数据为val数据
    '''
    i  = 0
    fid_train = open(file_train, 'w')
    fid_val = open(file_val,'w')
    for line in open(file_in):
        if i%val_rate == 0:
            fid_val.write(line)
        else:
            fid_train.write(line)
        i+=1
    fid_train.close()
    fid_val.close()
    
def convert_for_lmdb(input_file, output_file,Image_Root):
    '''
	@brief 将ImageData格式的list文件转化为LMDB所需要的格式文件，即是否为全路径问题。
	@param input_file: 输入的原始ImageData文件list列表
	@param output_file: 输出保存的位LMDB准备的文件列表
	
	@return None
    '''
    fid_in = open(input_file)
    fid_out = open(output_file, 'w')
    for line in fid_in.readlines():
        items = line.split('\t')
        file_path = items[0]
        file_path = file_path.split(Image_Root)[1]
        fid_out.write(file_path+'\t'+items[1])
    fid_in.close()
    fid_out.close()

def convert_2_lmdb(Image_Root, file_list_name, lmdb_path, save_image_size=(128,128)):
    '''
	@brief 将list文件列表转化为lmdb格式文件
	@param Image_Root: 图像的跟路径
	@param file_list_name: 图像列表的文件名
	@param imdb_path: 保存的imdb格式的文件路径
	@param save_image_size: 保存的图像大小
	'''
    command = 'GLOG_logtostderr=1 '+TOOLS+'convert_imageset --resize_height='+str(save_image_size[0])+' --resize_width='+str(save_image_size[1])  +'  --shuffle '+Image_Root+' ' +file_list_name+' '+lmdb_path
    print command
    os.system(command)
    print 'convert done!'

def caculate_image_mean(lmdb_path, save_path):
    command_mean =TOOLS+'compute_image_mean '+  lmdb_path+' '+save_path
    os.system(command_mean)
    print 'caculate image mean done!'

if __name__ == "__main__":	
    
    '''divide train data and val data '''
    file_in = Path_Root+'data/identity_CelebA.txt'
    file_iden = Path_Root+'data/Convnet_lable.txt'
    file_iden1 = Path_Root+'data/Convnet_lable1.txt'
    file_train = Path_Root+'data/Convnet_train.txt'
    file_val = Path_Root+'data/Convnet_val.txt'
    file_Convnet = Path_Root+'data/Convnet_data.txt'  
    file_SVM = Path_Root+'data/SVM_data.txt'
    file_Test = Path_Root+'data/Test_data.txt'

    
  
    '''
    @brief: lables are arraged in order    '''      
    fid_Convnet = open(file_Convnet,'r')  
    fid_iden = open(file_iden,'w')
    
    i  = 0
    result = list()
    for line in fid_Convnet.readlines():                          #依次读取每行  
        line = line.strip().split()
        result.append(tuple(line))                            #保存  
    reresult = sorted(result, key=lambda x:x[1])
    
    i = 0
    relable = list()
    for line in reresult:
        relable = ('%s' % ' '.join(line))+'\r\n'
        fid_iden.write(relable) #保存入结果文件  
        i+=1
    fid_iden.close()

    
    
    '''    
    @brief: divide train data and val data '''    
  
    

    fid_train = open(file_train, 'w')
    fid_val = open(file_val,'w')    
    fid_iden = open(file_iden,'r')
    fid_iden1 = open(file_iden1,'w')
    i = 0   # calculate the number of total image
    iden_num = 1   #first iden's lable
    iden_sum = 0    #calulate the number of iden image
    val_rate = 10
    #calculte number of each identity      
    for line in fid_iden.readlines():    
        lable = int(line.split()[-1])
        line = line.split()
        if lable == iden_num:
            fid_iden1.write(('%s'%' '.join(line))+' '+str(iden_sum)+'\r\n')
            iden_sum+=1
        else:
            iden_sum = 0
            iden_num = lable
            fid_iden1.write('%s'%' '.join(line)+' '+str(iden_sum)+'\r\n')
            iden_sum+=1
        i+=1
        # divide train and val
        if iden_sum%val_rate == 0:
            fid_val.write('%s'%' '.join(line)+'\r\n')
        else:
            fid_train.write('%s'%' '.join(line)+'\r\n')   
  
    fid_iden.close()
    fid_train.close()
    fid_val.close()    
 
    '''
    @brief: calculate the number of iden of Convnet_train data
    '''
    
    fid_iden = open(file_iden,'r')
    iden_i = 1
    iden_n = 1
    lable_i = 0
    for line in fid_iden.readlines():
        lable = int(line.split()[-1])
        if lable == lable_i:
            iden_n+=1
        else:
            lable_i = lable
            iden_i+=1
    print iden_i
        
        
                
            
    
#    
#    for line in open(file_in):
#        
#        lable = int(line.split()[-1])
#        print lable
#        if i%val_rate == 0:
#            fid_val.write(line)
#        else:
#            fid_train.write(line)
#        i+=1
#    fid_train.close()
#    fid_val.close()
#    
#    div_train_val(file_in, file_train,file_val, val_rate = 10)
    
#    Image_Root = '/media/leo/0000EEBB000EB107/database/CelebA/img_align_celeba'
#    lmdb_path = '/home/leo/caffe/examples/exercise-deepid1/data/val'
#    file_val_lmdb = "ANet_val.list"
#    convert_2_lmdb(Image_Root, file_val_lmdb, lmdb_path, save_image_size)
#    
#    file_train_lmdb = "ANet_train.list"
#    lmdb_path = '/home/leo/caffe/examples/exercise-deepid1/data/train'
#    convert_2_lmdb(Image_Root, file_train_lmdb, lmdb_path, save_image_size)
#    
#    caculate_image_mean(lmdb_path, save_path='/home/leo/caffe/examples/exercise-deepid1/data/mean.binaryproto')
