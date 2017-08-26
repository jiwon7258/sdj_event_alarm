from bs4 import  BeautifulSoup
import urllib.request
import time
import smtp_test
import smtplib
'''
파일마다 수정사항
1. 링크
2. 새로운 ~~ 알림
'''
'''

'''

class dataload:
    def __init__ (self, name):
        self.dbname= name # 클래스 명으로 dbname을 생성한다
        # self.mode = mode

    def load(self):
        filename = self.dbname +".txt" # filename은 생성 파일 이름을 변수로 가진다
        file = open(filename, 'w') # db.txt를 생성한다
        file.close()
        with urllib.request.urlopen(
                "http://sdjhs.djsch.kr/boardCnts/list.do?boardID=42367&m=0402&s=sdj") as url:  # 대회 알림
            data = url.read()
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')  # beautifulsoup를 통해 url을 불러온다
        list = soup.find_all('a', href='#contents')
        '''
        ===============테스트용 코드, 건드리지 말 것=======================
        if self.mode == 1:
            with urllib.request.urlopen("http://sdjhs.djsch.kr/boardCnts/list.do?type=default&page=1&m=0402&s=sdj&boardID=42367") as url: # 대회 알림
                data = url.read()
            soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8') #beautifulsoup를 통해 url을 불러온다
            list = soup.find_all('a', href='#contents')
        if self.mode == 2 :
            with urllib.request.urlopen(
                    'http://sdjhs.djsch.kr/boardCnts/list.do?type=default&page=1&m=0401&s=sdj&boardID=42366') as url: # 평가알림
                data = url.read()
            soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')  # beautifulsoup를 통해 url을 불러온다
            list = soup.find_all('a', href='#contents')
        '''
        file = open(filename, 'a')
        n = len(list)
        for s in list:
            title = s.get('title')
            file.write(title + '\n')
        file.close()
        file = open(filename, 'r')
        self.data = file.readlines()
        file.close()



origindb = dataload('origindb')
origindb.load()
loop = 0

while True :

    newdb = dataload('newdb')
    newdb.load()
    # print('newdb_data =', newdb.data)

    originfile = open('origindb.txt')
    originfiledb = originfile.readlines()
    originfile.close()

    # 서로 다른 것이 있는지 검사하는 코드
    s = set(originfiledb)
    result = [x for x in set(newdb.data) if x not in s]



    """
    1. newdb에 존재 but origindb에 없는 값 -> diff.txt에 복사
    2. origindb를 덮어씌운다
    """

    if result :
        print('if문 실행합니다')
        #1번 코드
        originfile = open('origindb.txt', 'r')
        originfiledb = originfile.readlines()
        # print(originfiledb)

        newfile = open('newdb.txt', 'r')
        newfiledb = newfile.readlines()

        diff_file = open('diff.txt', 'w')
        for text in newfiledb:
            if text not in originfiledb:
                diff_file.write(text)
        diff_file.close()
        diff_file = open('diff.txt', 'r')
        print(diff_file.readlines())
        # print(originfiledb)
        # print(newfiledb)

        # 2번 코드
        originfile = open('origindb.txt', 'w')
        newfile = open('newdb.txt', 'r')
        newfiledb = newfile.readlines()
        # print(newfiledb)
        for text in newfiledb:
            originfile.write(text)

        # 이메일 발송코드
        contents = ''
        diff_file = open('diff.txt', 'r')
        number_ = 0
        for text in diff_file:
            number_ += 1
            contents = contents + str(number_) + '. ' + str(text)
        contents = '자세한 안내 사항은 서대전고등학교 홈페이지를 참조하세요\n' + contents
        mail_list = open('mail_list.txt', 'r')
        for mailname in mail_list:
            smtp_test.sendMail('sdjevent@gmail.com', str(mailname), '[서대전고]새로운 대회 알림', contents)



    loop = loop + 1

    print('%s회 루프 끝났습니다' % loop)
    # time.sleep(3600)  # 한시간 주기로 검색을 한다