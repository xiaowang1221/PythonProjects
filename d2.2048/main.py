import random


class Matrix2048():
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
        matrix = self.matrix
        column = self.column
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
                if self.matrix[row][col] == self.matrix[row][col+1]:
                    return False
        # 垂直方向有相同数字则未结束
        for row in range(self.column - 1):
            for col in range(self.column):
                if self.matrix[row][col] == self.matrix[row+1][col]:
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

    def matrix_move(self):
        """
        移动合并
        :return:
        """
        pass

    def move(self, position):
        """
        向移动方位移动
        :param position: 移动方向
        :return:
        """
        pass


