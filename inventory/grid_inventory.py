import pygame


class GridInventory:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]
        self.items = []  # (item, x, y)
        self.dragged_item = None
        self.drag_offset = (0, 0)

    def can_place(self, item, x, y):
        if x + item.width > self.columns or y + item.height > self.rows:
            return False
        for dy in range(item.height):
            for dx in range(item.width):
                if self.grid[y + dy][x + dx] is not None:
                    return False
        return True

    def place_item(self, item, x, y):
        if not self.can_place(item, x, y):
            return False
        for dy in range(item.height):
            for dx in range(item.width):
                self.grid[y + dy][x + dx] = item
        self.items.append((item, x, y))
        return True

    def remove_item(self, item):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[y][x] == item:
                    self.grid[y][x] = None
        self.items = [entry for entry in self.items if entry[0] != item]

    def start_drag(self, mouse_pos, tile_size):
        mx, my = mouse_pos
        grid_x = mx // tile_size
        grid_y = my // tile_size
        for item, ix, iy in self.items:
            if ix <= grid_x < ix + item.width and iy <= grid_y < iy + item.height:
                self.remove_item(item)
                self.dragged_item = item
                self.drag_offset = (grid_x - ix, grid_y - iy)
                return

    def drop_drag(self, mouse_pos, tile_size):
        if self.dragged_item is None:
            return
        mx, my = mouse_pos
        grid_x = mx // tile_size - self.drag_offset[0]
        grid_y = my // tile_size - self.drag_offset[1]
        placed = self.place_item(self.dragged_item, grid_x, grid_y)
        if not placed:
            pass
        self.dragged_item = None

