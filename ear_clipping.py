from frame import Triangle_Frame, Frame, Ear_Frame, FrameOptions, clear_frames
from triangulated_polygon import Triangulated_Polygon
import html_generator  

# Retorna índice da primeira verdade em um lista de Bool
def search_true(x):
    for i in range(len(x)):
        if x[i] == True:
            return i
    raise ValueError("Nothing found on list")

class Ear_clipping:
    def __init__(self, initial_polygon, width, height):
        self.width = width
        self.height = height
        self.polygon_list = [initial_polygon]
        self.frame_list = []
        self.new_edges = []
        self.triangles = []

        xlim = 0
        ylim = 0
        for point in initial_polygon.points:
            xlim = max(xlim, point.x)
            ylim = max(ylim, point.y)
        xlim *= 1.1
        ylim *= 1.1

        self.scale = min(width/xlim, height/ylim)

    def triangulation(self):
        current_polygon = self.polygon_list[0]
        ear_list = [False] * current_polygon.get_size()

        # Para cada verificação, adiciona 2 frames
        for i in range(current_polygon.get_size()):
            verify_frame = Ear_Frame(current_polygon, ear_list, FrameOptions(self.scale, self.width, self.height), i)
            self.frame_list.append(verify_frame)

            response_frame = Ear_Frame(current_polygon, ear_list, FrameOptions(self.scale, self.width, self.height), i)

            if current_polygon.is_ear(i):
                ear_list[i] = True
                response_frame.set_vertex_type(i, "green")
            else:
                response_frame.set_vertex_type(i, "black")

            self.frame_list.append(response_frame)


        while current_polygon.get_size() > 3:
            to_be_removed = search_true(ear_list)

            # Registra novo triângulo na triangulação final
            idx1 = current_polygon.get_points()[to_be_removed-1 if to_be_removed>0 else 0].idx
            idx2 = current_polygon.get_points()[to_be_removed].idx
            idx3 = current_polygon.get_points()[to_be_removed+1 if to_be_removed<current_polygon.get_size()-1 else current_polygon.get_size()-1].idx
            self.new_edges.append([ idx1, idx3 ])
            self.triangles.append([ idx1, idx2, idx3 ])

            # Marca que vértice será removido
            removed_frame = Frame(current_polygon, ear_list, FrameOptions(self.scale, self.width, self.height))
            removed_frame.set_vertex_type(to_be_removed, "red")
            self.frame_list.append(removed_frame)

            ear_list.pop(to_be_removed)
            new_polygon = current_polygon.removed_vertex(to_be_removed)

            # Vértice foi removido
            new_polygon_frame = Frame(new_polygon, ear_list, FrameOptions(self.scale, self.width, self.height))
            self.frame_list.append(new_polygon_frame)

            previous_index = to_be_removed-1 if to_be_removed > 0 else new_polygon.get_size()-1
            next_index = to_be_removed if to_be_removed < new_polygon.get_size()-1 else 0

            list_index = [ previous_index, next_index ]

            for idx in list_index:
                verify_frame = Ear_Frame(new_polygon, ear_list, FrameOptions(self.scale, self.width, self.height), idx)
                self.frame_list.append(verify_frame)

                ear_list[idx] = new_polygon.is_ear(idx)

                response_frame = Ear_Frame(new_polygon, ear_list, FrameOptions(self.scale, self.width, self.height), idx)
                if ear_list[idx]:
                    response_frame.set_vertex_type(idx, "red")
                else:
                    response_frame.set_vertex_type(idx, "black")
                self.frame_list.append(response_frame)

            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)

        # Frame vazio para fim
        # self.frame_list.append(EmptyFrame())
    
    def get_polygons(self):
        return self.polygon_list
    
    def get_new_edges(self):
        return self.new_edges

    def get_result(self):
        return Triangulated_Polygon(self.polygon_list[0], self.new_edges, self.triangles)

    def generate_html(self):
        clear_frames()

        zero_list = [ 0 ]* self.polygon_list[0].get_size()
        background_frame = Triangle_Frame(self.get_result(), zero_list, FrameOptions(self.scale, self.width, self.height, 0.2))

        for i, frame in enumerate(self.frame_list):
            with open(f"./frames/frame{i}.svg", "w") as file:
                file.write(frame.generate_svg(background_frame))

        return html_generator.get(len(self.frame_list), self.width, self.height)
    
