import http.client
import json
import csv


#############################################################################################################################
#
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_move_detail(), get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0],n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0],e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str)->None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        
        # add new node if it does not exist
        if (id, name) not in self.nodes:
            self.nodes.append((id, name))

        # return NotImplemented


    def add_edge(self, source: str, target: str)->None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """

        # add new node if it does not exist
        if (source, target) not in self.edges and (target, source) not in self.edges:
            self.edges.append((source, target))

        # return NotImplemented


    def total_nodes(self)->int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)


    def total_edges(self)->int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)


    def max_degree_nodes(self)->dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """

        # initialize
        node_id = '0'
        highest_degree =  0
        highest_degree_dict = {node_id: highest_degree}

        # loop through node
        for node in self.nodes:
            node_id = node[0]
            node_degree = 0

            # loop through edges
            for edge in self.edges:
                if edge[0] == node[0] or edge[1] == node[0]:
                    node_degree = node_degree + 1
            # compare node_degree
            if node_degree > highest_degree:
                # higher
                highest_degree = node_degree
                highest_degree_dict = {node_id: highest_degree}
                continue
            if node_degree == highest_degree:
                # a tie
                highest_degree_dict.update({node_id: highest_degree})

        return highest_degree_dict


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")



class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param integer limit: number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If there are fewer cast members than the specified limit or the limit not specified, return all cast members
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'cast_id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit}, ... ]
        Important: the exclude_ids processing should occur prior to limiting output.
        """
        # collect data
        connection = http.client.HTTPSConnection('api.themoviedb.org')
        connection.request("GET", "/3/movie/" + movie_id + "/credits?api_key=" + self.api_key)
        response = connection.getresponse()
        movie_casts_raw = response.read().decode('utf-8')

        # clean data
        movie_casts_json = json.loads(movie_casts_raw)
        casts = movie_casts_json['cast']

        # buid movie casts list for a movie
        movie_casts = []
        for cast in casts:
            exclude = False
            actorid = cast['id']
            
            if exclude_ids != None:
                for id in exclude_ids:
                    if actorid == id:
                        # exclude this id
                        exclude = True
                        break
            if exclude:
                continue

            order = cast['order']
            
            if limit != None:
                if len(casts) >= limit:
                   if limit <= order:
                       # order is not interesting
                       continue

            # populate attributes
            character = cast['character']
            credit_id = cast['credit_id']
            cast_id = cast['cast_id']

            # remove comma from the name
            name = cast['name'].replace(',', '') 
            
            #name = name.replace('\u014c', '')
            #name = name.replace('\u1ea5', '')
            #name = name.replace('\u1ea1', '')

            name = name.encode("ascii", "ignore").decode("ascii")

            gender = cast['gender']
            profile_path = cast['profile_path']

            dictionary = {'cast_id': cast_id, 'character': character, 'credit_id': credit_id, 'gender': gender, 
                          'id': actorid, 'name': name, 'order': order, 'profile_pathp': profile_path}
            movie_casts.append(dictionary)
            
            if limit != None:
                if len(casts) >= limit:
                    if len(movie_casts) == limit:
                        # reached enough items
                        break

        return movie_casts 


    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        # collect data
        connection = http.client.HTTPSConnection('api.themoviedb.org')
        connection.request("GET", "/3/person/" + person_id + "/movie_credits?api_key=" + self.api_key + "&language=en-US")
        response = connection.getresponse()
        movie_credits_raw = response.read().decode('utf-8')

        # clean data
        movie_credits_json = json.loads(movie_credits_raw)
        credits = movie_credits_json['cast']

        # build movie credits list for a person
        movie_credits = []

        for credit in credits:
            vote_average = credit['vote_average']

            if vote_avg_threshold != None:
                if vote_average < vote_avg_threshold:
                    # vote average not interesting
                    continue

            # populate attributes
            if 'character' in credit:
                character = credit['character']
            else:
                character = ''

            credit_id = credit['credit_id']

            if 'release_date' in credit:
                release_date = credit['release_date']
            else:
                release_date = '2020-01-01'

            vote_count = credit['vote_count']
            video = credit['video']
            adult = credit['adult']
            title = credit['title']
            genre_ids = credit['genre_ids']
            original_language = credit['original_language']
            original_title = credit['original_title']
            popularity = credit['popularity']
            id = credit['id']
            backdrop_path = credit['backdrop_path']
            overview = credit['overview']
            poster_path = credit['poster_path']

            dictionary = {'character': character, 'credit_id': credit_id, 'release_date': release_date, 'vote_count': vote_count, 'video': video,
                         'adult': adult, 'vote_average': vote_average, 'title': title, 'genre_ids': genre_ids,
                         'original_language': original_language, 'original_title': original_title,
                         'id': id, 'backdrop_path': backdrop_path, 'overview': overview, 'poster_path': poster_path}
            
            movie_credits.append(dictionary)

        return movie_credits

#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# Build your co-actor graph on the actress 'Meryl Streep' w/ person_id 5064.
# Initialize a Graph object with a single node representing Meryl Streep
# Find all of Meryl Streep's movie credits that have a vote average >= 8.0
#
# 1. For each movie credit:
#   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   for each movie cast member:
#       using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#       using graph.add_edge(), add an edge between the Meryl Streep (actress) node
#       and each new node (co-actor/co-actress)
#
#
# Using the nodes added in the first iteration (this excludes the original node of Meryl Streep!)
#
# 2. For each node (actor / actress) added in the previous iteration:
#   get the movie credits for the actor that have a vote average >= 8.0
#   for each movie credit:
#       try to get the 3 movie cast members having an 'order' value between 0-2
#       for each movie cast member:
#           if the node doesn't already exist:
#               add the node to the graph (track all new nodes added to the graph)
#               if the edge does not exist:
#                   add an edge between the node (actor) and the new node (co-actor/co-actress)
#
#
# - Repeat the steps from # 2. until you have iterated 3 times to build an appropriately sized graph.
# - Your graph should not have any duplicate edges or nodes
# - Write out your finished graph as a nodes file and an edges file using
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. It may be necessary to insert periodic sleeps when you are building your graph.


def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return rmutombo3


def return_argo_lite_snapshot()->str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return 'https://poloclub.github.io/argo-graph-lite/#6276eb8e-8398-4bfd-9a72-59228a980ddd'


if __name__ == "__main__":

    graph = Graph()
    graph.add_node(id='5064', name='Meryl Streep')
    tmdb_api_utils = TMDBAPIUtils(api_key='9eebf02dd445673dd389c56feac267b1')

    # call functions or place code here to build graph (graph building code not graded)
    
    # get meryl movie_credits
    meryl_id = '5064'
    movie_credits = tmdb_api_utils.get_movie_credits_for_person(meryl_id, 8.0)
    index = range(len(movie_credits))

    # iteration 1

    # add meryl_id to exclude_ids
    exclude_ids = [int(meryl_id)]

    # keep track of new nodes created
    new_node_ids_iteration1 = []

    for i in index:
        movie_credit = movie_credits[i]
        movie_id = str(movie_credit['id'])
        movie_casts = tmdb_api_utils.get_movie_cast(movie_id, 3, exclude_ids)

        # do not need empty casts
        if len(movie_casts) == 0:
            continue
        
        for movie_cast in movie_casts:
            # capture new_node_id
            actor_id = movie_cast['id']
            new_node_id = str(actor_id)
            
            if new_node_id in new_node_ids_iteration1:
                # node already added
                continue

            # capture new node
            new_node_name = movie_cast['name']
            new_node_ids_iteration1.append(new_node_id)

            # Add new node and new edge
            graph.add_node(new_node_id, new_node_name)
            graph.add_edge(meryl_id, new_node_id)

    # iteration 2

    new_node_ids_iteration2 = []

    for person_id in new_node_ids_iteration1:
        # get person movie_credits
        movie_credits = tmdb_api_utils.get_movie_credits_for_person(person_id, 8.0)
        index = range(len(movie_credits))

        # add person_id to exclude_ids
        exclude_ids = [int(meryl_id), int(person_id)]

        for i in index:
            movie_credit = movie_credits[i]
            movie_id = str(movie_credit['id'])
            movie_casts = tmdb_api_utils.get_movie_cast(movie_id, 3, exclude_ids)

            # do not need empty casts
            if len(movie_casts) == 0:
                continue
        
            for movie_cast in movie_casts:
                # capture new_node_id
                actor_id = movie_cast['id']
                new_node_id = str(actor_id)

                if new_node_id in new_node_ids_iteration2:
                    # try to add edge
                    graph.add_edge(person_id, new_node_id)
                    continue

                # if node exists do not pick it up
                if (new_node_id, new_node_name) not in graph.nodes:
                    new_node_ids_iteration2.append(new_node_id)

                # capture new_node_name
                new_node_name = movie_cast['name']

                # Add new node and new edge
                graph.add_node(new_node_id, new_node_name)
                #source_id = movie_credit['actorid']
                graph.add_edge(person_id, new_node_id)

    # iteration 3

    new_node_ids_iteration3 = []

    for person_id in new_node_ids_iteration2:
        movie_credits = tmdb_api_utils.get_movie_credits_for_person(person_id, 8.0)
        index = range(len(movie_credits))

        # add ids to exclude_ids
        exclude_ids = []
        for edge in graph.edges:
            if edge[1] == person_id:
                exclude_ids.append(int(edge[0]))

        exclude_ids.append(int(person_id))

        for i in index:
            movie_credit = movie_credits[i]
            movie_id = str(movie_credit['id'])
            movie_casts = tmdb_api_utils.get_movie_cast(movie_id, 3, exclude_ids)

            # do not need empty casts
            if len(movie_casts) == 0:
                continue
        
            for movie_cast in movie_casts:
                # capture new_node_id
                actor_id = movie_cast['id']
                new_node_id = str(actor_id)

                if new_node_id in new_node_ids_iteration3:
                    # try to add edge
                    graph.add_edge(person_id, new_node_id)
                    continue

                if (new_node_id, new_node_name) not in graph.nodes:
                    new_node_ids_iteration3.append(new_node_id)

                # capture new_node_name
                new_node_name = movie_cast['name']

                # Add new node and new edge
                graph.add_node(new_node_id, new_node_name)
                #source_id = movie_credit['actorid']
                graph.add_edge(person_id, new_node_id)

    graph.write_edges_file()
    graph.write_nodes_file()

