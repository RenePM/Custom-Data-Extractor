#**import field
# More Divide & Conquer inspired classes

# Class that reads field one-by-one, by removing the read part or
# it can read a specific value using a field start endIds list "conditions"
# that can extract all specified fields based on fieldsConditionChain "rules"
# NOTE: If Chain take up to much stack space consider redesigning to use "thisNode" method to serach for data & nodes instead of search using Recursive calls
# STATUS: COMPLETED, TESTED, WORKING
# TODO: Make enum for Types and ensure enum import error bug is fixed!!
# TODO: Redesign to use same simi-recursive node handling and design as my analysisNodeTree, hence helper/wrapper functions that call core functions etc...
# TODO: Redesign to look like nodeTree (and use thisNode = self & ret -1 => ret "", nodeIx_ used to find conditions) but just for nodeChains, key should be called nodeId_ so that i have a standard name of item id's to make my classes more portable & flexible

# a field and its attriutes
class   field(object):
    def __init__(self, value_, startId_, startIx_, endId_, endIx_):
        self.value_ = value_
        self.startIx_ = startIx_
        self.startId_ = startId_
        self.endIx_ = endIx_
        self.endId_ = endId_

class fieldReader(object):
    def __init__(self, line_=""):
        self.error_ = "" # Holds "thisError text, can be read to see what went wrong when a nodeChain method returns nothing"

        # Set conditionNode attributes
        self.fields_ = {} # Dict of identified fields

        self.startId_ = "" # last found field->startId
        self.endId_ = "" # last found field->endId
        self.value_ = "" # last found field->value, Keeps track of the value extracted using thisCondition
        self.matchValue_ = "" # Set the value that a condition must match for the condition to be met
        self.startIx_ = 0
        self.endIx_ = 0
        self.line_ = line_        

    # Gets last/thisError that occured whil handling thisNode
    def getError(self):
        return self.error_

#---------------- Reset field search --------------------
    # Restart Search from ix 0
    def restart(self):
        self.fields_ = [] # Reset the known fields dictonary
        self.offsetIx_ = 0
        self.startIx_ = 0
        self.endIx_ = 0
        self.startId_=""
        self.endId_ = ""
        self.value_
#--------------------------------------------------------

#---------------- Move to char Ix -----------------------
    # Move to the specified relative (thisIx + ix) line char ix if it is valid
    def moveRelIx(self, offsetIx_):
        self.startIx_ += offsetIx_

    # Move to the specified Absolute line char ix if it is valid
    def moveAbsIx(self, offsetIx_):
        self.startIx_ = offsetIx_    
#--------------------------------------------------------

# ------------------- load new line -----------------------
    def loadLine(self, line_):
        self.line_ = line_

#-----------------------------------------------------------

