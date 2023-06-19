#----------------#
# Import modules # 
#----------------#

from pathlib import Path

import numpy as np
import pandas as pd
import re

#------------------#
# Define functions #
#------------------#

def find_substring_index(string,
                         substring, 
                         advanced_search=False,
                         find_whole_words=False,
                         case_sensitive=False,
                         all_cases=False):
    
    # substring: str or list of str
    #       If 'str' then it can either be as is or a regex.
    #       In the latter case, there is no need to explicitly define as so,
    #       because it connects with Python's built-in 're' module.

    if isinstance(string, str):        
        if advanced_search:
            substrLowestIdx = string_VS_string_search(string, substring, 
                                                      find_whole_words,
                                                      case_sensitive,
                                                      all_cases)
        else:
            substrLowestIdx = np.char.find(string,
                                           substring,
                                           start=0,
                                           end=None)
            

    elif isinstance(string, list)\
    or isinstance(string, tuple)\
    or isinstance(string, np.ndarray):
        
        if isinstance(string, tuple):
            string = list(string)
        
        if not advanced_search:
            if isinstance(substring, str):
                substrLowestIdxNoFilt = np.char.find(string, 
                                                     substring, 
                                                     start=0,
                                                     end=None)

                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[0].tolist()
           
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):
                
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string,
                                                             substring, 
                                                             start=0,
                                                             end=None)
                
        else:
            if isinstance(substring, str):
                substrLowestIdxNoFilt\
                = np.array([string_VS_string_search(s_el, substring,
                                                    find_whole_words,
                                                    case_sensitive, 
                                                    all_cases)
                            for s_el in string])
                
                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[0].tolist()
                
                
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):
                
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string, 
                                                             substring,
                                                             start=0, 
                                                             end=None)
                
            
    elif isinstance(string, pd.DataFrame) or isinstance(string, pd.Series):
        try:
            substrLowestIdxNoFilt = string.str.contains[substring].index
        except:
            substrLowestIdxNoFilt = string.iloc[:,0].str.contains[substring].index
        
        substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt]
        print(substrLowestIdx)
        
    if (isinstance(substrLowestIdx, list) and len(substrLowestIdx) == 1):
        return substrLowestIdx[0]
    else:
        return substrLowestIdx
            

def string_VS_string_search(string,
                            substring,
                            find_whole_words,
                            case_sensitive,
                            all_cases):
    
    # No option selected #
    #--------------------#
    
    if not case_sensitive and not all_cases and not find_whole_words:
        firstOnlyMatch = re.search(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = firstOnlyMatch.start(0)
            return substrLowestIdx
        except:
            return -1
        
    # One option selected #
    #---------------------#
        
    elif case_sensitive and not all_cases and not find_whole_words:
        firstOnlyMatch = re.search(substring, string)
        try:
            substrLowestIdx = firstOnlyMatch.start(0)
            return substrLowestIdx
        except:
            return -1
        
    elif not case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = [m.start(0) for m in allMatchesIterator]
            return substrLowestIdx
        except:
            return -1
        
    elif not case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = exactMatch.start(0)
            return substrLowestIdx
        except:
            return -1

    # Two options selected #
    #----------------------# 
    
    elif case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string)
        try:
            substrLowestIdx = [m.start(0) for m in allMatchesIterator]
            return substrLowestIdx
        except:
            return -1
        
    elif case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(substring, string)
        try:
            substrLowestIdx = exactMatch.start(0)
            return substrLowestIdx
        except:
            return -1
    

def stringList_VS_stringList_search_wholeWords(strList, 
                                               substrList, 
                                               start=0, 
                                               end=None):
    
    substrLowestIdxNoFilt\
    = np.array([np.char.find(strList, substr_el, start=0, end=None)
                for substr_el in substrList])
    
    substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[-1].tolist()
    return substrLowestIdx

    
def obj_path_specs(obj_path, splitchar=None):
    
    obj_PATH = Path(obj_path)
    
    obj_path_parent = obj_PATH.parent
    obj_path_name = obj_PATH.name
    obj_path_name_noext = obj_PATH.stem
    obj_path_ext = obj_PATH.suffix[1:]
    
    obj_specs_dict = {
        objSpecsKeys[0] : obj_path_parent,
        objSpecsKeys[1] : obj_path_name,
        objSpecsKeys[2] : obj_path_name_noext,
        objSpecsKeys[4] : obj_path_ext
        }
    
    if splitchar is not None:
        obj_path_name_noext_parts = obj_path_name_noext.split(splitchar)
        addItemDict = {objSpecsKeys[3] : obj_path_name_noext_parts}
        obj_specs_dict.update(addItemDict)
        
    return obj_specs_dict


