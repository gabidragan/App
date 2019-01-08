python manage.py shell
from django.core.paginator import Paginator
from pprint import pprint

posts = ['1', '2', '3', '4', '5']
pprint(posts)
## ['1', '2', '3', '4', '5']

p = Paginator(posts, 2)

p = Paginator(posts, 2)
p.num_pages
## 3
for page in p.page_range:
	print(page)
## 1
## 2
## 3

p1 = p.page(1)
p1
## <Page 1 of 3>

p1.number
## 1

p1.object_list
## ['1', '2']

p1.has_previous()
## False

p1.has_next()
## True

p1.next_page_number()
## 2