# --------------- FIND fields and values ---------------
    # Returns a field value if start and endId match is found, Search relative from from this startIx + offsetIx
    # Use matchValue to specifie one or more field->values that result must match
    # NOTE: use getFieldValueAbs() if you are reading the fields in random order!!
    # NOTE: unique Name must be set if you want to store the field as an object
    def getFieldValueRel(self, name_="", startIds_=[], endIds_=[], matchValues_ = [], offsetIx_=0, caseSensitiveIds_=0, caseSensitiveValues_=0):
        # Keep track of prev StartIx
        prevStartIx = self.startIx_

        # Move to next field
        self.startIx_ = self.endIx_

        # Find first startId
        startIx = -1
        for startId in startIds_:
            # Is search case sensitive?
            if(caseSensitiveIds_ == 1):
                #YES
                startIx = self.line_.find(startId, self.startIx_ + offsetIx_)
            else: # NO
                startIx = self.line_.lower().find(startId.lower(), self.startIx_ + offsetIx_)

            # Was a valid startId found?
            if(startIx != -1):
                #YES
                thisStartId = startId
                break

        # Has startId(s) been specified?
        if(len(startIds_) == 0):
            # Assume no startId and cont. search from prevField
            thisStartId = ""
            startIx = self.startIx_

        # Was a valid startId found/located?
        if(startIx == -1):
            #NO => Condition not met
            # Restore StartIx
            self.startIx_ = prevStartIx
            return ""

        # Assume startIx was located
        # Has endId(s) been specified
        if(len(endIds_) == 0):
            # Update field info
            self.startIx_ = startIx
            self.startId_ = thisStartId

            # Assume read to end-of-line
            # Get Field->value->startIx
            valueStartIx = startIx + len(thisStartId)
            # Set endIx to length of string
            endIx = len(self.line_)

            # Update field info
            self.endIx_ = endIx
            self.endId_ = "" 
        else: # YES
            # Update field info
            self.startIx_ = startIx
            self.startId_ = thisStartId

            # Get Field->value->startIx
            valueStartIx = startIx + len(thisStartId)
            
            # Find endId
            endIx = -1
            for endId in endIds_:
                # Is search case senstive?
                if(caseSensitiveIds_ == 1):
                    #YES
                    endIx = self.line_.find(endId, valueStartIx)
                else: #NO
                    endIx = self.line_.lower().find(endId.lower(), valueStartIx)

                # Was a valid endId found?
                if(endIx != -1):
                    # YES
                    # update field info
                    self.endId_ = endId
                    self.endIx_ = endIx + len(endId)
                    break
            
            # Was the endId found?
            if(endIx == -1):
                #NO => Field coundtion not met
                return ""

        # Has a matchValue been specified?
        if(len(matchValues_) == 0):
            # NO
            # Update filed info
            self.matchValue_ = ""
            self.value_ = self.line_[valueStartIx:endIx]

            # Has name been specified?
            if(name_ != ""):
                #YES
                # Add new Field object to know fields
                newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
                self.fields_[name_] = newField

            # Return the value
            return self.value_
        else: # YES
            # Get the this value
            thisValue = self.line_[valueStartIx:endIx]
            for values in matchValues_:
                # Does thisValue match the specifed value
                # is the matching case sensitive?
                if(caseSensitiveValues_ == 0):
                    #NO
                    if(values == thisValue):
                        # Updae field info
                        self.value_ = thisValue

                        # Has name been specified?
                        if(name_ != ""):
                            # Add new Field object to know fields
                            newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
                            self.fields_[name_] = newField                            
                            
                        # Valid value found => return it
                        return thisValue
                else: # YES
                    if(values.lower() == thisValue.lower()):
                        # Update field info
                        self.value_ = thisValue

                        # Has name been specified?
                        if(name_ != ""):                        
                            # Add new Field object to know fields
                            newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
                            self.fields_[name_] = newField                            
                            
                        # Valid value found => return it
                        return thisValue

        # Assume somthing went wrong
        return ""

    # Returns a field value if start and endId match is found, Search from this Absolute offsetIx
    # Useful when reading fields in random order
    def getFieldValueAbs(self, name_="", startIds_=[], endIds_=[], matchValues_ = [], offsetIx_=0, caseSensitiveIds_=0, caseSensitiveValues_=0):
        # Keep track of prev StartIx
        prevStartIx = self.startIx_

        # Move to abs ix
        self.startIx_ = offsetIx_
        
        # Find first startId
        startIx = -1
        for startId in startIds_:
            # Is search case sensitive?
            if(caseSensitiveIds_ == 1):
                #YES
                startIx = self.line_.find(startId, self.startIx_)
            else: # NO
                startIx = self.line_.lower().find(startId.lower(), self.startIx_)
            
            # Was a valid startId found?
            if(startIx != -1):
                #YES
                thisStartId = startId
                break

        # Has startId(s) been specified?
        if(len(startIds_) == 0):
            # Assume no startId and cont. search from prevField
            thisStartId = ""
            startIx = self.startIx_

        # Was a valid startId found/located?
        if(startIx == -1):
            #NO => Condition not met
            # Restore StartIx
            self.startIx_ = prevStartIx
            return ""

        # Assume startIx was located
        # Has endId(s) been specified
        if(len(endIds_) == 0):
            # Update field info
            self.startIx_ = startIx
            self.startId_ = thisStartId

            # Assume read to end-of-line
            # Get Field->value->startIx
            valueStartIx = startIx + len(thisStartId)
            # Set endIx to length of string
            endIx = len(self.line_)

            # Update field info
            self.endIx_ = endIx
            self.endId_ = "" 
        else: # YES
            # Update field info
            self.startIx_ = startIx
            self.startId_ = thisStartId

            # Get Field->value->startIx
            valueStartIx = startIx + len(thisStartId)

            # Find endId
            endIx = -1
            for endId in endIds_:
                # Is search case senstive?
                if(caseSensitiveIds_ == 1):
                    #YES
                    endIx = self.line_.find(endId, valueStartIx)
                else: #NO
                    endIx = self.line_.lower().find(endId.lower(), valueStartIx)

                # Was a valid endId found?
                if(endIx != -1):
                    # YES
                    # update field info
                    self.endId_ = endId
                    self.endIx_ = endIx + len(endId)
                    break
            
            # Was the endId found?
            if(endIx == -1):
                #NO => Field coundtion not met
                return ""

        # Has a matchValue been specified?
        if(len(matchValues_) == 0):
            # NO
            # Update filed info
            self.matchValue_ = ""
            self.value_ = self.line_[valueStartIx:endIx]

            # Has name been specified?
            if(name_ != ""):
                # Add new Field object to know fields
                newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
                self.fields_[name_] = newField

            # Return the value
            return self.value_
        else: # YES
            # Get the this value
            thisValue = self.line_[valueStartIx:endIx]
            for values in matchValues_:
                # Does thisValue match the specifed value
                # is the matching case sensitive?
                if(caseSensitiveValues_ == 0):
                    #NO
                    if(values == thisValue):
                        # Updae field info
                        self.value_ = thisValue

                        # Has name been specified?
                        if(name_ != ""):
                            # Add new Field object to know fields
                            newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)                            
                            self.fields_[name_] = newField                            
                            
                        # Valid value found => return it
                        return thisValue
                else: # YES
                    if(values.lower() == thisValue.lower()):
                        # Update field info
                        self.value_ = thisValue

                        # Has name been specified?
                        if(name_ != ""):
                            # Add new Field object to know fields
                            newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
                            self.fields_[name_] = newField

                        # Valid value found => return it
                        return thisValue

        # Assume somthing went wrong
        return ""


    # Returns a field object with the specified name
    def getField(self, name_):
        if(name_ in self.fields_.keys()):
            return self.fields_[name_]
        
        # Assume the field was not found
        return ""

    # Returns a field object for last found field
    def getThisField(self):        
        # Create new field objetc containg last found field
        newField = field(self.value_, self.startId_, self.startIx_, self.endId_, self.endIx_)
        
        return newField        
 
     # Returns a field value if start and endId match is found, Search from this Absolute offsetIx
     # And removes the found field using slice method
     # NOTE: Does not support field objects, use non slicing version to keep track of fields
    def getFieldValueRelAndSlice(self, name_="", startIds_=[], endIds_=[], matchValues_ = [], offsetIx_=0, caseSensitiveIds_=0, caseSensitiveValues_=0):

        # Need to use absolute, since we keep slicing the string
        thisField = self.getFieldValueAbs(name_, startIds_, endIds_, matchValues_, offsetIx_, caseSensitiveIds_, caseSensitiveValues_)

        # Was a valid field found?
        if(thisField == ""):
            return ""

        # Remove the field from the string
        self.line_ = self.line_[:self.startIx_] + self.line_[self.endIx_:]

        return thisField


     # Returns a field value if start and endId match is found, Search from this Absolute offsetIx
     # And removes the found field using slice method
     # NOTE: DOES NOT SUPPORT field objects, use non slicing version to keep track of fields
    def getFieldValueAbsAndSlice(self, name_="", startIds_=[], endIds_=[], matchValues_ = [], offsetIx_=0, caseSensitiveIds_=0, caseSensitiveValues_=0):

        thisField = self.getFieldValueAbs(name_, startIds_, endIds_, matchValues_, offsetIx_, caseSensitiveIds_, caseSensitiveValues_)

        # Was a valid field found?
        if(thisField == ""):
            return ""

        # Remove the field from the string
        self.line_ = self.line_[:self.startIx_] + self.line_[self.endIx_:]

        return thisField        

#---------------------------