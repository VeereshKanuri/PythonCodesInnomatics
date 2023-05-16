#!/usr/bin/env python
# coding: utf-8

# In[47]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


df = pd.read_excel('asp2015.xlsx')


# In[4]:


df.info()


# In[5]:


df.columns


# In[6]:


df.head()


# In[7]:


df.shape


# # There is a unnamed column and we cannot use for data analysis

# In[8]:


#drop that column
df=df.drop(['Unnamed: 0','ID'],axis=1)


# In[9]:


df.shape


# In[10]:


df.info()


# In[11]:


#checking for anolities in data
for i in df.columns:
    print('*'*10,i,'*'*10)
    print(df[i].unique())


# ### Observations of the columns(regarding cleaning and missing values):
# * 1.We can see the DOJ,DOL,DOB are given in timestamp format
# * 2.Job city column contains -1 values which are NaN equivalents.
# * 3.10 board column contain 0 value which is missing value
# * 4.12 board column contain 0 value which is missing value
# * 5.college state column contain 'union teritory' which is not a specific state
# * 6.Graduation year column contain 0 which is a missing value
# * 7.Domain column contain -1 which is a missing value
# 

# ##### We can see the DOJ and DOL are given in timestamp format. As per our objective,we only need date,we will convert timestamp into date using datetime module.
# 
# #### In DOL column,We can see the value '***present***' . We will convert this into the present date for our analysis

# In[12]:


#lets first conver DOJ column from timedate to date
import datetime as dt
df['DOJ']=pd.to_datetime(df['DOJ']).dt.date


# In[13]:


df['DOJ']


# In[14]:


df["DOL"].replace("present",dt.datetime.today(),inplace=True)
df['DOL']=pd.to_datetime(df["DOL"]).dt.date
df["work_period"]=pd.to_datetime(df['DOL']).dt.year - pd.to_datetime(df['DOJ']).dt.year


# In[15]:


##We only need DOB year,so we will convert DOB column from timestamp to year
df['DOB'] = pd.to_datetime(df['DOB']).dt.year
df.head()


# In[16]:


##We also know graduation year contains 0 value,we need to impute it with mode before engineering new feature from this.
df['GraduationYear'].replace(0,df['GraduationYear'].mode()[0],inplace=True)


# # We do not need 12th graduation and 10th graduation timestamps,we only need the age of people during graduation to know whether they have any drop years.
# #### So we drop those columns and engineer new columns
# * 12Gradage - It indicates the age of person during 12th graduation
# * Gradage - It indicates the age of person during their higher education graduation(Degree/Engineering etc)
# 
# 
# 

# In[17]:


df['12GradAge']=abs(df['12graduation']-df['DOB'])
df['GradAge']=abs(df['GraduationYear']-df['DOB'])


# In[18]:


### Here we could have compared modes of all the columns and then could have selected the mode out of the resulting modes
### But from intuition,i thought mostly people from particular specialization choose desired designations.
df[df["Designation"]=="get"][['Designation','JobCity','Salary','Specialization']]


# # From here,we can see that most of people whose designation is unknown are from mechanical domain(70%) and ECE(30%).
# ### So we can pick the mode of designation for people belonging to mechanical domain and impute it with get value.
# ### similarly for electrical domain

# In[19]:


#lets replace get in  (mechanical engineering) and (mechanical and automation) specializations
mech= df[df["Specialization"].isin(['mechanical engineering','mechanical and automation'])]['Designation'].mode()[0]


# In[22]:


eee = df[df['Specialization']==('electronics and electrical engineering')]['Designation'].mode()[0]
print(f'mode for mechanical:  {mech}\nmode for EEE:  {eee}')


# In[25]:


#For mechanical domain
df.loc[df['Specialization'].isin(['mechanical engineering','mechanical and automation']),'Designation'].replace('get',mech,inplace=True)
#for EEE domain,as all previous get's will be replaced,we can replace the remaining directly without conditions
df['Designation'].replace('get',eee,inplace=True)


# ## Column : 'Jobcity'
# ### Jobcity contains missing values(-1).We will treat this by using mode.We will compute the mode of all columns with rows having jobcity as -1.Then we make a list of these modes and compute the overall mode of the resulting list. 
# ### In this way,we could consider all columns for substituting the missing value.

