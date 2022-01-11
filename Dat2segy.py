import os
import numpy as np
import segysak                
import xarray as xr
from segysak import segy

def write_cube(data, path):
    data = np.transpose(data,[1,2,0]).astype(np.single)
    data.tofile(path)

def read_cube(input_data_path, size):
    input_cube = np.fromfile(input_data_path, dtype=np.single)
    input_cube = np.reshape(input_cube, size)
    input_cube = input_cube.transpose((2,0,1))
    return input_cube

data_name = "cnooc"
root_path = os.path.join(os.path.abspath('.'), 'cig-cnooc', data_name)
seis_path = os.path.join(root_path, "data\prediction")
sgy_path = os.path.join(root_path, "data\prediction")
twt,iline,xline = 1252,287,735        #设置文件的维度
print(sgy_path)                       #检查一下sgy输出的文件夹 可省略

input_data_path = os.path.join(seis_path, f"seis.dat")     #输入的文件名字 可改为 预测出来的.dat
gx = read_cube(input_data_path, (xline,iline,twt))
print(input_data_path)                #检查一下

data_sgy = segysak.create3d_dataset((iline, xline, twt))
data_sgy.__setitem__("data", (('iline','xline','twt'), gx.transpose((2,1,0))))
segysak.segy.segy_writer(data_sgy, os.path.join(sgy_path, f"kerry.sgy"))     #输出sgy的文件名
