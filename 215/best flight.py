##import heapq
##
##def make_link(G, node1, node2, w):
##    if node1 not in G:
##        G[node1] = {}
##    if node2 not in G[node1]:
##        (G[node1])[node2] = ('MAX',"MAX",'MAX')
##    (G[node1])[node2] = min(w, G[node1][node2])
####    if node2 not in G:
####        G[node2] = {}
####    if node1 not in G[node2]:
####        (G[node2])[node1] = ('MAX',"MAX",'MAX')
####    (G[node2])[node1] = min(w, G[node2][node1])
##    return G
##
##def dijkstra(G,v):
##    dist_so_far = []
##    distMap = {v: (0, 0, [],('',''))}
##    heapq.heappush(dist_so_far, (0, 0, v, [],('','')))
##    final_dist = {}
##    while len(final_dist) < len(G):
##        d, t, w, path, stnd = heapq.heappop(dist_so_far)
##        while d != distMap[w][0] or t != distMap[w][1]:
##          d, t, w, path, stnd = heapq.heappop(dist_so_far)
##        # lock it down!
##        final_dist[w] = (d, t, path)
##        for x in G[w]:
##            if x not in final_dist:
##              d = final_dist[w][0] + G[w][x][0]
##              t = final_dist[w][1] + G[w][x][1]
##              path = final_dist[w][2] + [G[w][x][3]]
##              if x not in distMap or d < distMap[x][0] or t < distMap[x][1]:
##                distMap[x] = (d, t, path)
##                heapq.heappush(dist_so_far, (d, t, x, path))
##    return final_dist
##
##def find_best_flights(flights, origin, destination):
##    G = {}
##    for k in flights:
##        make_link(G, k[1], k[2], (k[5], k[3], k[4], k[0]))
##    print G
##    final_path = dijkstra(G, origin)
##    if destination not in final_path:
##        return None
##    # your code here
##    return final_path[destination][2]

def compute_time(k3, k4):
    return 60*(int(k4[0:2])-int(k3[0:2])) +int(k4[3:]) - int(k3[3:])

def find_best_flights(flights, origin, destination):
    to_search = [(k[5], compute_time(k[3], k[4]), [k]) for k in flights if k[1] == origin]
    while to_search:
        w = to_search.pop(0)
        path = w[2]
        #print [p[0] for p in path]
        if path[-1][2] == destination:
            return [k[0] for k in path]
        next_flight = [p for p in flights
                       if (path[-1][2] == p[1] and compute_time(path[-1][4], p[3])>0)]
        #print next_flight
        to_search += [(w[0]+k[5], compute_time(path[0][3], k[4]), path+[k]) for k in next_flight]
        to_search.sort()
        