# In[27]:


### we do not want our data to be case sensitive in jobcity
### ,because it will effect our analysis.so let us replace -1 with some string and then apply title method to it.
df['JobCity'].replace(-1,'unknown',inplace=True)
df['JobCity'].apply(lambda x:x.title())


# In[28]:


df[df["JobCity"]=='unknown']


# In[30]:


df[df["JobCity"]=="unknown"][["Designation","12GradAge","GradAge","JobCity","Gender","10percentage","10board","12percentage","12board","Degree","Specialization","CollegeState","Specialization"]].mode()


# In[32]:


### cleaning the column which have similar meaning but has spelling difference orelse it will effect the distribution.
df["JobCity"].replace("Bangalore","Bengaluru",inplace=True)
df["JobCity"].replace("Banaglore","Bengaluru",inplace=True)
df["JobCity"].replace("Chennai, Bangalore","Bengaluru",inplace=True)
df["JobCity"].replace(" Bangalore","Bengaluru",inplace=True)
df["JobCity"].replace("Bangalore ","Bengaluru",inplace=True)
df["JobCity"].replace("Banglore","Bengaluru",inplace=True)
df["JobCity"].replace("Jaipur ","Jaipur",inplace=True)
df["JobCity"].replace("Gandhinagar","Gandhi Nagar",inplace=True)
df["JobCity"].replace("Bangalore ","Bengaluru",inplace=True)
df["JobCity"].replace("Jaipur ","Jaipur",inplace=True)
df["JobCity"].replace("Gandhinagar","Gandhi Nagar",inplace=True)
df["JobCity"].replace("Hyderabad ","Hyderabad",inplace=True)
df["JobCity"].replace("Hyderabad(Bhadurpally)","Hyderabad",inplace=True)
df["JobCity"].replace("Bhubaneswar ","Bhubaneswar",inplace=True)
df["JobCity"].replace("Delhi/Ncr","Delhi",inplace=True)
df["JobCity"].replace("Nagpur ","Nagpur",inplace=True)
df["JobCity"].replace("Pune ","Pune",inplace=True)
df["JobCity"].replace("Trivandrum ","Trivandrum",inplace=True)
df["JobCity"].replace("Thiruvananthapuram","Trivandrum",inplace=True)


# In[33]:


### First,we saw the frequent(mode) values in other columns when we have a missing value in our target column('Jobcity')
### Now,we will find list of modes of other columns when they have the above found frequent value in their respective column.
### In this way,we are able to include the presence of all columns in predicting our best shot for the missing value.

best_mode = []
best_mode.append(df[df["Designation"]=="software engineer"]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["Gender"]=="m"]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["10percentage"]==76]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["10board"]=="cbse"]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["12percentage"]==64]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["12board"]=="cbse"]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["collegeGPA"]==70]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["Salary"]==200000]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["Degree"].str.startswith("B.Tech/")]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["Specialization"].str.startswith("electronics and communication eng")]["JobCity"].mode().to_list()[0])
best_mode.append(df[df["CollegeState"].str.startswith("Uttar Pradesh")]["JobCity"].mode().to_list()[0])
best_mode


# In[35]:


### We can see mode from the best_mode list is 'Bangalore'
df["JobCity"].replace("unknown",'Bengaluru',inplace=True)


# # 10-board

# In[36]:


df[df["10board"]==0][["Designation","12GradAge","GradAge","JobCity","Gender","10percentage","10board","12percentage","12board","Degree","Specialization","CollegeState","Specialization"]].mode()


# In[37]:


### Same process as above written for jobcity
best_value2=[]
best_value2.append(df[df["Designation"]=="software engineer"]["10board"].mode().to_list()[0])
best_value2.append(df[df["Gender"]=="m"]["10board"].mode().to_list()[0])
best_value2.append(df[df["10percentage"]==75]["10board"].mode().to_list()[0])
best_value2.append(df[df["JobCity"]=="Bengaluru"]["10board"].mode().to_list()[0])
best_value2.append(df[df["12percentage"]==65]["10board"].mode().to_list()[0])
best_value2.append(df[df["collegeGPA"]==65]["10board"].mode().to_list()[0])
best_value2.append(df[df["Salary"]==400000]["10board"].mode().to_list()[0])
best_value2.append(df[df["Degree"].str.startswith("B.Tech/")]["10board"].mode().to_list()[0])
best_value2.append(df[df["Specialization"].str.startswith("computer eng")]["10board"].mode().to_list()[0])
best_value2.append(df[df["CollegeState"].str.startswith("Tamil Nadu")]["10board"].mode().to_list()[0])
best_value2


