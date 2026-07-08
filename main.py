from maindef import crawling
from taobang import create_database,insert,simulate7days
create_database()
insert(crawling())
#simulate7days()

