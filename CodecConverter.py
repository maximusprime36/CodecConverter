#Video codec converter
#Mass rename files and transcode with ffmpeg

#V1
#V2 - Added natsort for natural sorting of files. Prevents python-sorting from mixing up file input order
#V3 - Set output filename to match input rather than just static variable "Vid"
#V4 - Added H.265 encoding option to generate smaller files for storage
#   - Added version control details
#V5 - Added Hardware acceleration (AMD) options
#   - Fixed "Invalid Option" bug
#V6 - Added Harware acceleration (AMD) ProRes option
#V7 - Added functionality for Colour Space detection and subsequent different commands. 
#   - Defined functions globally
#   - Removed absolute ffmpeg exe path
#V8 - Added genpts and vsync flags to resovle mobile phone decoding issues 





#--------------------------------------------------------------------------------------Configure--------------------------------------------------------




#Import modules
from msilib.schema import File                                                                  
import os
import subprocess
import json
from natsort import natsorted

print("Rename Files")

#Specify filetype to process
File_Ext = input("\nPlease type in the desired file type: ")     

#Specify new filename prefix                               
File_Name = input("\nPlease choose a filename prefix: ")                                                       

#Remove dot from file type
GetType = File_Ext.split(".")

#File type variable without the dot                                                                    
File_Ext2 = GetType[1]             

#Create new empty list to store each file                                                              
File_List = []                           

#Set counter for file names                    
Counter_Set_Int = 1        

#Get current directory
Directory = os.path.dirname(os.path.realpath(__file__))     

#Function for running ffmpeg with specified parameters
def runFFmpeg(args):                                                                        
    ffmpegCMD = ["ffmpeg"] + args
    print(ffmpegCMD)       

    #Check if any errors returned
    if subprocess.run(ffmpegCMD).returncode == 0:   
        #Display message if clear                                                                    
        print ("FFmpeg Script Ran Successfully")                                        
    else:
        #Display message if not clear 
        print ("There was an error running your FFmpeg script")                                                           

#Function for command arguments, with ColorSpace variable (ProRes encoding)
def buildFFmpegArgs(colourSpace):

    parameters = {}
    parameters["video_streams"] = "0"                       #Video strean 0
    parameters["video_codec"] = "prores_ks"                 #Prores_ks codec
    parameters["profile_switch"] = "3"                      #Prores profile 3
    parameters["pixel_format"] = "yuv422p10le"              #YUV 422 
    parameters["bitrate"] = "8000"                          #Max bitrate
    parameters["audio"] = "pcm_s16le"                       #Default audio 

    if colourSpace == "bt2020":
        parameters["colour_primaries"] = "bt2020"
        parameters["colour_transfer"] = "arib-std-b67"
        parameters["colour_space"] = "bt2020nc"
        pass

    elif colourSpace == "bt709":
        parameters["colour_primaries"] = "bt709"
        parameters["colour_transfer"] = "bt709"
        parameters["colour_space"] = "bt709"
        pass

    else:
        
        print("Unsupported colour space detected %s".format(colourSpace))
        exit(1)
        
    #Arguments list
    ffmpeg_args = [

        "-fflags",                              #Generate timestamps for correct sequencing
        "+genpts",
        "-i",                                   #Input file
        i,
        "-map",                                 #Video stream
        parameters["video_streams"],
        "-c:v",                                 #Copy video 
        parameters["video_codec"],              
        "-profile:v",                           #Codec Profile
        parameters["profile_switch"],           
        "-pix_fmt",                             #Pixel Format (chroma)
        parameters["pixel_format"],             
        "-bits_per_mb",                         #Maximum bitrate
        parameters["bitrate"],      
        "-color_primaries",                     #Colour primaries                     
        parameters["colour_primaries"],
        "-color_trc",                           #Colour transfer
        parameters["colour_transfer"],          
        "-colorspace",                          #Colour space
        parameters["colour_space"],
        "-vsync",                               #Enforce CFR
        "cfr",         
        "-c:a",                                 #Copy audio
        parameters["audio"],
        (File_Name + Str_y + "_1.mov") ]        #Output file
    
    return ffmpeg_args

#Look up each file in directory
with os.scandir(Directory) as entries:    
    #For each file                                                      
    for entry in entries:         
        #Get the file extension type                                                              
        Get_Ext = os.path.splitext(entry)[-1].lower()
        #If equal to specified extension                                               
        if Get_Ext == File_Ext:           
            #Add file to list                                                           
            File_List.append(entry)                                                              

#For each file in list
for i in File_List:                                                                              

    #Set integer to string to concatenate new filename  
    Counter_Set_Str= str(Counter_Set_Int)       
    #New name = Prefix + number + File extension type                                                                           
    os.rename(i, File_Name + Counter_Set_Str + File_Ext)                 
    #Convert counter back to integer                                       
    Counter_Set_Int = int(Counter_Set_Str)    
    #Icrement counter by 1                                                                              
    Counter_Set_Int+=1                                                                                        
    
