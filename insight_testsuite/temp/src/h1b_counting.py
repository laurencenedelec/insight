
def get_h1b(input, output_states, output_occupations):
    import  csv,re,os.path,pandas
    pathos=os.getcwd()
    
       
    # an investigation  of the .csv files shows that
    # the information we want is in the < CASE_NUMBER > <CASE_STATUS>  < WORKSITE_STATE>  <SOC_CODE>
    # <SOC_NAME> (same as SOC_CODE but in string) tags, and   <CASE_STATUS> to test  CERTIFIED
    #read the data with pandas 
    data=pandas.read_csv(pathos+'/'+input,delimiter=';',dtype=object,error_bad_lines=False)
    #create the column name that contain this information  and change name
    indexlist=['.*SOC_CODE*','.*SOC_NAME*','.*WORK.*STATE*','.*STATUS*','.*CASE_NUMBER*']
    column_real=[]
    for i in indexlist:
        regex=re.compile(i)
        name_real = list(filter(regex.match, data.columns))[0]
        column_real.append(name_real)
    df=data[column_real]
    df.columns=['SOC_CODE','SOC_NAME','WORKSITE_STATE','CASE_STATUS','CASE_NUMBER']
    #remove the case not certified
    df=df[df.CASE_STATUS == 'CERTIFIED']
    #
    #
    #create occupations and states 'output' with loop
    for type in [('states','WORKSITE_STATE','TOP_STATES'),('occupations','SOC_NAME','TOP_OCCUPATIONS')]:
       #create count and percentage
       stat=df.set_index(['%s' %(type[1]),'CASE_STATUS']).count(level='%s' %(type[1]))
       stat=stat[['CASE_NUMBER']]
       stat['PERCENTAGE']= 100*(stat['CASE_NUMBER']/ stat['CASE_NUMBER'].sum())
       stat.reset_index(level=0, inplace=True)
       #name columns
       stat.columns = [type[2],'NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']
       #sort two way
       stat.sort_values(by=[type[2]])
       stat=stat.sort_values(by=['PERCENTAGE'],ascending=False)
       #presentation of percentage as float  1 decimal place
       def approx(x):
          return(round(x,1))
       stat['PERCENTAGE']=stat['PERCENTAGE'].apply(approx)
       #keep only 10 first
       stat=stat[:10]
       #print output
      
       if type[0]=='states':
           stat.to_csv(pathos+'/'+output_states, sep=';', index=False)
       else:
           stat.to_csv(pathos+'/'+output_occupations , sep=';', index=False)

#add the arguments and run get_h1b
import sys
get_h1b( sys.argv[1],sys.argv[2],sys.argv[3])



