from datetime import datetime


def verify_dates(user1, location, date, mapping_list_locations):
    # Filter the num of time A stalker B (A and B stay in the same place but but arrive after A)
    return len(list(filter(lambda B: user1 == B[0]
                                     and location == B[4]
                                     and datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
                                     > datetime.strptime(B[1], '%Y-%m-%dT%H:%M:%SZ'),
                           mapping_list_locations))) > 0


if __name__ == '__main__':
    import itertools
    file_friends = open("Gowalla_edges.txt", "r")
    file_history = open("Gowalla_totalCheckins.txt", "r")
    file_list = file_history.readlines()

    # Delete the space between raws and cols
    remove_spaces_location = list(map(lambda i: i.rstrip("\n"), file_list))
    remove_spaces_friends = list(map(lambda i: i.rstrip("\n"), file_friends))

    mapping_list_friends = list(map(lambda i: i.replace('\t','-'), remove_spaces_friends))
    mapping_list_locations = list(map(lambda i: i.split('\t'), remove_spaces_location))
    #
    mapping_list_locations_users = list(set(map(lambda i: i[0], mapping_list_locations)))

    couples = {}
    data_friends = []
    data_no_friends = []

    for A in mapping_list_locations_users:
        locations = list(filter(lambda B: A != B[0]
                                          and verify_dates(A, B[4], B[1], mapping_list_locations),
                                mapping_list_locations))
        for i in locations:
            if locations:
                password = A+"-"+i[0]
                if password in couples:
                    couples[password].append(i[4])
                else:
                    couples[password] = ([i[4]])

    for i in couples.keys():
        couples[i] = len(list(set(couples[i])))

    for friends in couples.items():
        for friends_list in mapping_list_friends:
            if str(friends[0]) == str(friends_list):
                data_friends.append(friends)
            else:
                data_no_friends.append(friends)

    print("The couple of friends with maximum stalker score is : ", max(data_friends))
    print("The couple of no-friends with maximum stalker score is : ", max(data_no_friends))