#Create new list of all files
File_List2 = os.listdir()                                                                        
#Create new empty list to store files of correct type
File_List3 = []        
#Create new empty list to store re-concatenated file names                                                                          
File_List4 = []       

#For each file in list
for i in File_List2:                                                                             

    #Create new temporary list to get correct file types
    Temp_List = i.split(".")             
    #If file type is correct                                                        
    if Temp_List[1] == File_Ext2:      
        #Add to next list                                                           
        File_List3.append(Temp_List)                                                              
    else:
        #Skip
        continue                                                                                

#For each item in file list
for i in File_List3:
    #Create variable for both elements of file name                                                                           
    NewItem = i[0] + "." + i[1]       
    #Add new concatenated variable to next list                                                           
    File_List4.append(NewItem)        

#Sort list naturally using natsort
File_List4 = natsorted(File_List4)









#--------------------------------------------------------------------------------------- MAIN ---------------------------------------------------------------------------------

#Select codec option
SelectOption = input(
    "Select one of the following options\n(1) H.264/MP4\n(2) ProRes/MOV\n(3) H.265/MP4\n(4) H.265/MP4 (GPU)\n(5) ProRes/MOV (GPU)\n")      

#If select option 1
if SelectOption == ("1"):

    #Function for getting user input (currently null)
    def grabUserInput():                                                                        

        #Create empty list
        user_input_dict = {}                                                                    

        #Default value for video streams
        user_input_dict["video_streams"] = "0"      
        #Value to specify AVC codec                                            
        user_input_dict["video_codec"] = "libx264"        
        #Default bitrate value                                      
        user_input_dict["crf"] = "17"                                                           

        #Return list
        return user_input_dict                                                                  

    #Set inital value for output filename counter
    y = 1                                                                                       
    
    #For each file in list
    for i in File_List4:                                                                         

        #Convert to string to concatenate filename
        Str_y = str(y)                                                                          

        #Function for creating the ffmpeg command
        def buildFFmpegCommand():                                                               
            
            #Variable containing user input data
            final_user_input = grabUserInput()                                                  
  
            #Specify each command, argument is prespecified or value for argument is plugged in from the finaL__user_input list
            commands_list = [                                                                   
                "-i",
                i,
                "-map",
                final_user_input["video_streams"],
                "-c:v",
                final_user_input["video_codec"],
                "-crf",
                final_user_input["crf"],
                "-c:a",
                "copy",
                ("Vid" + Str_y + "_1.mp4")
                ]

            #Return value
            return commands_list                                                                

        
        #Run ffmpeg function with given commands
        runFFmpeg(buildFFmpegCommand())                                                         

        #Convert counter back to integer
        y = int(Str_y)           
        #Increment by 1                                                               
        y += 1                   

        print("Completed")                                                                      

#If select option 2
elif SelectOption == ("2"):  

    #User specifies device type of footage
    GetDevice = input(
        "\nPlease select the device type\n(1) Samsung Galaxy\n(2)DJI Drone / Lumix G9 / GoPro\n")

    #If select sub-option 1
    if GetDevice == ("1"):

        #Function for getting color space value from metadata using ffprobe
        def get_colour_primaries(path):

            #Build ffprobe command
            cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=color_primaries",
                "-of", "json", path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)

            try:
                return data["streams"][0]["color_primaries"]
            except (KeyError, IndexError):
                return None
            
        #Set inital value for output filename counter
        y = 1    

        #For each file in list
        for i in File_List4:

            #Convert to string to concatenate filename
            Str_y = str(y)
            #Extract colour space for each file
            primaries = get_colour_primaries(i)                                                         
            #Run ffmpeg command with correct color space arguments 
            runFFmpeg(buildFFmpegArgs(primaries))
            #Convert counter back to integer
            y = int(Str_y)                            
            #Increment by 1                                              
            y += 1                                                                                  

            print("Completed")

    #If select sub-option 1
    elif GetDevice == ("2"):

        #Set inital value for output filename counter
        y = 1    

        #For each file in list
        for i in File_List4:
            #Convert to string to concatenate filename
            Str_y = str(y)
            #Run ffmpeg command with default Rec.709 arguments
            runFFmpeg(buildFFmpegArgs("bt709"))                                                    
        #Convert counter back to integer
            y = int(Str_y)       
            #Increment by 1                                                                   
            y += 1                                                                                  

            print("Completed")

        