# In[39]:


### Replacing with the mode of the best_value list(visually as it is a small list orelse could have written code for it.)
df['10board'].replace(0,'cbse',inplace=True)


# # 12th BOARD

# In[48]:


### From what i found from above,we can be sure that 12 board missing value can be replaced with 'cbse' 
### as most of the people do 12th also from the same board.(general observation,can also be proved)
df['12board'].replace(0,'cbse',inplace=True)


# In[49]:


sns.boxplot(df['Domain'])
plt.show()


# In[51]:


### replacing the redundant values of the 12board column with 'state','cbse','icse'.
#replacing the redundant values of the 12board column with 'state','cbse','icse' and 'n/a'
replace_list_state=['board of intermediate education,ap', 'state board',
       'mp board',  'karnataka pre university board', 'up',
       'p u board, karnataka', 'dept of pre-university education', 'bie',
       'kerala state hse board', 'up board', 'bseb', 'chse', 'puc',
       ' upboard',
       'state  board of intermediate education, andhra pradesh',
       'karnataka state board',
       'west bengal state council of technical education', 'wbchse',
       'maharashtra state board', 'ssc',
       'sda matric higher secondary school', 'uttar pradesh board', 'ibe',
       'chsc', 'board of intermediate', 'upboard', 'sbtet',
       'hisher seconadry examination(state board)', 'pre university',
       'borad of intermediate', 'j & k board',
       'intermediate board of andhra pardesh', 'rbse',
       'central board of secondary education', 'jkbose', 'hbse',
       'board of intermediate education', 'state', 'ms board', 'pue',
       'intermediate state board', 'stateboard', 'hsc',
       'electonincs and communication(dote)', 'karnataka pu board',
       'government polytechnic mumbai , mumbai board', 'pu board',
       'baord of intermediate education', 'apbie', 'andhra board',
       'tamilnadu stateboard',
       'west bengal council of higher secondary education',
       'cbse,new delhi', 'u p board', 'intermediate', 'biec,patna',
       'diploma in engg (e &tc) tilak maharashtra vidayapeeth',
       'hsc pune', 'pu board karnataka', 'kerala', 'gsheb',
       'up(allahabad)', 'nagpur', 'st joseph hr sec school',
       'pre university board', 'ipe', 'maharashtra', 'kea', 'apsb',
       'himachal pradesh board of school education', 'staae board',
       'international baccalaureate (ib) diploma', 'nios',
       'karnataka board of university',
       'board of secondary education rajasthan', 'uttarakhand board',
       'ua', 'scte vt orissa', 'matriculation',
       'department of pre-university education', 'wbscte',
       'preuniversity board(karnataka)', 'jharkhand accademic council',
       'bieap', 'msbte (diploma in computer technology)',
       'jharkhand acamedic council (ranchi)',
       'department of pre-university eduction', 'biec',
       'sjrcw', ' board of intermediate', 'msbte',
       'sri sankara vidyalaya', 'chse, odisha', 'bihar board',
       'maharashtra state(latur board)', 'rajasthan board', 'mpboard',
       'state board of technical eduction panchkula', 'upbhsie', 'apbsc',
       'state board of technical education and training',
       'secondary board of rajasthan',
       'tamilnadu higher secondary education board',
       'jharkhand academic council',
       'board of intermediate education,hyderabad', 'up baord', 'pu',
       'dte', 'board of secondary education', 'pre-university',
       'board of intermediate education,andhra pradesh',
       'up board , allahabad', 'srv girls higher sec school,rasipuram',
       'intermediate board of education,andhra pradesh',
       'intermediate board examination',
       'department of pre-university education, bangalore',
       'stmiras college for girls', 'mbose',
       'department of pre-university education(government of karnataka)',
       'dpue', 'msbte pune', 'board of school education harayana',
       'sbte, jharkhand', 'bihar intermediate education council, patna',
       'higher secondary', 's j polytechnic', 'latur',
       'board of secondary education, rajasthan', 'jyoti nivas', 'pseb',
       'biec-patna', 'board of intermediate education,andra pradesh',
       'chse,orissa', 'pre-university board', 'mp', 'intermediate board',
       'govt of karnataka department of pre-university education',
       'karnataka education board',
       'board of secondary school of education', 'pu board ,karnataka',
       'karnataka secondary education board', 'karnataka sslc',
       'board of intermediate ap', 'u p', 'state board of karnataka',
       'directorate of technical education,banglore', 'matric board',
       'andhpradesh board of intermediate education',
       'stjoseph of cluny matrhrsecschool,neyveli,cuddalore district',
       'bte up', 'scte and vt ,orissa', 'hbsc',
       'jawahar higher secondary school', 'nagpur board', 'bsemp',
       'board of intermediate education, andhra pradesh',
       'board of higher secondary orissa',
       'board of secondary education,rajasthan(rbse)',
       'board of intermediate education:ap,hyderabad', 'science college',
       'karnatak pu board', 'aissce', 'pre university board of karnataka',
       'bihar', 'kerala state board', 'uo board', 
       'karnataka board', 'tn state board',
       'kolhapur divisional board, maharashtra',
       'jaycee matriculation school',
       'board of higher secondary examination, kerala',
       'uttaranchal state board', 'intermidiate', 'bciec,patna', 'bice',
       'karnataka state', 'state broad', 'wbbhse', 'gseb',
       'uttar pradesh', 'ghseb', 'board of school education uttarakhand',
       'gseb/technical education board', 'msbshse,pune',
       'tamilnadu state board', 'board of technical education',
       'kerala university', 'uttaranchal shiksha avam pariksha parishad',
       'chse(concil of higher secondary education)',
       'bright way college, (up board)', 'board of intermidiate',
       'higher secondary state certificate', 'karanataka secondary board',
       'maharashtra board', 'cgbse', 'diploma in computers', 'bte,delhi',
       'rajasthan board ajmer', 'mpbse', 'pune board',
       'state board of technical education', 'gshseb',
       'amravati divisional board', 'dote (diploma - computer engg)',
       'karnataka pre-university board', 'jharkhand board',
       'punjab state board of technical education & industrial training',
       'department of technical education',
       'sri chaitanya junior kalasala', 'state board (jac, ranchi)',
       'aligarh muslim university', 'tamil nadu state board', 'hse',
       'karnataka secondary education', 'state board ',
       'karnataka pre unversity board',
       'ks rangasamy institute of technology',
       'karnataka board secondary education', 'narayana junior college',
       'bteup', 'board of intermediate(bie)', 'hsc maharashtra board',
       'tamil nadu state', 'uttrakhand board', 'psbte',
       'stateboard/tamil nadu', 'intermediate council patna',
       'technical board, punchkula', 'board of intermidiate examination',
       'sri kannika parameswari highier secondary school, udumalpet',
       'ap board', 'nashik board', 'himachal pradesh board',
       'maharashtra satate board',
       'andhra pradesh board of secondary education',
       'tamil nadu polytechnic',
       'maharashtra state board mumbai divisional board',
       'department of pre university education',
       'dav public school,hehal', 'board of intermediate education, ap',
       'rajasthan board of secondary education',
       'department of technical education, bangalore', 'chse,odisha',
       'maharashtra nasik board',
       'west bengal council of higher secondary examination (wbchse)',
       'holy cross matriculation hr sec school', 'cbsc',
       'pu  board karnataka', 'biec patna', 'kolhapur', 'bseb, patna',
       'up board allahabad', 'nagpur board,nagpur', 'diploma(msbte)',
       'dav public school', 'pre university board, karnataka',
       'ssm srsecschool', 'state bord', 'jstb,jharkhand',
       'intermediate board of education', 'mp board bhopal', 'pub',
       'madhya pradesh board', 'bihar intermediate education council',
       'west bengal council of higher secondary eucation',
        'mpc',
       'certificate for higher secondary education (chse)orissa',
       'maharashtra state board for hsc',
       'board of intermeadiate education', 'latur board',
       'andhra pradesh', 'karnataka pre-university',
       'lucknow public college', 'nagpur divisional board',
       'ap intermediate board', 'cgbse raipur', 'uttranchal board',
       'jiec', 
       'bihar school examination board patna',
       'state board of technical education harayana', 'mp-bse',
       'up bourd', 'dav public school sec 14',
       'haryana state board of technical education chandigarh',
       'council for indian school certificate examination',
       'jaswant modern school', 'madhya pradesh open school',
       'aurangabad board', 'j&k state board of school education',
       'diploma ( maharashtra state board of technical education)',
       'board of technicaleducation ,delhi',
       'maharashtra state boar of secondary and higher secondary education',
       'hslc (tamil nadu state board)',
       'karnataka state examination board', 'puboard', 'nasik',
       'west bengal board of higher secondary education',
       'up board,allahabad', 'board of intrmediate education,ap', 
       'karnataka state pre- university board',
       'state board - west bengal council of higher secondary education : wbchse',
       'maharashtra state board of secondary & higher secondary education',
       'biec, patna', 'state syllabus', 'cbse board', 'scte&vt',
       'board of intermediate,ap',
       'secnior secondary education board of rajasthan',
       'maharashtra board, pune', 'rbse (state board)',
       'board of intermidiate education,ap',
       'board of high school and intermediate education uttarpradesh',
       'higher secondary education',
       'board fo intermediate education, ap', 'intermedite',
       'ap board for intermediate education', 'ahsec',
       'punjab state board of technical education & industrial training, chandigarh',
       'state board - tamilnadu', 'jharkhand acedemic council',
       'scte & vt (diploma)', 'karnataka pu',
       'board of intmediate education ap', 'up-board',
       'boardofintermediate','intermideate','up bord','andhra pradesh state board','gujarat board']


