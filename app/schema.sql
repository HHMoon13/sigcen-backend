CREATE TABLE IF NOT EXISTS admin_table ( 
                    adminId VARCHAR(250) NOT NULL,
                   adminEmail VARCHAR(250), 
                   adminName VARCHAR(250),
                   adminPassword VARCHAR(250), 
                    adminPhone VARCHAR(250),  
                   userDetails BLOB, 
                   PRIMARY KEY (adminId)); 
                   
CREATE TABLE IF NOT EXISTS teacher_table ( 
                    teacherId VARCHAR(250) NOT NULL,
                   teacherEmail VARCHAR(250),
                   teacherName VARCHAR(250), 
                   teacherPassword VARCHAR(250), 
                    teacherPhone VARCHAR(250),  
                   userDetails BLOB, 
                   PRIMARY KEY (teacherId)); 

CREATE TABLE IF NOT EXISTS student_table ( 
                    studentId VARCHAR(250) NOT NULL,
                   studentEmail VARCHAR(250), 
                   studentName VARCHAR(250),
                   studentPassword VARCHAR(250), 
                    studentPhone VARCHAR(250),  
                   userDetails BLOB, 
                   PRIMARY KEY (studentId));

CREATE TABLE IF NOT EXISTS course_table ( 
                   courseId VARCHAR(250) NOT NULL, 
                   courseName VARCHAR(250), 
                   madeBy VARCHAR(250),
                   courseDetails BLOB, 
                   PRIMARY KEY (courseId));  

CREATE TABLE IF NOT EXISTS syndicate_table ( 
                   syndicateId VARCHAR(250) NOT NULL, 
                   syndicateName VARCHAR(250), 
                   exerciseId VARCHAR(250),
                   PRIMARY KEY (syndicateId));

CREATE TABLE IF NOT EXISTS syndicate_members ( 
                   syndicateId VARCHAR(250) NOT NULL, 
                   studentId VARCHAR(250) NOT NULL, 
                   studentRole VARCHAR(250) NOT NULL); 

CREATE TABLE IF NOT EXISTS syndicate_exercise_table ( 
                   syndicateId VARCHAR(250) NOT NULL, 
                   exerciseId VARCHAR(250) NOT NULL);

CREATE TABLE IF NOT EXISTS exercise_table ( 
                   exerciseId VARCHAR(250) NOT NULL, 
                   exerciseName VARCHAR(250),
                   courseId VARCHAR(250), 
                    exerciseDetails VARCHAR(250),
                   PRIMARY KEY (exerciseId)); 

CREATE TABLE IF NOT EXISTS course_exercise_table ( 
                   exerciseId VARCHAR(250) NOT NULL, 
                   courseId VARCHAR(250), 
                   PRIMARY KEY (exerciseId, courseId)); 

CREATE TABLE IF NOT EXISTS takes_table ( 
                   studentId VARCHAR(250) NOT NULL, 
                   courseId VARCHAR(250)); 

CREATE TABLE IF NOT EXISTS despatch_table ( 
                   despatchId VARCHAR(250) NOT NULL, 
                   despatchStatus VARCHAR(250),
                   despatchSecurityClassification VARCHAR(250),
                   despatchPrecedence VARCHAR(250),
                   despatchFrom VARCHAR(250),
                   despatchTo VARCHAR(250),
                   despatchLetterNumber VARCHAR(250),
                   despatchOriginatorNumber VARCHAR(250),
                   despatchDate VARCHAR(250),
                   PRIMARY KEY (despatchId)); 

CREATE TABLE IF NOT EXISTS despatch_association_table ( 
                   despatchId VARCHAR(250) NOT NULL, 
                   associationId VARCHAR(250), 
                   syndicateId VARCHAR(250)); 

CREATE TABLE IF NOT EXISTS message_table ( 
                   messageId VARCHAR(250) NOT NULL, 
                   messagePrecedence VARCHAR(250),
                   messageAction VARCHAR(250),
                   messageDateTime VARCHAR(250),
                   messageInstructions VARCHAR(250),
                   messageSpecialInstructions VARCHAR(250),
                   messagePrefix VARCHAR(250),
                   messageOriginatorsNumber VARCHAR(250),
                   messageText VARCHAR(250),
                   messageClassification VARCHAR(250),
                   messageInfo VARCHAR(250),
                   messageFrom VARCHAR(250),
                   messageTo VARCHAR(250),
                   messageSignRank VARCHAR(250),
                   messageStatus VARCHAR(250),
                   PRIMARY KEY (messageId)); 

CREATE TABLE IF NOT EXISTS message_association_table ( 
                   messageId VARCHAR(250), 
                   associationId VARCHAR(250),
                   syndicateId VARCHAR(250)
);  

CREATE TABLE IF NOT EXISTS transit_slip_table ( 
                   transitSlipId VARCHAR(250) NOT NULL, 
                   transitSlipFrom VARCHAR(250), 
                   transitSlipTo VARCHAR(250),
                   transitSlipNumber VARCHAR(250),
                   transitSlipRoute VARCHAR(250),
                   transitSlipCourier VARCHAR(250),
                   transitSlipStatus VARCHAR(250),
                   PRIMARY KEY (transitSlipId)); 

CREATE TABLE IF NOT EXISTS transit_slip_association_table ( 
                   transitSlipId VARCHAR(250), 
                   despatchId VARCHAR(250),
                   syndicateId VARCHAR(250));               

CREATE TABLE IF NOT EXISTS assignment_table ( 
                   assignmentId VARCHAR(250) NOT NULL, 
                   despatchId VARCHAR(250), 
                   messageId VARCHAR(250), 
                   syndicateId VARCHAR(250), 
                   PRIMARY KEY (assignmentId)); 

CREATE TABLE IF NOT EXISTS message_register_table ( 
                   registerId VARCHAR(250) NOT NULL, 
                   messageList BLOB, 
                   PRIMARY KEY (registerId)); 

CREATE TABLE IF NOT EXISTS question_table ( 
                   questionId VARCHAR(250) NOT NULL, 
                   questionTitle VARCHAR(250),
                   questionGeneralIdea VARCHAR(250),
                   questionSpecialIdea VARCHAR(250),
                   questionNarrative1 VARCHAR(250),
                   questionRequirement1 VARCHAR(250),
                   questionNarrative2 VARCHAR(250),
                   questionRequirement2 VARCHAR(250),
                   PRIMARY KEY (questionId)); 

CREATE TABLE IF NOT EXISTS question_association_table ( 
                   questionId VARCHAR(250), 
                   exerciseId VARCHAR(250), 
                   teacherId VARCHAR(250)); 
