import bpy
import bmesh
import json
import os

def export_triangulated_meshes_collection(collection_name, output_file):
    """
    Экспортирует все триангулированные меши из коллекции в JSON файл
    """
    
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        raise FileNotFoundError(f"Collection '{collection_name}' not found")
    
    collection_data = {
        'collection_name': collection_name,
        'meshes': []
    }
    
    for obj in collection.objects:
        if obj.type == 'MESH':
            mesh_data = get_triangulated_mesh_data(obj)
            if mesh_data:
                collection_data['meshes'].append(mesh_data)
        else:
            # Пропускаем не-mesh объекты (не аварийно)
            continue
    
    # Сохраняем в JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(collection_data, file, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(collection_data['meshes'])} meshes to {output_file}")

def get_triangulated_mesh_data(obj):
    """
    Возвращает данные триангулированного меша.
    Построение ordered_vertices и triangle indices должно соответствовать:
    - ordered_vertices: последовательный список вершин в порядке, в котором они
      впервые встречаются при обходе треугольников (loop_triangles).
    - triangles: тройки индексов, указывающие на позиции в ordered_vertices.
    """
    mesh = obj.data
    world_matrix = obj.matrix_world

    # Export vertices in original mesh vertex order (stable and easy to reference)
    vertices_world = []
    for v in mesh.vertices:
        world_co = world_matrix @ v.co
        vertices_world.append([float(world_co.x), float(world_co.y), float(world_co.z)])

    # Triangles as lists of original vertex indices (loop_triangles gives those indices)
    triangles_indices = [list(tri.vertices) for tri in mesh.loop_triangles]

    # Extract boundary loops (outer contour and holes) from mesh topology using bmesh
    def extract_boundary_loops(mesh_data):
        bm = bmesh.new()
        bm.from_mesh(mesh_data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        # boundary edges: edges with exactly one linked face
        boundary_edges = [e for e in bm.edges if len(e.link_faces) == 1]
        if not boundary_edges:
            bm.free()
            return []

        # build adjacency for boundary graph: vertex_index -> list(neighbour_vertex_index)
        adj = {}
        for e in boundary_edges:
            a = e.verts[0].index
            b = e.verts[1].index
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)

        # set of remaining oriented edges for traversal (use tuple of ints)
        remaining = set()
        for e in boundary_edges:
            a = e.verts[0].index
            b = e.verts[1].index
            remaining.add((a, b))
            remaining.add((b, a))

        loops = []
        visited_vertices = set()

        # Walk loops by following adjacency
        for start_v in list(adj.keys()):
            if start_v in visited_vertices:
                continue
            # choose neighbour to start
            neighs = adj.get(start_v, [])
            if not neighs:
                continue
            prev = start_v
            curr = neighs[0]
            loop = [prev, curr]
            visited_vertices.add(prev)
            # mark edge visited
            remaining.discard((prev, curr))
            remaining.discard((curr, prev))
            while True:
                nbrs = adj.get(curr, [])
                # pick next vertex that's not previous (if possible)
                next_v = None
                for v_idx in nbrs:
                    if v_idx != prev:
                        next_v = v_idx
                        break
                if next_v is None:
                    break
                prev, curr = curr, next_v
                if curr == loop[0]:
                    # closed loop
                    break
                if curr in loop:
                    # encountered already — stop to avoid infinite loop
                    break
                loop.append(curr)
                visited_vertices.add(curr)
                remaining.discard((prev, curr))
                remaining.discard((curr, prev))

            # close the loop if needed
            if loop[0] != loop[-1]:
                # if we closed via equality, append start to make explicit; otherwise leave as sequence
                if loop[0] in adj.get(loop[-1], []):
                    loop.append(loop[0])

            # only keep loops with at least 3 distinct vertices
            uniq = [v for v in loop if isinstance(v, int)]
            if len(set(uniq)) >= 3:
                # if loop ends with repeated start, remove final duplicate for compactness
                if uniq[0] == uniq[-1]:
                    uniq = uniq[:-1]
                loops.append(uniq)

        bm.free()
        return loops

    loops = extract_boundary_loops(mesh)

    # compute 2D signed area for each loop to detect orientation
    def signed_area_2d(loop_indices, verts):
        area = 0.0
        n = len(loop_indices)
        for i in range(n):
            x1, y1 = verts[loop_indices[i]][0], verts[loop_indices[i]][1]
            x2, y2 = verts[loop_indices[(i + 1) % n]][0], verts[loop_indices[(i + 1) % n]][1]
            area += (x1 * y2 - x2 * y1)
        return area / 2.0

    # If no triangles, skip export
    if not vertices_world or not triangles_indices:
        return None

    xs = [v[0] for v in vertices_world]
    ys = [v[1] for v in vertices_world]
    zs = [v[2] for v in vertices_world]
    bounds_min = [min(xs), min(ys), min(zs)]
    bounds_max = [max(xs), max(ys), max(zs)]

    # annotate loops with orientation and signed area
    loops_with_meta = []
    for loop in loops:
        if not loop:
            continue
        area = signed_area_2d(loop, vertices_world)
        orientation = 'CCW' if area > 0 else 'CW' if area < 0 else 'UNKNOWN'
        loops_with_meta.append({'indices': loop, 'area': float(area), 'orientation': orientation})

    return {
        'name': obj.name,
        'vertices': vertices_world,  # all vertices in original mesh order
        'triangles': triangles_indices,  # triangles referencing original vertex indices
        'loops': loops_with_meta,  # explicit boundary loops (outer + holes)
        'vertex_count': len(vertices_world),
        'triangle_count': len(triangles_indices),
        'bounds': {
            'min': bounds_min,
            'max': bounds_max
        }
    }

# Использование в Blender
if __name__ == "__main__":
    export_triangulated_meshes_collection(
        collection_name="Planes",  # Замените на имя вашей коллекции
        output_file=r"C:\Users\vladi\Documents\CLONE_Art-gallery-theorem\Visual_charts\Examples\Vectorized_plans\meshes_data.json"  # Укажите ваш путь
    )