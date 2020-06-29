#Importing pandas library
import pandas as pd 

# Function to read the file data to spilt list values
def read_data(filename):

    # Read csv file into File_Data dataframe
    File_Data = pd.read_csv(filename)
    
    # Check if any row value of eventLabel column in File_Data is List
    File_Data['Is_eventLabel_List'] = File_Data.eventLabel.apply(Check_List)
    df = File_Data[File_Data.Is_eventLabel_List==True]
    
    # Creating an auto-incremented index value for key reference
    df = df.reset_index()
    df['id'] = df.index
    
    # We start with creating a new dataframe from the series with the newly created id(as key) as the index
    new_df = pd.DataFrame(df.eventLabel.str.split('},').tolist(), index=df.id).stack()
    
    # We now want to get rid of the secondary index
    # To do this, we will make EmployeeId as a column (it can't be an index since the values will be duplicate)
    new_df = new_df.reset_index([0, 'id'])
    
    # Specify new_df column names
    new_df.columns = ['id', 'eventLabel']
    
    #Passing new_df[eventLabel] column in ModifyData function
    new_df['eventLabel']=new_df.eventLabel.apply(Modify_Data)
    
    # Dropping eventLable from old df as we wil be replacing the new eventLable values
    df=df.drop(['eventLabel'], axis=1)
    
    #Join modified df with the df containing all the columns on the basis of id column
    final_df = pd.merge(df,new_df,on='id')
    
    #Creating a csv file for the result
    final_df.to_csv('test.csv')
    
    # printing dataframes column names
    print(new_df.columns)
    print(final_df.columns)
    
    # END OF read_data()

# Function to check if col variable is List or not
def Check_List(col):
    if str(col)[0]== '[' and str(col)[-1] ==']':
        return True
    else:
        return False

#Function to manipulate string col if containing '[',']' and appending '}'
def Modify_Data(col):
    if str(col)[0] == '[':
        col=str(col)[1:]
    if str(col)[-1] == ']':
        col=str(col)[:-1]
    else:
        col=str(col)+'}'
    return col
    
    #END OF Modify_Data()

# main()
if __name__ == "__main__":
    read_data("2020-06-23.csv")