def get_obj_specs(obj_path,
                  obj_spec_key=None,
                  splitchar=None):
    
    arg_names = get_obj_specs.__code__.co_varnames
    osk_arg_pos = find_substring_index(arg_names, 
                                       "obj_spec_key",
                                       find_whole_words=True)
    
    if obj_spec_key not in objSpecsKeys_short:
        raise ValueError(f"Wrong '{arg_names[osk_arg_pos]}' option. "
                         f"Options are {objSpecsKeys_short}.")
        
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitchar)
    
    if obj_spec_key == "parent":
        osk = objSpecsKeys[0]
        
    elif obj_spec_key == "name":
        osk = objSpecsKeys[1]
    
    elif obj_spec_key == "name_noext":
        osk = objSpecsKeys[2]
        
    elif obj_spec_key == "name_noext_parts" and splitchar is not None:
        osk = objSpecsKeys[3]
        
    elif obj_spec_key == "name_noext_parts" and splitchar is None:
        raise ValueError("You must specify a string-splitting character "
                         f"if '{arg_names[osk_arg_pos]}' == {obj_spec_key}.")
        
    elif obj_spec_key == "ext":
        osk = objSpecsKeys[4]
    
    obj_spec = obj_specs_dict[osk]
    return obj_spec
    
    
def modify_obj_specs(target_path_obj,
                     obj2change,
                     new_obj=None,
                     str2add=None):
    
    # target_path_obj : str or dict
    
    arg_names = modify_obj_specs.__code__.co_varnames
    obj2ch_arg_pos = find_substring_index(arg_names, "obj2")
    
    if obj2change not in objSpecsKeys_short:
        raise ValueError(f"Wrong {arg_names[obj2ch_arg_pos]} option. "
                         "Options are {objSpecsKeys_short}.")
    
    if not isinstance(target_path_obj, dict):
        obj_specs_dict = obj_path_specs(target_path_obj)
        
    if obj2change == "name_noext_parts" and not isinstance(new_obj, tuple):
        raise ValueError("bi gauzak bete behar dira: "
                         "tupla(aldatzeko karaktere-katea, ordezkoa")
            
    if obj2change == "parent":
        osk = objSpecsKeys[0]
        
    elif obj2change == "name":
        osk = objSpecsKeys[1]
            
    elif obj2change == "name_noext":
        osk = objSpecsKeys[2]

        if str2add is not None:
            obj_specs_dict[osk] += str2add    
            lengthened_fileName = join_obj_path_specs(obj_specs_dict)
            new_obj = lengthened_fileName
        
    elif obj2change == "name_noext_parts" and isinstance(new_obj, tuple):
        osk = objSpecsKeys[2]
        name_noext = get_obj_specs(target_path_obj, osk)
        new_obj_aux = substring_replacer(name_noext, new_obj[0], new_obj[1])
        new_obj = new_obj_aux
            
    elif obj2change == "ext":
        osk = objSpecsKeys[4]

    item2updateDict = {osk : new_obj}
    obj_specs_dict.update(item2updateDict)
    
    new_obj_path_joint = join_obj_path_specs(obj_specs_dict)
    return new_obj_path_joint
        

def join_obj_path_specs(obj_specs_dict):
           
    obj_path_ext = obj_specs_dict[objSpecsKeys[-1]]
    obj_path_name_noext = obj_specs_dict[objSpecsKeys[2]]
  
    try:
        obj_path_parent = obj_specs_dict[objSpecsKeys[0]]
    except:
        obj_path_parent = None
    
    if obj_path_parent is not None:
        joint_obj_path = f"{obj_path_parent}/{obj_path_name_noext}.{obj_path_ext}"
    else:
        joint_obj_path = f"{obj_path_name_noext}.{obj_path_ext}"
        
    return joint_obj_path


def fileList2String(obj_list):

    allobj_string = ""
    for file in obj_list:
        allobj_string += f"{file} "

    return allobj_string


def substring_replacer(string, string2find, string2replace, count=-1):
    
    if isinstance(string, str):
        string_replaced = string.replace(string2find, string2replace, count)
        
    elif isinstance(string, list) or isinstance(string, np.ndarray):
        if isinstance(string, list):
            string = np.array(string)
        string_replaced = np.char.replace(string, string2find, string2replace)
        
    elif isinstance(string, pd.DataFrame):
        string_replaced = pd.DataFrame.replace(string, string2find, string2replace)
        
    elif isinstance(string, pd.Series):
        string_replaced = pd.Series.replace(string, string2find, string2replace)
    
    return string_replaced


#------------------#
# Local parameters #
#------------------#

objSpecsKeys = ["obj_path_parent",
                "obj_path_name", 
                "obj_path_name_noext",
                "obj_path_name_noext_parts",
                "obj_path_ext"]

objSpecsKeys_short = [substring_replacer(s, "obj_path_", "")
                      for s in objSpecsKeys]