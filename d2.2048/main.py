import random
import tkinter
import tkinter.messagebox
from tkinter import Label


class Matrix2048:
    """实现业务逻辑"""

    def __init__(self, column: int = 4):
        """
        创建矩阵
        :param column: 矩阵行列数
        """
        self.column = column
        self.matrix = [[0 for _ in range(column)] for _ in range(column)]

    def generate_num(self):
        """
        生成新数字
        """
        # 找出所有 0 的位置
        zero_positions = [(i, j) for i in range(len(self.matrix))
                          for j in range(len(self.matrix[i])) if self.matrix[i][j] == 0]
        # 如果存在 0，则随机选择一个位置并将其值改为 2
        if zero_positions:
            i, j = random.choice(zero_positions)
            self.matrix[i][j] = 2

    def is_over(self) -> bool:
        """
        判断是否结束游戏
        :return:结束返回True，未结束返回False
        """
        # 矩阵有0则未结束
        if any(0 in row for row in self.matrix):
            return False
        # 水平方向有相同数字则未结束
        for row in range(self.column):
            for col in range(self.column - 1):  # 注意数组不要越界
                if self.matrix[row][col] == self.matrix[row][col + 1]:
                    return False
        # 垂直方向有相同数字则未结束
        for row in range(self.column - 1):
            for col in range(self.column):
                if self.matrix[row][col] == self.matrix[row + 1][col]:
                    return False
        # 以上条件不满足则游戏结束
        return True

    def init(self):
        """
        新建游戏和重置游戏
        """
        self.matrix = [[0 for _ in range(self.column)] for _ in range(self.column)]
        self.generate_num()
        self.generate_num()

    @staticmethod
    def compress(row):
        """
        将行里非0数字左移，并在右侧添加0
        :param row: list
        :return: list
        """
        new_row = [num for num in row if num != 0]  # 移除0
        return new_row + [0] * (len(row) - len(new_row))  # 补齐0

    @staticmethod
    def merge(row):
        """
        合并数字，向左移动
        :param row:list
        :return: list
        """
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2  # 相同数字合并
                row[i + 1] = 0
        return row

    def matrix_move(self):
        """
        实现矩阵的左移合并
        """
        for i in range(self.column):
            self.matrix[i] = self.compress(self.matrix[i])  # 左移
            self.matrix[i] = self.merge(self.matrix[i])  # 合并
            self.matrix[i] = self.compress(self.matrix[i])  # 再次左移，清理合并后产生的空位

    def reverse(self):
        """
        反转矩阵中的每一行，用于向右移动
        """
        self.matrix = [row[::-1] for row in self.matrix]

    def transpose(self):
        """
        转置矩阵，用于实现上下移动
        """
        self.matrix = [list(row) for row in zip(*self.matrix)]

    def move(self, position: str):
        """
        根据移动方向对矩阵进行移动和合并
        :param position: 移动方向 ('left', 'right', 'up', 'down')
        """
        if position == 'left':
            self.matrix_move()
        elif position == 'right':
            self.reverse()  # 反转矩阵
            self.matrix_move()
            self.reverse()  # 恢复矩阵
        elif position == 'up':
            self.transpose()  # 转置矩阵
            self.matrix_move()
            self.transpose()  # 恢复矩阵
        elif position == 'down':
            self.transpose()
            self.reverse()
            self.matrix_move()
            self.reverse()
            self.transpose()

        # 每次移动后生成一个新的数字
        self.generate_num()


