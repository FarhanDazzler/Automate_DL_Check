# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 23:08:31 2022

@author: chariteash.narra
"""

import time
from selenium import webdriver
import pandas as pd
import warnings
from selenium.webdriver.chrome.options import Options
from  selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DesiredCapabilities

def main():   
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    caps = DesiredCapabilities.CHROME
    driver = webdriver.Chrome(desired_capabilities=caps,options=options)
#    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    
    driver.set_page_load_timeout(60) 
    
   
    df = pd.read_excel('URLS.xlsx')   
    urls = df.Input_url
    print ("AA")
    expected_ga_id = df.GA_ID[0]
    expected_launch_property = df.property_name[0]
    expected_report_suite_id = df.Report_Suite_ID[0]
    expected_internal_domain = df.internal_domain[0]
    unexp_ga_id = []
    unexp_launch_property = []
    unexp_report_suite = []
    unexp_content_type = []
    unexp_internal_domain = []                  
    unsuccessful_urls = []
    content_type = []
#    expectedLaunchProperty = df.property_name[0]
#    print (expectedLaunchProperty)
#    expectedReport_Suite_ID = df.Report_Suite_ID[0]
#    print (expectedReport_Suite_ID)
    driver.get(urls[0])
    AllPageURLs = []

    urls = driver.execute_script('''
                        const AllPageURLs = [];
                        var allButtons = document.querySelectorAll("loc");
    
    for (var i = 0; i < allButtons.length; i++) {
    const pageURL = allButtons[i].innerHTML;
    AllPageURLs.push(pageURL); 
    } 
    //console.log(AllPageURLs);       
    return AllPageURLs;                      
                       
                                            
                        ''')
                        
    print ("Fetched Urls")
    driver.close()                   

    driver = webdriver.Chrome(desired_capabilities=caps,options=options)
#    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    
    driver.set_page_load_timeout(60) 
#    print (urls)
    i = 1;
    c = 1;

    # Run loop on input URL's $ Get required paramter's values
    #while (i<=5):
    ga_id = []
    launch_property = []
    report_suite = []
    internal_domain = []
    content_type = []
#    cd2 = []
#    cd3 = []
#    cd4 = []
#    cd5 = []
    skipped = []
    success_urls = []
    flag = False
    print ("Taking unique Urls")
    for url in urls:
        print("URL is --> "+str(url))
        try:
            driver.get(str(url))
            time.sleep(10)
            ua_id = driver.execute_script('''
          
                      if(typeof digitalData != "undefined"){
                      if(typeof digitalData.trackingInfo != "undefined"){
                      if(typeof digitalData.trackingInfo.tool != "undefined"){
                      if(digitalData.trackingInfo.tool.length>0){
                      if(typeof digitalData.trackingInfo.tool[0] != "undefined"){
                      if(digitalData.trackingInfo.tool[0].id){
                              return digitalData.trackingInfo.tool[0].id;
                      }
                      }
                      }
                      }}}
                      
                      if(typeof _satellite !="undefined"){ 
                      if(_satellite.getVar("Global_AGID")!= "undefined"){
                              return _satellite.getVar("Global_AGID");
                      }}
                      if(typeof udm != "undefined"){
                      if(typeof udm.gaa != "undefined"){
                          return udm.gaa;
                      }}
                      
                      return "GA-id not found ";                          
                      ''')
            
        except:
            print('Time out for '+url)
            skipped.append(url)
            i+=1
            flag = True
            driver.close()
            driver = driver  # Optional argument, if not specified will search path.
            driver.set_page_load_timeout(30) 
            continue
        
        if(flag==True):        
            try:
                ## Popup Evidon
                driver.find_element_by_id('_evidon-accept-button').click()
                time.sleep(1)
                driver.get(url)
            except:
                
                try:
                ## Popup onetrust
                    driver.find_element_by_id('_onetrust-accept-btn-handler').click()
                    time.sleep(1)
                    driver.get(url)
                except:
                    try:
                        ## Popup type 2
                        driver.switch_to_frame(0)
                        time.sleep(2)
                        driver.find_element_by_class_name('acceptbutton').click()
                        time.sleep(1)
                        driver.get(url)
                    except:
                        ## Evidon popup type 2
                        try:
                            driver.switch_to_default_content()
                            driver.find_element_by_id('_evidon-banner-acceptbutton').click()
                            time.sleep(1)
                            driver.get(url)
                        except:
                            try:
                                driver.switch_to_frame(0)
                                driver.find_element_by_class_name('acc').click()
                                time.sleep(1)
                                driver.get(url)
                            except:
                                try:
                                    driver.switch_to_default_content()
                                    pass
                                except:
                                    skipped('Skipping for '+url)
                                    i+=1
                                    continue
           
        if(flag==True or flag==False):
             try:
              print("Checking GA ID")
              time.sleep(4)
              ua_id = driver.execute_script('''
            
                        if(typeof digitalData != "undefined"){
                        if(typeof digitalData.trackingInfo != "undefined"){
                        if(typeof digitalData.trackingInfo.tool != "undefined"){
                        if(digitalData.trackingInfo.tool.length>0){
                        if(typeof digitalData.trackingInfo.tool[0] != "undefined"){
                        if(digitalData.trackingInfo.tool[0].id){
                                return digitalData.trackingInfo.tool[0].id;
                        }
                        }
                        }
                        }}}
                        
                        if(typeof _satellite !="undefined"){ 
                        if(_satellite.getVar("Global_AGID")!= "undefined"){
                                return _satellite.getVar("Global_AGID");
                        }}
                        if(typeof udm != "undefined"){
                        if(typeof udm.gaa != "undefined"){
                            return udm.gaa;
                        }}
                        
                        return "GA-id not found ";                          
                        ''')
              print(ua_id)
              print("Checking Launch")
              launch = driver.execute_script('''
                     
                        if(typeof _satellite !="undefined"){ 
                        if(_satellite.property!= "undefined"){
                            return _satellite.property.name;
                        }}
                        return "Property not found ";                          
                        ''')
              print(launch)  
              print("Checking Report Suite")
              reportSuite = driver.execute_script('''
                        if(typeof digitalData != "undefined"){
                        if(typeof digitalData.trackingInfo != "undefined"){
                        if(typeof digitalData.trackingInfo.tool != "undefined"){
                        if(digitalData.trackingInfo.tool.length>0){
                        if(typeof digitalData.trackingInfo.tool[1] != "undefined"){
                        if(digitalData.trackingInfo.tool[1].id){
                                return digitalData.trackingInfo.tool[1].id;
                       }
                        }
                        }
                        }}}
                        if(typeof _satellite !="undefined"){ 
                        if(_satellite.getVar('Global_ReportSuiteID')!= "undefined"){
                                return _satellite.getVar('Global_ReportSuiteID');
                        }}
                        return "RS not found";                          
                        ''')
              print(reportSuite) 
              print("Checking Content Type")
              contentType = driver.execute_script('''
                                       if(typeof digitalData != "undefined"){
                                      if(typeof digitalData.page != "undefined"){
                                      if(typeof digitalData.page.attributes != "undefined"){
                                     if(digitalData.page.attributes.contentType.length>0){
                                          return digitalData.page.attributes.contentType;
                                      }
                                      
                                      }}}
                                      return "contentType not found";
                                      ''')
              print(contentType)   
              print("Checking internal Domain")                      
              internalDomain = driver.execute_script('''
                                         if(typeof digitalData != "undefined"){
                                         if(typeof digitalData.siteInfo != "undefined"){
                                         if(typeof digitalData.siteInfo.internalDomain != "undefined"){
                                             return digitalData.siteInfo.internalDomain;
                                         }
                                         
                                         }}
                                         return "internalDomain not found";
                                         ''')   
              print(internalDomain)                               



              if expected_ga_id == ua_id and  expected_launch_property == launch and  expected_report_suite_id == reportSuite and contentType != "undefined" and expected_internal_domain ==internalDomain :
                ga_id.append(ua_id)
                launch_property.append(launch)
                report_suite.append(reportSuite)
                content_type.append(contentType)
                internal_domain.append(internalDomain)            
                success_urls.append(url)
             
              else :
                  unexp_ga_id.append(ua_id)
                  unexp_launch_property.append(launch)
                  unexp_report_suite.append(reportSuite)
                  unexp_content_type.append(contentType)
                  unexp_internal_domain.append(internalDomain)                   
                  unsuccessful_urls.append(url)
                 
                
              i = i+1
              c = c+1
              
             except:
                print ('skipping' + url)
                skipped.append(url)
                
#        if output_value_ is not None:
#    					print("Parameter value is -->"+output_value_)
#    					sheet1.write(c, 0, input_url_new) 
#    					sheet1.write(c, 1, output_value_) 
#                    	# Write values in Excel
#    					wb.save('Automate_Testing_result.xls') 
#    					print("\n")
#        i = i+1
#        c = c+1

    # GET VALUE FROM DIGITALDATA OBJECT
    #print(driver.execute_script(''' return digitalData.page.pageInfo.pageName; '''))
#    print(len(success_urls),len(ga_id), len(launch_property) )# Print all of them out here
    cf1 = pd.DataFrame({'url':success_urls,'GA_ID':ga_id,'Launch':launch_property,'reportSuite':report_suite,'contentType':content_type,'internalDomain':internal_domain})
#    cf2 = pd.DataFrame({'url':success_urls,'Launch':launch_property})
    cf2 = pd.DataFrame({'url':unsuccessful_urls,'GA_ID':unexp_ga_id,'Launch':unexp_launch_property,'reportSuite':unexp_report_suite,'contentType':unexp_content_type,'internalDomain':unexp_internal_domain})
#    cf1.to_excel('test_accenture.xlsx',index= False)
#    cf2.to_excel('test_accenture.xlsx',index= False)    
    
    writer = pd.ExcelWriter('test_accenture.xlsx', engine='xlsxwriter')
#
## Write each dataframe to a different worksheet.
    cf1.to_excel(writer, sheet_name='Successful')
#    cf2.to_excel(writer, sheet_name='Sheet2')
    cf2.to_excel(writer, sheet_name='UnSuccessful')
    writer.save()

    driver.quit()
main()