# In[53]:


#replacing the redundant values of the 12board column with 'state','cbse','icse' 
for i in replace_list_state:
    df['12board'].replace(i,'state',inplace=True)

replace_list_cbse=['cbse', 
       'all india board', 
       'central board of secondary education, new delhi', 'cbese']
for i in replace_list_cbse:
    df['12board'].replace(i,'cbse',inplace=True)

replace_list_icse=[ 'isc', 'icse', 'isc board', 'isce', 'cicse',
       'isc board , new delhi']
for i in replace_list_icse:
    df['12board'].replace(i,'icse',inplace=True)
    df['12board'].unique()


# In[54]:


specialization_map = {'electronics and communication engineering' : 'EC',
 'computer science & engineering' : 'CS',
 'information technology' : 'CS' ,
 'computer engineering' : 'CS',
 'computer application' : 'CS',
 'mechanical engineering' : 'ME',
 'electronics and electrical engineering' : 'EC',
 'electronics & telecommunications' : 'EC',
 'electrical engineering' : 'EL',
 'electronics & instrumentation eng' : 'EC',
 'civil engineering' : 'CE',
 'electronics and instrumentation engineering' : 'EC',
 'information science engineering' : 'CS',
 'instrumentation and control engineering' : 'EC',
 'electronics engineering' : 'EC',
 'biotechnology' : 'other',
 'other' : 'other',
 'industrial & production engineering' : 'other',
 'chemical engineering' : 'other',
 'applied electronics and instrumentation' : 'EC',
 'computer science and technology' : 'CS',
 'telecommunication engineering' : 'EC',
 'mechanical and automation' : 'ME',
 'automobile/automotive engineering' : 'ME',
 'instrumentation engineering' : 'EC',
 'mechatronics' : 'ME',
 'electronics and computer engineering' : 'CS',
 'aeronautical engineering' : 'ME',
 'computer science' : 'CS',
 'metallurgical engineering' : 'other',
 'biomedical engineering' : 'other',
 'industrial engineering' : 'other',
 'information & communication technology' : 'EC',
 'electrical and power engineering' : 'EL',
 'industrial & management engineering' : 'other',
 'computer networking' : 'CS',
 'embedded systems technology' : 'EC',
 'power systems and automation' : 'EL',
 'computer and communication engineering' : 'CS',
 'information science' : 'CS',
 'internal combustion engine' : 'ME',
 'ceramic engineering' : 'other',
 'mechanical & production engineering' : 'ME',
 'control and instrumentation engineering' : 'EC',
 'polymer technology' : 'other',
 'electronics' : 'EC'}


