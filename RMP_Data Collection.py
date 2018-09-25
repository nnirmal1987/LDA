import json
import urllib2 as url
import random
import MySQLdb
import time
from math import ceil

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
#Unique School ID. Needs to be manually Evaluated
school_id=[1415]
           #1420,1426,1432,1433,1440,1447,1452,1466,1469,1471,1484,1485,1490,1491,1492,1495,1498,4714,4919,4928,12184]
school_name=['Brock University']
             #,'Carleton University','University of Guelph','Lakehead University','Laurentian University','McMaster University','Nipissing University','University of Ottawa','Queens University','Royal Military College','Ryerson University',
             #'University of Toronto StGeorge','Trent University','University of Waterloo','Western University','Wilfrid Laurier University','York University','Algoma University','University of Ontario Institute of Technology','University of Toronto Scarborough','University of Toronto Missisauga','University of Toronto']
failures

#Scraping Contents
def scrape2mysql(host,uname,pwd,schoolid,schoolname,dept):
    #department='Economics'    
    dept=dept.replace(' ','+')
    dept=dept.replace('&','%26')
    link_to_profs = "http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=200&callback=noCB&q=*%3A*+AND+schoolid_s%3A{}+AND+teacherdepartment_s%3A{}&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t".format(schoolid,dept)
    #print(link_to_profs)
    con=MySQLdb.connect(host=host,user=uname,passwd=pwd)
    cur=con.cursor()
    try:
        cur.execute("use rmp_ontario")
        #cur.execute("SET NAMES utf8")
    except:
        print("rmp_ontario_new database does not exist. Do you want us to create it and initialize tables? [y/n]")
        response = raw_input()
        if "y" in response.lower():
            print("Creating rmp_ontario DB")
        elif "n" in response.lower():
            print("Halting program. Goodbye!")
            exit()
        else:
            print("Did not understand input. Aborting!")
            exit() 
        cur.execute("CREATE DATABASE IF NOT EXISTS rmp_ontario")
        cur.execute("use rmp_ontario")
        cur.execute("CREATE TABLE professor (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,pk_id INT NOT NULL PRIMARY KEY, fname varchar(20) NOT NULL, lname varchar(20) NOT NULL, school text NOT NULL,department varchar(50) NOT NULL,KEY(pk_id))")
        cur.execute("CREATE TABLE reviews (reviewID int NOT NULL AUTO_INCREMENT, profID int NOT NULL, review TEXT, PRIMARY KEY (reviewID), FOREIGN KEY (profID) REFERENCES professor(pk_id),reviewDate date NOT NULL,subjectCode varchar(15) NOT NULL,ratngIntrst varchar(50) NOT NULL,profQlty varchar(25) NOT NULL,overalRtng float NOT NULL,rEasy float NOT NULL)")
        print("Finished creating and initializing DB")       
    
    prof_req = url.Request(link_to_profs,headers=headers)
    profs=url.urlopen(prof_req).read()
    profs = profs.replace("noCB(", "").replace(");", "")
    json_profs = json.loads(profs)["response"]["docs"]
    random.shuffle(json_profs)
    for prof in json_profs:
        print("Loading results for {} {}, with id: {}".format(prof["teacherfirstname_t"].encode('utf-8'), prof["teacherlastname_t"].encode('utf-8'), prof["pk_id"]))
        cur.execute("insert into professor (pk_id, fname, lname, school, department) values ({},\"{}\",\"{}\", \"{}\",\"{}\")".format(prof["pk_id"],prof["teacherfirstname_t"], prof["teacherlastname_t"],schoolname,dept))
        con.commit()
        #curr_id = cur.fetchone()[0]
        prof_comments = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid={}&page=1".format(prof["pk_id"])
        i = 1
        while True:
            if i > 10:
                print("Tried 10. Giving up on {} {}!".format(prof_comments["teacherfirstname_t"].encode('utf-8'), prof_comments["teacherlastname_t"]))
                failures.append((prof_comments["teacherfirstname_t"], prof_comments["teacherlastname_t"]))
                break
            try:
                site = url.Request(prof_comments,headers=headers)
                comments=url.urlopen(site).read()
                break
            except url.HTTPError, e:
                print('HTTPError = ' + str(e.code))
                time.sleep(i)
            i = i + 1
        if i > 10:
            continue
            
        total_pages = int(ceil((json.loads(comments)["remaining"] + 20)/20))
        try:
            for i in range(1, total_pages + 2):
                time.sleep(4)
                prof_comments = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid={}&page={}".format(prof["pk_id"], i)
                try:
                    site=url.Request(prof_comments,headers=headers)
                    comments = url.urlopen(site).read()
                except url.HTTPError, e:
                    print('HTTPError in comment collection = ' + str(e.code))
                    break 
                for comment in json.loads(comments)["ratings"]:
                    cur.execute("insert into reviews (profID, review, reviewDate, subjectCode, ratngIntrst, profQlty, overalRtng, rEasy) VALUES ({}, \"{}\",STR_TO_DATE(\"{}\",\"%m/%d/%Y\"),\"{}\",\"{}\",\"{}\",{},{})".format(prof["pk_id"], MySQLdb.escape_string(comment["rComments"]),comment["rDate"],MySQLdb.escape_string(comment["rClass"]),MySQLdb.escape_string(comment["rInterest"]),MySQLdb.escape_string(comment["quality"]),comment["rOverall"],comment["rEasy"]))   
                    con.commit()                                                                                                               
        except:
            pass
        
    con.close()
                                                                                                                                    
for schoolid,schoolname in zip(school_id,school_name):
    dept = url.Request('http://www.ratemyprofessors.com/teacher/getDepartmentListFromSchool?sid={}'.format(schoolid),headers=headers)
    dept_page = url.urlopen(dept).read()
    dept_json=json.loads(dept_page)['departments']
    for value in dept_json:
        dept=value['name']
        print(dept)
        scrape2mysql('localhost','root','root123',schoolid,schoolname,dept)