elif SelectOption == ("3"):

    #Function for getting user input (currently null)
    def grabUserInput():                                                                        

        #Create empty list
        user_input_dict = {}                                                                    

        user_input_dict["video_streams"] = "0"                                                  #Default value for streams
        user_input_dict["video_codec"] = "libx265"                                              #Value to specify AVC codec
        user_input_dict["crf"] = "26"
        user_input_dict["preset"] = "slow"  
        user_input_dict["audio_codec"] = "aac"                                                  #Default bitrate value

        return user_input_dict                                                                  #Return list

    y = 1                                                                                       #Set inital value for output filename counter
    
    for i in File_List4:                                                                         #For each file in list

        Str_y = str(y)                                                                          #Convert to string to concatenate filename

        def buildFFmpegCommand():                                                               #Function for creating the ffmpeg command

            final_user_input = grabUserInput()                                                  #Variable containing user input data
  
            commands_list = [                                                                   #Specify each command, argument is prespecified or value for argument is plugged in from the finaL__user_input list
                
                "-i",
                i,
                "-map",
                final_user_input["video_streams"],
                "-c:v",
                final_user_input["video_codec"],
                "-crf",
                final_user_input["crf"],
                "-c:a",
                final_user_input["audio_codec"],
                "-b:a",
                "1536k",
                ("Vid" + Str_y + "_1.mp4")
                ]

            return commands_list                                                                #Return value

        runFFmpeg(buildFFmpegCommand())                                                         #Run ffmpeg function with given commands

        y = int(Str_y)                                                                          #Convert counter back to integer
        y += 1                                                                                  #Increment by 1

        print("Completed")         


elif SelectOption == ("4"):

    #Function for getting user input (currently null)
    def grabUserInput():       

        #Create empty list
        user_input_dict = {}                                                                    
         #Default value for video streams
        user_input_dict["video_streams"] = "0"        
        #Value to specify HEVC codec                                         
        user_input_dict["video_codec"] = "hevc_amf"                                              
        user_input_dict["quality_1"] = "15"
        user_input_dict["quality_2"] = "15"
        user_input_dict["quality_3"] = "qvbr"
        #Default bitrate value
        user_input_dict["rate"] = "15"  
        user_input_dict["audio_codec"] = "aac"                                                  

        #Return list
        return user_input_dict                                                                  

    #Set inital value for output filename counter
    y = 1                                                                                       
    
    #For each file in list
    for i in File_List4:                                                                         

        #Convert counter to string to concatenate filename
        Str_y = str(y)                                                                          

        #Function for creating the ffmpeg command
        def buildFFmpegCommand():                                                               

            #Variable containing user input data
            final_user_input = grabUserInput()                                                  
  
            #Specify each command, argument is prespecified or value for argument is plugged in from the finaL__user_input list
            commands_list = [                                                                   
                "-i",
                i,
                "-map",
                final_user_input["video_streams"],
                "-c:v",
                final_user_input["video_codec"],
                "-rc",
                final_user_input["quality_3"], 
                "-qvbr_quality_level",
                final_user_input["rate"],
                "-qp_p",
                final_user_input["quality_1"],
                "-qp_i",
                final_user_input["quality_2"],
                "-c:a",
                final_user_input["audio_codec"],
                "-b:a",
                "1536k",
                ("Vid" + Str_y + "_1.mp4")
                ]

            #Return value
            return commands_list                                                                

        #Run ffmpeg function with given commands
        runFFmpeg(buildFFmpegCommand())                                                         

        #Convert counter back to integer
        y = int(Str_y)     
        #Increment by 1                                                                     
        y += 1                                                                                 

        print("Completed")       



elif SelectOption == ("5"): 

    def grabUserInput():    

        def filterInput(message, default):  
            user_input = input (message)   

            if user_input == "":            
                user_input = default       
            return user_input               

        user_input_dict = {}    

        user_input_dict["hardware_accel"] = "vulkan"
        user_input_dict["hardware_dev"] = "vulkan=amd_gpu"
        user_input_dict["filter_dev"] = "amd_gpu"
        user_input_dict["video_codec"] = "prores_ks"
        user_input_dict["profile_switch"] = "2"
        user_input_dict["quality_switch"] = "1"

        return user_input_dict  

    y = 1
    
    for i in File_List4:

        Str_y = str(y)

        def buildFFmpegCommand():   

            final_user_input = grabUserInput()  
  
            commands_list = [   
                "-hwaccel",
                final_user_input["hardware_accel"],
                "-init_hw_device",
                final_user_input["hardware_dev"],
                "-filter_hw_device",
                final_user_input["filter_dev"],
                "-i",
                i,
                "-c:v",
                final_user_input["video_codec"],
                "-profile:v",
                final_user_input["profile_switch"],
                "-qscale:v",
                final_user_input["quality_switch"],
                "-c:a",
                "pcm_s16le",
                (File_Name + Str_y + "_1.mov")
                ]

            return commands_list    

        runFFmpeg(buildFFmpegCommand())

        y = int(Str_y)
        y += 1

        print("Completed")                              

else:
    print("Invalid Option")