# In[56]:


df['Specialization'] = df['Specialization'].map(specialization_map)
df['Specialization'].unique()


# # univariate and bivariate analysis

# In[57]:


df.drop(columns=['CollegeID','CollegeCityID','CollegeCityTier'],axis=1,inplace=True)


# In[58]:


df.columns


# In[60]:


### Salary less than 50000 people might have entered their montly income rather than yearly
df.loc[df['Salary']<=50000,'Salary']*=12
lst = ['ComputerProgramming','ElectronicsAndSemicon','ComputerScience','MechanicalEngg','ElectricalEngg','TelecomEngg','CivilEngg']
for i in lst:
    df[i].replace(-1,0,inplace=True)


# In[62]:


plt.figure(figsize=(15,5))
colors = sns.color_palette('bright',n_colors=2)
sns.FacetGrid(df, col="Gender", size=5,palette=colors)    .map(sns.distplot, "Salary",bins=50)    .add_legend()
plt.show()
print


# # * We can observe that the salary data is right skewed.
# * We can also see that the distributions are quite similar for male and female in the range below 10lakhs.

# In[63]:


sns.countplot(df['Gender'])
print(df['Gender'].value_counts())


# In[64]:


plt.figure(figsize=(10,5))
sns.boxplot(x='Salary',y='Gender',data=df)