class Window2048:
    """
    建立窗体GUI
    """

    def __init__(self, column: int = 4):
        self.init_setting(column)
        self.data = Matrix2048(column)
        self.root = self.init_root()
        self.t = 0  # 判断游戏结束时用
        self.main()

    def init_setting(self, column):
        """
        配置初始化
        :param column:
        :return:
        """
        self.column = column
        # 棋盘中格子的间隔，单位为px
        self.space_size = 12

        # 棋盘中格子的大小，单位为px
        self.cell_size = 80

        # 用于存储tkinter.Lable对象
        self.emts = []  # 存储lable对象

        # 用于存储游戏的样式信息，如背景色，字体颜色，字体大小等
        self.style = {
            'page': {'bg': '#d6dee0', },
            # 0 ~ 4 灰色系  bg 背景颜色， fg字体颜色， fz字体大小
            0: {'bg': '#EEEEEE', 'fg': '#EEEEEE', 'fz': 30},
            2 ** 1: {'bg': '#E5E5E5', 'fg': '#707070', 'fz': 30},
            2 ** 2: {'bg': '#D4D4D4', 'fg': '#707070', 'fz': 30},
            # 8 ～ 16 橙色系
            2 ** 3: {'bg': '#FFCC80', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 4: {'bg': '#FFB74D', 'fg': '#FAFAFA', 'fz': 30},
            # 32 ～ 64 红色系
            2 ** 5: {'bg': '#FF7043', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 6: {'bg': '#FF5722', 'fg': '#FAFAFA', 'fz': 30},
            # 128～2048 黄色系
            2 ** 7: {'bg': '#FFEE58', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 8: {'bg': '#FFEB3B', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 9: {'bg': '#FDD835', 'fg': '#FAFAFA', 'fz': 30},
            # 1024~2048 橙色系
            2 ** 10: {'bg': '#FF9800', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 11: {'bg': '#FB8C00', 'fg': '#FAFAFA', 'fz': 28},
            # 4096 +  红色系
            2 ** 12: {'bg': '#fb3030', 'fg': '#FAFAFA', 'fz': 28},
            2 ** 13: {'bg': '#e92e2e', 'fg': '#FAFAFA', 'fz': 28},
            2 ** 14: {'bg': '#da1e1e', 'fg': '#FAFAFA', 'fz': 24},
            # 2**15 +  黑色 超过2**15颜色不再改变
            2 ** 15: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 22},
            2 ** 16: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 17: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 18: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 19: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 18},
            2 ** 20: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 17},
            2 ** 21: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 16},
            2 ** 22: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 15},
            2 ** 23: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 14},
            2 ** 24: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 13},
            2 ** 25: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 12},
        }

    def init_root(self):
        """
        窗口初始化
        :return:
        """
        column = self.column
        space_size = self.space_size
        cell_size = self.cell_size

        # 创建根窗口
        root = tkinter.Tk()
        root.title('2048')

        # 根窗口尺寸设置
        window_w = column * (space_size + cell_size) + space_size
        window_h = window_w + cell_size + 2 * space_size
        root.geometry(f'{window_w}x{window_h}')

        # 顶栏
        header_h = cell_size + space_size * 2
        header = tkinter.Frame(root, height=header_h, width=window_w)
        self.init_header(header)

        # 棋盘
        table = tkinter.Frame(root, height=window_w, width=window_w)
        self.init_table(table)

        return root

    def init_header(self, header):
        header.pack()

    def init_table(self, table):
        table.pack()
        for row in range(self.column):
            row_emts = []
            for col in range(self.column):
                label = Label(table, width=4, height=2, font=('Helvetica', 24, 'bold'), text='',
                              relief='ridge', bg=self.style[0]['bg'], fg=self.style[0]['fg'])
                label.grid(row=row, column=col, padx=self.space_size, pady=self.space_size)
                row_emts.append(label)
            self.emts.append(row_emts)

    def update_ui(self):
        """
        更新UI
        :return:
        """
        for i in range(self.column):
            for j in range(self.column):
                value = self.data.matrix[i][j]
                style = self.style.get(value, self.style[2 ** 15])
                self.emts[i][j].configure(
                    text=str(value) if value != 0 else '',
                    bg=style['bg'],
                    fg=style['fg'],
                    font=('Helvetica', style['fz'], 'bold')
                )

    def key_event(self, event):
        """
        事件循环
        :param event:键盘事件
        :return:
        """
        direction_keys = {
            'Up': 'up', 'Down': 'down', 'Left': 'left', 'Right': 'right'
        }
        if event.keysym in direction_keys:
            self.data.move(direction_keys[event.keysym])
            self.update_ui()
            if self.data.is_over():
                print("Game Over!")
                self.root.after(2000, self.reset_game)

    def reset_game(self):
        """
        重置游戏
        :return:
        """
        self.data.init()
        self.update_ui()

    def main(self):
        """
        主程序
        :return:
        """
        self.reset_game()
        self.root.bind("<Key>", self.key_event)
        self.root.mainloop()

g = Window2048(4)