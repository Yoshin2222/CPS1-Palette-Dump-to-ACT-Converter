import os

def verify_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)

def verify_input():
    PATH = os.path.dirname(os.path.realpath(__file__))
    suffix = ".bin"
    filename = input("Input filename, minus the .bin extension\n")
    test = os.path.join(PATH,filename+suffix)
    print(test)
    while not os.path.isfile(test):
        filename = input("Invalid filename, try something else\n")
        test = os.path.join(PATH,filename+suffix)
        print(test)
    with open(test,"rb") as inp:
        temp = inp.read()
    return [filename,temp]

#Name of bin file, data to convert
def convert_bin_to_ACT(path,data):
    #The CPS1 handles palettes using 16-bits, 4 bits for RGB respectively, and 4
    #for "brightness". Even Capcom themselves seemed to ignore these upper bits, so
    #we will too. They aren't need for conversion anyway as .ACT files store each
    #colour in its own byte, the file ending with 0x0FFFFF
    verify_folder(path)

    act_Out = []
    for i in range(0,len(data),2):
        #Set R, ignore upper 4 bits
        r = (data[i]&0x0F) << 4
        g = ((data[i+1]&0xF0))
        b = (data[i+1]&0x0F) << 4
        act_Out.append(r)
        act_Out.append(g)
        act_Out.append(b)

    #Export each 256 palette
    index = 0
    for i in range(0,len(act_Out),0x300):
        dat = act_Out[i:i+0x300]
        out_path = os.path.join(path,"{}_{}.ACT".format(path,index))
        with open(out_path,"wb") as out:
            dat = [byte for byte in dat]
            dat.append(0x0F)
            dat.append(0xFF)
            dat.append(0xFF)
            out.write(bytes(dat))
            index += 1

def main():
    file = verify_input()
    convert_bin_to_ACT(file[0],file[1])

if __name__ == "__main__":
    main()