# # * It is noted that there are many outliers in the salary data
# * There is not much difference between median salary for both genders.
# * We can also observe male have more outliers indicating they are more people getting higher pays in male than female category

# In[65]:


plt.figure(figsize=(15,5))
sns.boxplot(x='Salary',y='Specialization',data=df)
plt.suptitle('Salary levels by specialization')


# # * Median salary of people from all specializations are nearly similar.
# * We can see there are more people getting higher pays who have specialization in CS/EC compared to others.

# In[66]:


### Designation
popular_Designation = df['Designation'].value_counts()[:20].index.tolist()
print(popular_Designation)


# In[67]:


### We want on
top_Designations = df[df['Designation'].isin(popular_Designation)]
print(f"Unique professions : {len(df['Designation'].unique())}")
top_Designations.head()


# In[68]:


plt.figure(figsize=(20,10))
sns.countplot(x='Designation',hue='Gender',data=top_Designations)
plt.xticks(fontsize=30,rotation=90)
plt.yticks(fontsize=30)
plt.show()


# * All the general professions are more dominated by the males as we can there is considerable difference of frequency for every role.
# * Here we took the most common roles taken by the amcat aspirants which are mostly 'IT Roles'.
# * from the below plot,we can understand the reason for most 'IT roles' might be because of Specialization

# In[69]:


sns.countplot(df['Specialization'])


# In[70]:


sns.countplot(df['Degree'])


# In[71]:


plt.figure(figsize=(20,10))
sns.barplot(x='Designation',y='Salary',hue='Gender',data=top_Designations)
plt.xticks(fontsize=30,rotation=90)
plt.yticks(fontsize=30)
plt.show()


# * mean salary of top most frequent roles is nearly independent of gender.
# * there is some considerable difference in some roles.but we cannot be sure that women is being paid less in that role
# * it might be due to experience,specialization etc

# In[74]:


high = list(df.sort_values("Salary",ascending=False)["Designation"].unique())[:20]
high_pay = df[df['Designation'].isin(high)]
high_pay.head()


# In[75]:


plt.figure(figsize=(20,10))
sns.barplot(x='Designation',y='Salary',hue='Gender',data=high_pay)
plt.xticks(fontsize=30,rotation=90)
plt.yticks(fontsize=30)
plt.show()


#  Most of the high paying jobs are from IT domain.
# * In 45% of top paying roles,men are generally paid higher compared to women.
# * In 20% of top paying roles,women are paid higher than men
# * In roles like junior manager,sales account manager,software engineer trainee there are no women working in these fields.
# * Junior manager is highest paying for men and field engineer is the highest paying role for women.
# * The disperancy between pay based on gender might be because of other features like experience,specialization etc.
# * Software Enginner and Software developer are most frequent and highest paying jobs

# In[77]:


plt.figure(figsize=(20,20))
sns.heatmap(df.corr(),annot=True)


# In[85]:





# In[84]:





# In[ ]:





# In[ ]:




