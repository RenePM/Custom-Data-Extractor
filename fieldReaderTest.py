
# STATUS: Completed, Working, Tested
import fieldReader

# ----------------- module tests -----------------
def testFieldSlicer():
# Test slicer
    myFieldReader = fieldReader.fieldReader(myLine)
    nameFieldValue = myFieldReader.getFieldValueRelAndSlice("name", endIds_=[","])
    nameField = myFieldReader.getField("name")
    ageFieldValue = myFieldReader.getFieldValueRelAndSlice("age", ["age:"], [","]) 
    ageField = myFieldReader.getField("age")
    emailFieldValue = myFieldReader.getFieldValueRelAndSlice("email", ["e-mail:"], [","])
    emailField = myFieldReader.getField("email")
    addressFieldValue = myFieldReader.getFieldValueRelAndSlice("address", ["address:"], [","])
    addressField = myFieldReader.getField("address")
    zipcodeFieldValue = myFieldReader.getFieldValueRelAndSlice("zipcode", ["zip:"])
    zipcodeField = myFieldReader.getField("zipcode")
    # Read the field->values in reverse order to demonstrate the power of the condition chains
    print("------ testFieldSlicer() ----------")
    print("value of zip: " + zipcodeField.value_)
    print("value of address: " + addressField.value_)
    print("value of e-mail: " + emailField.value_)
    print("value of age: " + ageField.value_)
    print("value of name: " + nameField.value_)
    print("---------------------------------------------")    

# Test non systematic order (OK)
    myFieldReader = fieldReader.fieldReader(myLine)
    addressFieldValue = myFieldReader.getFieldValueAbsAndSlice("address", ["address:"], [","])
    ageFieldValue = myFieldReader.getFieldValueAbsAndSlice("age", ["age:"], [","]) 
    emailFieldValue = myFieldReader.getFieldValueAbsAndSlice("email", ["e-mail:"], [","]) 
    nameFieldValue = myFieldReader.getFieldValueAbsAndSlice("name", endIds_=[","])
    zipcodeFieldValue = myFieldReader.getFieldValueAbsAndSlice("zip", ["zip:"])

    # Read the field->values in reverse order to demonstrate the power of the condition chains
    print("------ testFieldSlicer() ----------")
    print("value of zip: " + zipcodeFieldValue)
    print("value of address: " + addressFieldValue)
    print("value of e-mail: " + emailFieldValue)
    print("value of age: " + ageFieldValue)
    print("value of name: " + nameFieldValue)
    print("---------------------------------------------")

# Test name less
    myFieldReader = fieldReader.fieldReader(myLine)
    addressFieldValue = myFieldReader.getFieldValueAbsAndSlice(startIds_=["address:"], endIds_=[","])
    ageFieldValue = myFieldReader.getFieldValueAbsAndSlice(startIds_=["age:"], endIds_=[","]) 
    emailFieldValue = myFieldReader.getFieldValueAbsAndSlice(startIds_=["e-mail:"], endIds_=[","]) 
    nameFieldValue = myFieldReader.getFieldValueAbsAndSlice(endIds_=[","])
    zipcodeFieldValue = myFieldReader.getFieldValueAbsAndSlice(startIds_=["zip:"])

    # Read the field->values in reverse order to demonstrate the power of the condition chains
    print("------ testFieldSlicer() ----------")
    print("value of zip: " + zipcodeFieldValue)
    print("value of address: " + addressFieldValue)
    print("value of e-mail: " + emailFieldValue)
    print("value of age: " + ageFieldValue)
    print("value of name: " + nameFieldValue)
    print("---------------------------------------------")    


def testFieldreader():
    myFieldReader = fieldReader.fieldReader(myLine)
    nameFieldValue = myFieldReader.getFieldValueRel("name", endIds_=[","])
    nameField = myFieldReader.getField("name")    
    ageFieldValue = myFieldReader.getFieldValueRel("age", ["age:"], [","]) 
    ageField = myFieldReader.getField("age")    
    emailFieldValue = myFieldReader.getFieldValueRel("email", ["e-mail:"], [","]) 
    emailField = myFieldReader.getField("email")    
    addressFieldValue = myFieldReader.getFieldValueRel("address", ["address:"], [","])
    addressField = myFieldReader.getField("address")    
    zipcodeFieldValue = myFieldReader.getFieldValueRel("zip", ["zip:"])
    zipcodeField = myFieldReader.getField("zip")

    # Read the field->values in any order
    print("------ testFieldReader() ----------")
    print("value of zip: " + zipcodeField.value_)
    print("value of address: " + addressField.value_)
    print("value of e-mail: " + emailField.value_)
    print("value of age: " + ageField.value_)
    print("value of name: " + nameField.value_)
    print("---------------------------------------------")

# Test non systematic order
    myFieldReader = fieldReader.fieldReader(myLine)
    emailFieldValue = myFieldReader.getFieldValueAbs("email", ["e-mail:"], [","]) # note ValueEndIx so prev field->endId is used as thisField->startId
    emailField = myFieldReader.getField("email")
    ageFieldValue = myFieldReader.getFieldValueAbs("age", ["age:"], [","]) # note ValueEndIx ix so prev field->endId is used as thisField->startId
    ageField = myFieldReader.getField("age")    
    zipcodeFieldValue = myFieldReader.getFieldValueAbs("zip", ["zip:"])
    zipcodeField = myFieldReader.getField("zip")
    addressFieldValue = myFieldReader.getFieldValueAbs("address", ["address:"], [","])
    addressField = myFieldReader.getField("address")    
    nameFieldValue = myFieldReader.getFieldValueAbs("name", endIds_=[","])
    nameField = myFieldReader.getField("name")


    # Read the field->values in any order
    print("------ testFieldReader() ----------")
    print("value of zip: " + zipcodeField.value_)
    print("value of address: " + addressField.value_)
    print("value of e-mail: " + emailField.value_)
    print("value of age: " + ageField.value_)
    print("value of name: " + nameField.value_)
    print("---------------------------------------------")        

# build string
myLine = "johnny, age: 10, e-mail: johnny@gmail.com, address: hulabula vej, zip: 8645"
testFieldreader() #OK
testFieldSlicer() #OK

