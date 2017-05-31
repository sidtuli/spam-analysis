from bs4 import BeautifulSoup
import csv
import re
import codecs



def read_spam_html(csv_dict_writer,spam_page_url):
    file = codecs.open(spam_page_url,encoding="utf-8")
    soup = BeautifulSoup(file.read(),"html.parser")
    comment_list = soup.find_all("tr")
    word_dict = {}
    for comment in comment_list:
        result_dict = {}
        # All these filters are for a certain numbered id, which all comments have
        comment_id = comment.get("id")
        if(comment_id is not None):
            comment_number = re.search(r'\d+', comment_id)
            if(comment_number is not None):

                # Getting comment number
                comment_number = int(comment_number.group()) - 1
                
                result_dict["Comment Number"] = comment_number

                # Finding author
                td_list = comment.find_all("td")
                
                author = td_list[0].strong
                if(author.img is not None):
                    author.img.decompose()
                result_dict["Author"] = str(author.find_all(text=True)[0])

                # Finding author's website, email, and IP address

                result_dict["Website"] = ""
                result_dict["Email"] = ""
                result_dict["IP Address"] = ""
                author_a_list = td_list[0].find_all("a")
                for a_tag in author_a_list:
                    if a_tag.get("title") is not None:
                        result_dict["Website"] = str(a_tag.get("href"))
                    
                    elif str(a_tag.get("href")).startswith("mailto:"):
                        result_dict["Email"] = str(a_tag.find_all(text=True)[0])
                    else:
                        result_dict["IP Address"] = str(a_tag.find_all(text=True)[0])

                
                
                # Finding comment time and content
                submit_div = td_list[1].find_all("div",{ "class" : "submitted-on" })[0]
                submit = submit_div.a
                time = submit.find_all(text=True)[0]
                time_list = str(time).split(" ")
                result_dict["Submit Time"] = str(time_list[2] + " " + time_list[3])
                result_dict["Submit Year"] = str(time_list[0].split("/")[0])
                result_dict["Submit Month"] = str(time_list[0].split("/")[1])
                result_dict["Submit Day"] = str(time_list[0].split("/")[2])
                result_dict["Comment"] = str(td_list[1].p.find_all(text=True)[0])

                # Getting post that comment was made on
                response_div = td_list[2].find_all("div",{"class":"response-links"})[0]
                post_span = response_div.find_all("span",{"class":"post-com-count-wrapper"})[0]
                result_dict["Post"] = str(post_span.a.find_all(text=True)[0])
                                    
                csv_dict_writer.writerow(result_dict)
    


with codecs.open('spam_data.csv','w',encoding="utf-8") as file:
    fieldnames = ['Comment Number',"Author","Website","Email","IP Address","Submit Time","Submit Year","Submit Month","Submit Day","Comment","Post"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    read_spam_html(writer,"comments_page1.htm")
    read_spam_html(writer,"comments_page2.htm")
    read_spam_html(writer,"comments_page3.htm")
    file.close()