#
all_flights = [(523, 'Broome', 'Derby', '07:17', '08:57', 60),
               (526, 'Broome', 'Derby', '08:41', '10:30', 50),
               (527, 'Broome', 'Derby', '11:46', '13:24', 200),
               (530, 'Broome', 'Derby', '14:23', '15:59', 50),
               (540, 'Broome', 'Derby', '17:49', '19:40', 50),
               (546, 'Broome', 'Derby', '20:34', '22:09', 20),
               (547, 'Broome', 'Perth', '06:41', '08:44', 30),
               (549, 'Broome', 'Perth', '17:16', '19:18', 100),
               (559, 'Carnarvon', 'Geraldton', '09:05', '10:57', 50),
               (561, 'Carnarvon', 'Geraldton', '11:14', '13:03', 30),
               (578, 'Carnarvon', 'Geraldton', '14:56', '16:48', 150),
               (582, 'Carnarvon', 'Geraldton', '17:05', '18:46', 50),
               (598, 'Carnarvon', 'Geraldton', '22:08', '23:49', 20),
               (599, 'Carnarvon', 'Perth', '07:04', '09:46', 200),
               (100, 'Carnarvon', 'Perth', '10:53', '13:38', 60),
               (604, 'Carnarvon', 'Perth', '14:50', '17:16', 200),
               (612, 'Carnarvon', 'Perth', '19:54', '22:38', 50),
               (107, 'Derby', 'Broome', '08:44', '10:36', 160),
               (108, 'Derby', 'Broome', '21:18', '23:04', 30),
               (622, 'Derby', 'Fitzroy Crossing', '13:59', '15:04', 60),
               (112, 'Derby', 'Fitzroy Crossing', '19:24', '20:15', 60),
               (113, 'Derby', 'Geraldton', '07:00', '08:10', 20),
               (115, 'Derby', 'Geraldton', '10:00', '11:07', 200),
               (118, 'Derby', 'Geraldton', '13:24', '14:31', 50),
               (121, 'Derby', 'Geraldton', '14:41', '15:52', 50),
               (122, 'Derby', 'Geraldton', '17:05', '18:09', 60),
               (635, 'Derby', 'Geraldton', '18:59', '20:18', 60),
               (638, 'Fitzroy Crossing', 'Derby', '09:18', '10:08', 50),
               (131, 'Fitzroy Crossing', 'Derby', '13:59', '14:51', 160),
               (226, 'Fitzroy Crossing', 'Derby', '14:34', '15:34', 110),
               (139, 'Fitzroy Crossing', 'Derby', '18:43', '19:36', 50),
               (654, 'Fitzroy Crossing', 'Halls Creek', '07:55', '09:48', 180),
               (143, 'Fitzroy Crossing', 'Halls Creek', '09:45', '11:39', 20),
               (280, 'Fitzroy Crossing', 'Halls Creek', '15:10', '17:07', 110),
               (660, 'Fitzroy Crossing', 'Halls Creek', '18:41', '20:24', 30),
               (661, 'Fitzroy Crossing', 'Halls Creek', '20:35', '22:19', 200),
               (663, 'Geraldton', 'Carnarvon', '08:30', '10:24', 30),
               (152, 'Geraldton', 'Carnarvon', '12:52', '14:42', 50),
               (153, 'Geraldton', 'Carnarvon', '15:24', '17:15', 30),
               (154, 'Geraldton', 'Carnarvon', '18:07', '19:53', 180),
               (671, 'Geraldton', 'Derby', '06:01', '07:10', 120),
               (676, 'Geraldton', 'Derby', '10:46', '12:09', 20),
               (165, 'Geraldton', 'Derby', '11:29', '12:45', 30),
               (683, 'Geraldton', 'Derby', '14:17', '15:23', 50),
               (174, 'Geraldton', 'Derby', '16:45', '17:58', 180),
               (175, 'Geraldton', 'Derby', '18:31', '19:47', 20),
               (179, 'Halls Creek', 'Fitzroy Crossing', '06:32', '08:22', 200),
               (187, 'Halls Creek', 'Fitzroy Crossing', '13:19', '15:03', 200),
               (702, 'Halls Creek', 'Fitzroy Crossing', '14:04', '15:45', 20),
               (192, 'Halls Creek', 'Fitzroy Crossing', '20:08', '21:59', 160),
               (195, 'Halls Creek', 'Kalbarri', '06:43', '09:01', 110),
               (709, 'Halls Creek', 'Kalbarri', '08:45', '11:04', 200),
               (199, 'Halls Creek', 'Kalbarri', '13:21', '15:39', 20),
               (209, 'Halls Creek', 'Kalbarri', '15:45', '18:01', 100),
               (723, 'Halls Creek', 'Kalbarri', '16:04', '18:10', 50),
               (724, 'Halls Creek', 'Kalbarri', '19:52', '22:07', 160),
               (216, 'Kalbarri', 'Halls Creek', '06:15', '08:34', 100),
               (217, 'Kalbarri', 'Halls Creek', '14:57', '17:14', 200),
               (730, 'Kalbarri', 'Halls Creek', '21:05', '23:24', 20),
               (731, 'Kalbarri', 'Perth', '06:18', '08:50', 50),
               (734, 'Kalbarri', 'Perth', '12:23', '14:59', 120),
               (735, 'Kalbarri', 'Perth', '12:59', '15:19', 30),
               (738, 'Kalbarri', 'Perth', '18:41', '21:10', 60),
               (739, 'Kalbarri', 'Perth', '19:42', '22:18', 60),
               (740, 'Laverton', 'Leonora', '07:39', '08:53', 180),
               (745, 'Laverton', 'Leonora', '12:20', '13:32', 20),
               (748, 'Laverton', 'Leonora', '13:44', '15:08', 30),
               (751, 'Laverton', 'Leonora', '18:00', '19:11', 200),
               (240, 'Laverton', 'Leonora', '20:34', '21:40', 110),
               (754, 'Laverton', 'Perth', '07:21', '08:21', 180),
               (247, 'Laverton', 'Perth', '20:11', '21:22', 160),
               (248, 'Leinster', 'Perth', '08:37', '11:16', 180),
               (249, 'Leinster', 'Perth', '13:44', '16:12', 110),
               (763, 'Leinster', 'Perth', '16:29', '19:06', 160),
               (765, 'Leinster', 'Perth', '19:17', '21:47', 20),
               (981, 'Leinster', 'Wiluna', '10:51', '13:03', 200),
               (770, 'Leinster', 'Wiluna', '16:02', '18:17', 50),
               (259, 'Leinster', 'Wiluna', '19:44', '22:09', 60),
               (772, 'Leonora', 'Laverton', '10:39', '11:59', 110),
               (987, 'Leonora', 'Laverton', '15:56', '17:13', 110),
               (264, 'Leonora', 'Laverton', '21:39', '22:48', 200),
               (779, 'Leonora', 'Perth', '10:29', '11:59', 50),
               (780, 'Leonora', 'Perth', '11:26', '12:58', 50),
               (783, 'Leonora', 'Perth', '19:48', '21:25', 30),
               (278, 'Meekatharra', 'Mt Magnet', '07:40', '08:42', 60),
               (792, 'Meekatharra', 'Mt Magnet', '08:35', '09:35', 60),
               (793, 'Meekatharra', 'Mt Magnet', '11:50', '12:44', 110),
               (796, 'Meekatharra', 'Mt Magnet', '14:32', '15:26', 30),
               (798, 'Meekatharra', 'Mt Magnet', '16:56', '17:52', 160),
               (288, 'Meekatharra', 'Mt Magnet', '19:38', '20:27', 60),
               (289, 'Meekatharra', 'Perth', '08:12', '09:28', 50),
               (803, 'Meekatharra', 'Perth', '09:12', '10:25', 30),
               (805, 'Meekatharra', 'Perth', '12:10', '13:16', 50),
               (298, 'Meekatharra', 'Perth', '13:33', '14:40', 50),
               (391, 'Meekatharra', 'Perth', '16:45', '17:50', 30),
               (815, 'Meekatharra', 'Perth', '20:17', '21:29', 110),
               (817, 'Monkey Mia', 'Perth', '08:26', '10:51', 20),
               (393, 'Monkey Mia', 'Perth', '13:12', '15:51', 30),
               (825, 'Monkey Mia', 'Perth', '21:01', '23:37', 180),
               (314, 'Mt Magnet', 'Meekatharra', '06:29', '07:30', 30),
               (827, 'Mt Magnet', 'Meekatharra', '08:56', '10:00', 50),
               (829, 'Mt Magnet', 'Meekatharra', '13:09', '14:14', 30),
               (832, 'Mt Magnet', 'Meekatharra', '14:10', '15:09', 30),
               (833, 'Mt Magnet', 'Meekatharra', '17:39', '18:41', 180),
               (322, 'Mt Magnet', 'Meekatharra', '19:51', '20:55', 160),
               (333, 'Mt Magnet', 'Perth', '07:53', '08:38', 120),
               (846, 'Mt Magnet', 'Perth', '15:45', '16:29', 20),
               (967, 'Mt Magnet', 'Perth', '18:04', '18:49', 20),
               (336, 'Mt Magnet', 'Wiluna', '07:34', '09:08', 200),
               (338, 'Mt Magnet', 'Wiluna', '13:35', '15:17', 30),
               (856, 'Mt Magnet', 'Wiluna', '14:54', '16:27', 50),
               (345, 'Mt Magnet', 'Wiluna', '18:03', '19:35', 50),
               (859, 'Perth', 'Broome', '07:21', '09:14', 50),
               (348, 'Perth', 'Broome', '10:37', '12:46', 60),
               (349, 'Perth', 'Broome', '12:56', '14:57', 20),
               (350, 'Perth', 'Broome', '15:01', '17:11', 110),
               (356, 'Perth', 'Broome', '18:03', '20:03', 60),
               (364, 'Perth', 'Broome', '18:45', '20:54', 150),
               (880, 'Perth', 'Carnarvon', '07:39', '10:09', 50),
               (884, 'Perth', 'Carnarvon', '10:33', '13:11', 30),
               (374, 'Perth', 'Carnarvon', '12:04', '14:31', 50),
               (375, 'Perth', 'Carnarvon', '13:59', '16:32', 30),
               (378, 'Perth', 'Carnarvon', '17:04', '19:38', 50),
               (299, 'Perth', 'Carnarvon', '19:27', '22:09', 50),
               (383, 'Perth', 'Kalbarri', '06:41', '09:12', 120),
               (384, 'Perth', 'Kalbarri', '12:42', '15:03', 20),
               (898, 'Perth', 'Kalbarri', '19:13', '21:38', 30),
               (390, 'Perth', 'Laverton', '10:20', '11:23', 60),
               (321, 'Perth', 'Laverton', '14:08', '15:03', 60),
               (905, 'Perth', 'Laverton', '19:58', '20:53', 100),
               (395, 'Perth', 'Leinster', '06:59', '09:28', 200),
               (396, 'Perth', 'Leinster', '10:17', '12:48', 100),
               (401, 'Perth', 'Leinster', '14:24', '16:50', 50),
               (914, 'Perth', 'Leinster', '18:54', '21:34', 160),
               (404, 'Perth', 'Leonora', '11:03', '12:40', 30),
               (918, 'Perth', 'Leonora', '12:37', '14:17', 150),
               (408, 'Perth', 'Leonora', '20:42', '22:10', 100),
               (923, 'Perth', 'Meekatharra', '06:21', '07:35', 110),
               (927, 'Perth', 'Meekatharra', '10:25', '11:26', 20),
               (933, 'Perth', 'Meekatharra', '14:27', '15:24', 50),
               (934, 'Perth', 'Meekatharra', '17:49', '18:50', 200),
               (941, 'Perth', 'Meekatharra', '21:56', '23:08', 30),
               (430, 'Perth', 'Monkey Mia', '06:18', '08:48', 30),
               (943, 'Perth', 'Monkey Mia', '12:11', '14:48', 180),
               (432, 'Perth', 'Monkey Mia', '17:32', '20:13', 50),
               (433, 'Perth', 'Monkey Mia', '19:48', '22:23', 100),
               (947, 'Perth', 'Mt Magnet', '06:43', '07:23', 100),
               (948, 'Perth', 'Mt Magnet', '13:59', '14:54', 20),
               (954, 'Perth', 'Mt Magnet', '15:44', '16:26', 120),
               (955, 'Perth', 'Mt Magnet', '19:34', '20:26', 200),
               (475, 'Perth', 'Wiluna', '07:34', '09:57', 60),
               (959, 'Perth', 'Wiluna', '09:44', '12:22', 50),
               (455, 'Perth', 'Wiluna', '12:22', '14:45', 60),
               (969, 'Perth', 'Wiluna', '14:26', '16:59', 50),
               (458, 'Perth', 'Wiluna', '17:19', '19:38', 60),
               (459, 'Perth', 'Wiluna', '19:09', '21:35', 30),
               (461, 'Wiluna', 'Leinster', '07:54', '10:16', 20),
               (462, 'Wiluna', 'Leinster', '08:35', '10:50', 200),
               (463, 'Wiluna', 'Leinster', '11:50', '14:01', 200),
               (976, 'Wiluna', 'Leinster', '13:54', '16:15', 50),
               (469, 'Wiluna', 'Leinster', '17:24', '19:43', 30),
               (984, 'Wiluna', 'Leinster', '19:58', '22:13', 200),
               (847, 'Wiluna', 'Mt Magnet', '07:13', '08:42', 30),
               (478, 'Wiluna', 'Mt Magnet', '11:48', '13:14', 50),
               (993, 'Wiluna', 'Mt Magnet', '13:00', '14:27', 20),
               (483, 'Wiluna', 'Mt Magnet', '17:20', '18:57', 60),
               (422, 'Wiluna', 'Mt Magnet', '21:40', '23:21', 60),
               (494, 'Wiluna', 'Perth', '08:28', '11:07', 160),
               (253, 'Wiluna', 'Perth', '11:17', '13:41', 150),
               (498, 'Wiluna', 'Perth', '13:53', '16:13', 60),
               (501, 'Wiluna', 'Perth', '17:59', '20:27', 20),
               (505, 'Wiluna', 'Perth', '20:21', '22:41', 180)]

def test():
    flights = find_best_flights(all_flights, 'Mt Magnet', 'Fitzroy Crossing')
    assert flights == [314, 803, 348, 530, 112]

    flights = find_best_flights(all_flights, 'Leonora', 'Fitzroy Crossing')
    assert flights == None

    flights = find_best_flights(all_flights, 'Meekatharra', 'Wiluna')
    assert flights == [391, 459]

    print 'test pass'

test()
