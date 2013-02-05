import csv

def read_graph_tsv1(filename='imdb-1.tsv'):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (node1, node2, year) in tsv:
        make_link(G, (node1, 'Star'), (node2, 'Book', year))
    return G

def read_graph_tsv2(filename='imdb-weight.tsv'):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    actors = {}
    for (node2, year, m) in tsv:
        actors[(node2, year)] = float(m)
    return actors

def make_link(G, node1, node2, n=1):
    if node1 not in G:
        G[node1] = {}
    G[node1].setdefault(node2, 100)
    G[node1][node2] = min(G[node1][node2], n)
    if node2 not in G:
        G[node2] = {}
    G[node2].setdefault(node1, 100)
    G[node2][node1] = min(G[node2][node1], n)
    return G

def make_second_graph(G, w):
    G2 = {}
    for k in G:
        if k[1] == 'Star':
            for k2 in G[k]:
                if k2[1] == 'Book':
                    for k3 in G[k2]:
                        if k3[1] == 'Star' and k3 != k:
                            make_link(G2, k[0], k3[0], w[(k2[0], k2[2])])
    return G2

k = read_graph_tsv1()
w = read_graph_tsv2()
k2 = make_second_graph(k, w)

import heapq

def dijkstra(G,v):
    dist_so_far = []
    distMap = {v: 0}
    heapq.heappush(dist_so_far, (0, v))
    final_dist = {}
    while len(final_dist) < len(G):
        if not dist_so_far:
            break
        d, w = heapq.heappop(dist_so_far)
        while d != distMap[w]:
            if not dist_so_far:
                break
            d, w = heapq.heappop(dist_so_far)
        # lock it down!
        final_dist[w] = d
        for x in G[w]:
            if x not in final_dist:
              d = max(final_dist[w], G[w][x])
              if x not in distMap or d < distMap[x]:
                distMap[x] = d
                heapq.heappush(dist_so_far, (d, x))
    return final_dist

answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

# Here are some test cases.
# For example, the obscurity score of the least obscure path
# between 'Ali, Tony' and 'Allen, Woody' is 0.5657
test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
 #       (u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}

#test
for nodes in test:
    assert dijkstra(k2, nodes[0])[nodes[1]] == test[nodes]
    print 'test pass'

ans = {}
for nodes in answer:
    ans[nodes] = dijkstra(k2, nodes[0])[nodes[1]]
print ans
