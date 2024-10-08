Create Table Mental_Health (
	Employee_ID Varchar(100) Primary Key not null,
	Mental_Health_Condition Varchar(100) not null,
	Stress_Level Varchar(100) not null,
	Physical_Activity Varchar(100) not null,
	Sleep_Quality Varchar(100) not null,
	Hours_Worked_Per_Week int not null,
	Number_of_Virtual_Meetings int not null,
	Work_Life_Balance_Rating int not null,
	Access_to_Mental_Health_Resources Varchar(100) not null,
	Productivity_Change Varchar(100) not null,
	Social_Isolation_Rating int not null,
	Satisfaction_with_Remote_Work Varchar(100) not null,
	Company_Support_for_Remote_Work int not null
);

Create table employee (
	Employee_ID Varchar(100) Primary Key not null,
	Age int not null,
	Gender Varchar(100) not null,
	Job_Role Varchar(100) not null,
	Industry Varchar(100) not null,
	Years_of_Experience int not null,
	Work_Location Varchar(100) not null,
	Region Varchar(100) not null
);

Create Table age_group (
	Employee_ID Varchar(100) Primary Key not null,
	agegroup Varchar(100) not null
);

Select * From Mental_Health
SELECT * FROM employee	
Select * From age_group




