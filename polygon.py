from geometry import Point

class Polygon:
<<<<<<< HEAD
    def __init__(self, file_name='', points=[], copy_polygon=None):
        if copy_polygon != None:
            self.size = copy_polygon.size
            self.points = copy_polygon.points.copy()
        else:
            self.size = len(points)
            self.points = points
=======
    def __init__(self, file_name='', points=None):
        self.size = len(points)
        self.points = points

        if file_name.endswith('.txt'):
            self.read_from_file(file_name)
        elif file_name.endswith('.pol'):
            self.read_from_pol(file_name)
>>>>>>> 754eeb3384d062780a393dfe77ec694f34a5da13

            if file_name.endswith('.txt'):
                self.read_from_file(file_name)
            elif file_name.endswith('.pol'):
                self.read_from_pol(file_name)
            elif file_name != '':                 
                raise FileNotFoundError("Não foi implementado leitura desse tipo de arquivo")

    # Lê do arquivo .txt
    def read_from_file(self, file_name):
        self.points = []
        with open(file_name, 'r') as file:
            self.size = int(file.readline().strip())
            for i in range(self.size):
                x, y = map(int, file.readline().strip().split())
                self.points.append(Point(x,y,i))

    # Lê do arquivo .pol
    def read_from_pol(self, file_path):
        self.points = []
        with open(file_path, 'r') as file:
            line = file.readline().strip()
            parts = line.split()
            N = int(parts[0])
            self.size = N
            coordinates = parts[1:]

            if len(coordinates) != 2 * N:
                raise ValueError(f"Expected {2 * N} coordinate parts, but got {len(coordinates)}")

            for i in range(N):
                p, q = map(int, coordinates[2 * i].split('/'))
                r, s = map(int, coordinates[2 * i + 1].split('/'))
                x = p / q
                y = r / s
                self.points.append(Point(x, y, i))

        self.ear_list = [False]*self.size

    # retorna quantidade de pontos
    def get_size(self):
        return self.size

    # adidciona vertex
    def add_vertex(self, Point):
        self.size += 1
        self.points.append(Point)

    # remove vértice
    def removed_vertex(self, idx):
        new_points = []
        for i, pt in enumerate(self.points):
            if i != idx:
                new_points.append(Point(pt.x, pt.y, pt.idx))
        return Polygon('', new_points)
    
    # retorna lista de pontos
    def get_points(self):
        return self.points
