"page has the content of a web page as a string"
#page = ('<html xmlns="http://www.w3.org/1999/xhtml"><br/><head><br/><title>Udacity</title> <br/></head><br/><br/><body> <br/><h1>Udacity</h1><br/><br/> <p><b>Udacity</b> is a private institution of <a href="http://www.wikipedia.org/wiki/Higher_education"> higher education founded by</a> <a href="http://www.wikipedia.org/wiki/Sebastian_Thrun">Sebastian Thrun</a>, David Stavens, and Mike Sokolsky with the goal to provide university-level education that is "both high quality and low cost".<br/>It is the outgrowth of a free computer science class offered in 2011 through Stanford University. Currently, Udacity is working on its second course on building a search engine. Udacity was announced at the 2012 <a href="http://www.wikipedia.org/wiki/Digital_Life_Design">Digital Life Design</a> conference.</p><br/></body><br/></html>')

import urllib

def lucky_search(index, ranks, keyword):
    if keyword in index:
        high_rank = 0
        for page in index[keyword]:
            if ranks[page] >= high_rank:
                high_rank = ranks[page]
                result = page
        return result
    else:
        return None
            
            

cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}

def get_page(url):
    if url in cache:
        return cache[url]
    return ""

def real_get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_all_links(page):
    point = 0
    urls =  []
    while page.find('<a href=', point) != -1:
        start_link = page.find('<a href=', point)
        start_quote = page.find('"', start_link)
        url = page[start_quote+1:page.find('"', start_quote+1)]
        urls.append(url)
        point = start_quote+1
    return urls

def check_depth(page, crawled):
    for e in crawled:
        if e[0] == page:
            return e[1]

def crawl_web(seed, max_length = 1000):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            outlinks = get_all_links(content)
            add_page_to_index(index, page, content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
        if len(index) > max_length:
            break
    return index, graph

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def crawl_web_with_depth(seed, max_depth=10):
    crawled=[]
    tocrawl = [[seed, 0]]
    index = {}
    graph ={}
    while tocrawl:
        page, depth = tocrawl.pop()
        if depth <= max_depth:
            current_depth = check_depth(page, crawled)
            if page not in [pages for pages, depths in crawled]:
                crawled.append([page, depth])
                content = get_page(page)
                add_page_to_index(index, page, content)
                outlinks = get_all_links(content)
                graph[page] = outlinks
                for e in outlinks:
                    tocrawl.append([e, depth+1])            
            elif depth < current_depth:
                crawled.remove([page, current_depth])
                crawled.append([page, depth])
                #content = get_page(page)
                #add_page_to_index(index, page, content)
                #outlinks = get_all_links(content)
                #graph[page] = outlinks
                for e in outlinks:
                    tocrawl.append([e, depth+1])                              
    return index, graph

def compute_ranks(graph, t = 10, d = 0.8):
    ranks = {}
    npages = len(graph)
    for url in graph:
        ranks[url] = 1.0/npages
    for i in range(0, t):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    return None

def lookup_best(index, keyword, ranks, n=1, ifprint = False):
    if keyword in index:
        need_rank = index[keyword]
        result = []
        for i in range(n):
            result.append(['',0])
        for page in need_rank:
            if ranks[page] > result[n-1][1]:
                result.pop()
                result.append([page, ranks[page]])
                sort_pages(result)
        if ifprint:
            print "You asked for the first", n, "results for your keyword:",keyword
            print ""
            some_miss = 0
            for node in result:
                if node[0] != "":
                    print node[0]
                else:
                    some_miss += 1
            print ""
            if some_miss:
                print "Sorry, we cannot find certain number of results"
                print "Here is the first", n-some_miss, "results"
            else:
                print "That's all results"
        return [page for page, rank in result]
    if ifprint:
        print "No page is find given the certain keyword: ",keyword
    return None

def sort_pages(result):
    for i in range(len(result)):
        for j in range(i+1, len(result)):
            if result[i][1] < result[j][1]:
                result[i], result[j] = result[j], result[i]

def add_page_to_index(index,url,content):
    for i in content.split():
        add_to_index(index, i, url)

def real_search_engine(keyword, n, seed = 'http://news.google.com', ifdepth = False, depth = 10):
    if ifdepth:
        index, graph = crawl_web_with_depth(seed,depth)
    else:
        index, graph = crawl_web(seed)
    ranks = compute_ranks(graph)
    return lookup_best(index, keyword, ranks, n = 10, ifprint = True)

#search_engine(keyword = 'China', n = 10, ifdepth = True, depth = 2)
#search_engine(keyword = 'China', n = 10)

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

#print lucky_search(index, ranks, 'Hummus')

def ordered_search(index, ranks, keyword):
    return quick_sort(index[keyword], key = ranks)

def quick_sort(mylist, key):
    if len(mylist) <= 1:
        return mylist
    less = []
    more = []
    pivot = mylist[0]
    for p in range(1,len(mylist)):
        if key[mylist[p]] > key[pivot]:
            more.append(mylist[p])
        else:
            less.append(mylist[p])
    return quick_sort(more,key)+[pivot]+quick_sort(less,key)

print ordered_search(index, ranks, 'Hummus')
