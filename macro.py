import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Macro:

    def __init__(self):

        self.driver = webdriver.Ie('./bin/IEDriverServer.exe')
        self.windows = 0
        self.timeout = 1

    def wait(self, element_id):
        expected = EC.presence_of_element_located((By.ID, element_id))
        WebDriverWait(self.driver, 10).until(expected)
        return self

    def test1(self):

        self.driver.get('http://www.edup.co.kr/')
        # 여기 IE에서 사용되는 쿠키로 변경
        cookies = '''
        '''
        self.driver.execute_script(cookies);
        self.driver.get('http://www.edup.co.kr/lectureroom/study_list.asp')

    def get_study_list(self):

        script = """list = [];
        a = document.getElementsByClassName('btn_lectureroom01');
        for(i = 0; i < a.length; i++){

            list.push(a.item(i).href);

        }
        return list;
        """
        study_list = self.driver.execute_script(script)
        print("[*] Get study list")
        return study_list

    def get_lesson_list(self):
    
        script = """list = []
        tr = document.getElementsByClassName('tdS table_bg_color').tags('tr');
        for(i = 0; i < tr.length; i++){

            try{
                not_success= tr.item(i).getElementsByTagName('td').item(3).innerText != "100% " && tr.item(i).getElementsByTagName('td').item(5).innerText != "100% " ;
                if(not_success){

                console.log(i);	
                list.push(tr.item(i).getElementsByClassName('Nbtn_study2 btnsize_70').item(0).href);

                    }
            }catch(e){}
        }
        return list;
        """
        lesson_list = self.driver.execute_script(script)
        print(lesson_list)
        print("[*] Get lesson list")
        return lesson_list

    def window_open(self, goto):

        print("[*] Window open")
        handles_before = self.driver.window_handles
        self.driver.execute_script(goto)
        self.windows += 1
        time.sleep(self.timeout)
        WebDriverWait(self.driver, 10).until(lambda driver: len(handles_before) != len(self.driver.window_handles))
        self.driver.switch_to_window(self.driver.window_handles[self.windows])
        return self.driver.window_handles[self.windows]

    def window_close(self):
    
        print("[*] Window close")
        handles_before = self.driver.window_handles
        self.driver.close()
        self.windows -= 1
        time.sleep(self.timeout)
        WebDriverWait(self.driver, 10).until(lambda driver: len(handles_before) != len(self.driver.window_handles))        

    def window_switch(self, dst):

        print("[*] Window switch")
        self.driver.switch_to_window(dst)

    def location(self, go):

        time.sleep(self.timeout)
        self.driver.execute_script('javascript:GoPage("'+go+'")')
        time.sleep(self.timeout)

    def watch(self):

        time.sleep(self.timeout)
        wait_time = self.driver.execute_script("video = $('video'); Play715	= $('.play_img'); setInterval(function(){if(document.getElementById('vod_skin_pop').style.display == 'block') Play715.click(); }, 1000); return video[0].duration;")
        #print("[*] Wait time: ")
        time.sleep(wait_time+2)

    def run(self):

        try:
            self.test1()
            study_list = self.get_study_list()
            study_list_page = self.driver.window_handles[self.windows]

            for study in study_list:

                lesson_list_page = self.window_open(study)
                print(1)
                self.wait("iSysInfo")
                print(2)
                lesson_list = self.get_lesson_list()
                
                for lesson in lesson_list:

                    print(lesson)
                    class_page = self.window_open(lesson)
                    self.wait("page_01")
                    self.location("1002.html")
                    self.location("1003.html")
                    self.location("1004.html")
                    self.watch()
                    self.location("1005.html")
                    self.location("1006.html")
                    self.location("1007.html")
                    self.window_close()
                    self.window_switch(lesson_list_page)


                self.window_close()
                self.window_switch(study_list_page)

            self.driver.quit()

        except:
        
            print(sys.exc_info()[0])
            self.driver.quit()
            print("restart")
            self.driver = webdriver.Ie('./bin/IEDriverServer.exe')
            time.sleep(self.timeout)
            self.windows = 0
            self.run()

    def close(self):

        self.driver.quit()

if __name__ == '__main__':

    test = Macro()
    test.run()

